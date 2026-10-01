import importlib
import json
import os
import re
import time
from pathlib import Path

from config.settings import settings
from helpers.logger import get_logger

log = get_logger("reporter")

_LOCATOR_NAMES = None
_STEP_MARK = "==>"
_ACTION_MARK = "-"


def _load_locator_names():
    mapping = {}
    root = Path(__file__).resolve().parent.parent
    folder = root / "locators"
    for module_file in sorted(folder.rglob("*_locators.py")):
        dotted = ".".join(module_file.relative_to(root).with_suffix("").parts)
        try:
            module = importlib.import_module(dotted)
        except Exception as exc:
            log.warning(f"locator names not loaded from {module_file.name}: {exc}")
            continue
        for candidate in vars(module).values():
            if not isinstance(candidate, type) or not candidate.__name__.endswith("Locators"):
                continue
            for key, value in vars(candidate).items():
                if key.startswith("_") or not isinstance(value, str):
                    continue
                mapping.setdefault(value, key)
    return mapping


def describe(locator):
    global _LOCATOR_NAMES
    if isinstance(locator, (tuple, list)) and len(locator) == 2:
        return str(locator[1])
    text = str(locator)
    if _LOCATOR_NAMES is None:
        _LOCATOR_NAMES = _load_locator_names()
    name = _LOCATOR_NAMES.get(text)
    if name:
        return name
    for xpath, constant in _LOCATOR_NAMES.items():
        if "{}" not in xpath:
            continue
        head = xpath.split("{}")[0]
        if len(head) > 10 and text.startswith(head):
            return constant
    return text


def _slug(text, limit=40):
    cleaned = re.sub(r"[^a-zA-Z0-9]+", "_", str(text)).strip("_").lower()
    return cleaned[:limit] or "step"


def _clip(value, limit=120):
    text = str(value)
    return text if len(text) <= limit else f"{text[:limit]}..."


class Reporter:
    def __init__(self):
        worker = os.getenv("PYTEST_XDIST_WORKER", "")
        device = os.getenv("DEVICE", "").strip()
        self.run_id = (time.strftime("%Y%m%d_%H%M%S") + (f"_device{device}" if device else "")
                       + (f"_{worker}" if worker else ""))
        self.tests = []
        self.current = None
        self.driver = None
        self.pdf = None
        self.pdf_paths = []
        self.force_screenshots = False

    @property
    def enabled(self):
        return settings.STEP_REPORT

    def bind(self, driver):
        self.driver = driver

    def unbind(self):
        self.driver = None

    def start_test(self, name):
        if not self.enabled:
            return None
        self.current = {
            "name": name,
            "started_at": time.time(),
            "started": time.strftime("%H:%M:%S"),
            "duration": 0.0,
            "status": "running",
            "error": None,
            "steps": [],
        }
        self.tests.append(self.current)
        return self.current

    def finish_test(self, status, error=None):
        if not self.current:
            return None
        self.current["status"] = status
        self.current["duration"] = round(time.time() - self.current["started_at"], 2)
        if error:
            self.current["error"] = _clip(error, 2000)
        finished = self.current
        self.current = None
        return finished

    def save_pdf(self, test):
        if not self.pdf or not test:
            return None
        path = self.pdf.save(test)
        self.pdf = None
        self.force_screenshots = False
        if path:
            self.pdf_paths.append(path)
        return path

    def add(self, text, kind="step", value=None, screenshot=None, evidence=False):
        if not self.enabled:
            return None
        if screenshot is None and (settings.STEP_SCREENSHOTS or (self.force_screenshots and evidence)):
            screenshot = self.capture(text)
        started = self.current["started_at"] if self.current else time.time()
        entry = {
            "index": len(self.current["steps"]) + 1 if self.current else 0,
            "kind": kind,
            "text": text,
            "value": None if value is None else _clip(value),
            "elapsed": round(time.time() - started, 2),
            "time": time.strftime("%H:%M:%S"),
            "screenshot": screenshot,
            "evidence": bool(evidence),
        }
        if self.current is not None:
            self.current["steps"].append(entry)
        self.echo(entry)
        return entry

    def echo(self, entry):
        if not settings.STEP_PRINT:
            return
        if entry["kind"] == "step":
            line = f"\n{_STEP_MARK} {entry['text']}"
        else:
            line = f"   {_ACTION_MARK} {entry['kind']:<10} {entry['text']}"
        if entry["value"] is not None:
            line = f"{line} -> {entry['value']}"
        print(line, flush=True)
        if entry["screenshot"]:
            print(f"     shot {entry['screenshot']}", flush=True)

    def step(self, text, screenshot=None):
        return self.add(text, kind="step", screenshot=screenshot)

    def action(self, verb, locator, detail=None):
        text = f"{verb} {describe(locator)}"
        if detail is not None:
            text = f"{text} = {_clip(detail, 60)}"
        return self.add(text, kind="action")

    def read(self, verb, locator, value):
        return self.add(f"{verb} {describe(locator)}", kind="read", value=value)

    def table(self, title, text):
        entry = self.add(title, kind="table", screenshot=self.capture(title), evidence=True)
        if entry is not None:
            entry["table"] = text
        return entry

    def note(self, text, evidence=False):
        return self.add(text, kind="note", evidence=evidence)

    def capture(self, label="step"):
        if self.driver is None:
            return None
        try:
            from helpers import media

            folder = Path(settings.SCREENSHOT_DIR) / "steps" / self.run_id
            index = len(self.current["steps"]) + 1 if self.current else 0
            return media.screenshot(self.driver, f"{index:03d}_{_slug(label)}", directory=folder)
        except Exception as exc:
            log.warning(f"step screenshot failed: {exc}")
            return None

    def capture_failure(self, label="failure"):
        if not self.enabled or self.driver is None:
            return None
        path = self.capture(label)
        if not path:
            return None
        steps = self.current["steps"] if self.current else []
        if steps and not steps[-1].get("screenshot"):
            steps[-1]["screenshot"] = path
            steps[-1]["failed"] = True
        else:
            entry = self.add("failed here", kind="failure", screenshot=path, evidence=True)
            if entry:
                entry["failed"] = True
        log.info(f"failure screenshot {path}")
        return path

    def cleanup_screenshots(self, keep_failures=True):
        removed = 0
        for test in self.tests:
            steps = test["steps"]
            keep = steps[-1] if keep_failures and steps and test["status"] == "failed" else None
            for entry in steps:
                path = entry.get("screenshot")
                if not path or entry is keep:
                    continue
                try:
                    Path(path).unlink()
                except FileNotFoundError:
                    pass
                except OSError as exc:
                    log.warning(f"screenshot not removed {path}: {exc}")
                    continue
                entry["screenshot"] = None
                removed += 1
        log.info(f"screenshots removed {removed}")
        return removed

    def attach(self, path, caption="attachment", evidence=True):
        return self.add(caption, kind="attachment", screenshot=str(path), evidence=evidence)

    def lines(self, test=None):
        target = test or self.current
        if not target:
            return []
        header = f"{target['name']} [{target['status']}] {target['duration']}s"
        rows = [header]
        for entry in target["steps"]:
            row = f"  {entry['index']:>3}. {entry['elapsed']:>7.2f}s  {entry['kind']:<10} {entry['text']}"
            if entry["value"] is not None:
                row = f"{row} -> {entry['value']}"
            if entry["screenshot"]:
                row = f"{row}\n        shot: {entry['screenshot']}"
            rows.append(row)
        if target["error"]:
            rows.append(f"  error: {target['error']}")
        return rows

    def payload(self):
        return {
            "run_id": self.run_id,
            "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
            "target": settings.TARGET,
            "device": settings.DEVICE_NAME,
            "bundle_id": settings.BUNDLE_ID,
            "totals": {
                "tests": len(self.tests),
                "passed": sum(1 for t in self.tests if t["status"] == "passed"),
                "failed": sum(1 for t in self.tests if t["status"] == "failed"),
                "steps": sum(len(t["steps"]) for t in self.tests),
                "screenshots": sum(
                    1 for t in self.tests for s in t["steps"] if s["screenshot"]
                ),
            },
            "tests": self.tests,
        }

    def cleanup_run(self):
        import shutil

        removed = 0
        for test in self.tests:
            for entry in test["steps"]:
                path = entry.get("screenshot")
                if not path:
                    continue
                try:
                    Path(path).unlink()
                    removed += 1
                except FileNotFoundError:
                    pass
                except OSError as exc:
                    log.warning(f"screenshot not removed {path}: {exc}")
                    continue
                entry["screenshot"] = None
        folder = Path(settings.SCREENSHOT_DIR) / "steps" / self.run_id
        if folder.exists():
            shutil.rmtree(folder, ignore_errors=True)
        log.info(f"run evidence removed, {removed} screenshots deleted")
        return removed

    def save(self):
        if not self.enabled or not self.tests:
            return None
        if self.pdf_paths and not settings.KEEP_EVIDENCE:
            log.info("step report skipped, the pdf reports are the evidence")
            return None
        folder = Path(settings.REPORT_DIR) / "steps"
        folder.mkdir(parents=True, exist_ok=True)
        json_path = folder / f"run_{self.run_id}.json"
        text_path = folder / f"run_{self.run_id}.txt"
        with open(json_path, "w", encoding="utf-8") as handle:
            json.dump(self.payload(), handle, indent=2)
        with open(text_path, "w", encoding="utf-8") as handle:
            for test in self.tests:
                handle.write("\n".join(self.lines(test)))
                handle.write("\n\n")
        log.info(f"step report saved {json_path}")
        return str(json_path)


reporter = Reporter()
