import os
import re
import sys
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

pytest_plugins = [
    "fixtures.driver_fixture",
    "fixtures.app_fixtures",
    "fixtures.page_fixtures",
    "fixtures.flow_fixtures",
    "fixtures.player_fixtures",
    "fixtures.data_fixtures",
]


def pytest_addoption(parser):
    parser.addoption("--target", action="store", default=None)
    parser.addoption("--bundle-id", action="store", default=None)
    parser.addoption("--udid", action="store", default=None)
    parser.addoption("--device-name", action="store", default=None)
    parser.addoption("--app-reset", action="store", default=None)


@pytest.hookimpl(tryfirst=True)
def pytest_configure(config):
    import os

    mapping = {
        "--target": "TARGET",
        "--bundle-id": "BUNDLE_ID",
        "--udid": "UDID",
        "--device-name": "DEVICE_NAME",
        "--app-reset": "APP_RESET_STRATEGY",
    }
    for option, env_key in mapping.items():
        value = config.getoption(option.lstrip("-").replace("-", "_"))
        if value:
            os.environ[env_key] = value

    config.addinivalue_line("markers", "smoke: quick sanity checks")
    config.addinivalue_line("markers", "regression: full regression suite")
    config.addinivalue_line("markers", "real_device: requires a physical device")
    config.addinivalue_line("markers", "simulator: requires a simulator")
    config.addinivalue_line(
        "markers",
        "app_reset(strategy, bundle_id=None): force_close, clear, reinstall or none",
    )
    config.addinivalue_line("markers", "group_booking: needs the host device plus the PLAYER_<n> devices")
    _device_html_report(config)
    config.addinivalue_line("markers", "regression_existing: end to end booking per payment method on existing accounts")
    config.addinivalue_line("markers", "device(n, app=None): run on the DEVICE_<n> block of the env file, optionally with a specific .app build")
    _validate_workers(config)


def _device_html_report(config):
    device = os.environ.get("DEVICE", "").strip()
    htmlpath = getattr(config.option, "htmlpath", None)
    if device and htmlpath == "reports/report.html":
        config.option.htmlpath = f"reports/report_device{device}.html"


def _validate_workers(config):
    import os

    if os.getenv("PYTEST_XDIST_WORKER"):
        return
    count = getattr(config.option, "numprocesses", None)
    if not count:
        return
    if not isinstance(count, int):
        raise pytest.UsageError(
            f"-n {count} is not supported, pass a number: every worker needs its own WORKER_<n>_UDID")
    problems = []
    claimed = {}

    def claim(kind, value, owner):
        key = (kind, str(value))
        if key in claimed:
            problems.append(f"{owner} uses {kind} {value}, already used by {claimed[key]}")
        else:
            claimed[key] = owner

    device_blocks = sorted({key[len("DEVICE_"):-len("_UDID")] for key in os.environ
                            if key.startswith("DEVICE_") and key.endswith("_UDID") and os.environ[key]})
    for device in device_blocks:
        owner = f"device {device}"
        claim("device", os.environ[f"DEVICE_{device}_UDID"], owner)
        for port in ("WDA_LOCAL_PORT", "MJPEG_PORT"):
            if os.getenv(f"DEVICE_{device}_{port}"):
                claim("port", os.getenv(f"DEVICE_{device}_{port}"), owner)

    for index in range(count):
        owner = f"worker gw{index}"

        def env(name, default=None):
            return os.getenv(f"WORKER_{index}_{name}") or default

        udid = env("UDID")
        if not udid:
            if not device_blocks:
                problems.append(f"WORKER_{index}_UDID is not set for {owner}")
            continue
        target = env("TARGET", os.getenv("TARGET", "simulator")).lower()
        if target not in ("simulator", "real_device"):
            problems.append(f"WORKER_{index}_TARGET must be simulator or real_device, found {target}")
        claim("device", udid, owner)
        claim("port", env("WDA_LOCAL_PORT", os.getenv("WDA_LOCAL_PORT", "8100")), owner)
        if env("MJPEG_PORT"):
            claim("port", env("MJPEG_PORT"), owner)

    player = 1
    while os.getenv(f"PLAYER_{player}_UDID"):
        owner = f"group booking player {player}"
        claim("device", os.getenv(f"PLAYER_{player}_UDID"), owner)
        claim("port", os.getenv(f"PLAYER_{player}_WDA_LOCAL_PORT") or 8100 + player, owner)
        claim("port", int(os.getenv("PLAYER_MJPEG_PORT") or 9101) + player - 1, owner)
        player += 1

    if problems:
        raise pytest.UsageError("parallel device setup is not valid:\n  - " + "\n  - ".join(problems))


FEATURE_ORDER = (
    "test_onboarding",
    "test_login",
    # "test_swing_credit",
    # "test_driving_range",
    # "test_tee_time",
    # "test_event",
)


def _feature_order():
    from config.settings import settings

    raw = [name.strip() for name in settings.TEST_ORDER.split(",") if name.strip()]
    names = raw or list(FEATURE_ORDER)
    return {name: index for index, name in enumerate(names)}


def _module_name(item):
    path = getattr(item, "path", None)
    return path.stem if path else Path(str(item.fspath)).stem


def _tc_id(item):
    callspec = getattr(item, "callspec", None)
    if callspec is None:
        return ""
    return str(callspec.params.get("TC_ID") or "")


def _natural_key(text):
    return tuple(
        int(part) if part.isdigit() else part.lower()
        for part in re.split(r"(\d+)", text)
        if part
    )


@pytest.hookimpl(tryfirst=True)
def pytest_collection_modifyitems(session, config, items):
    from config.settings import settings
    from helpers.logger import get_logger

    from config.capabilities import marker_device

    for item in items:
        device = marker_device(list(item.iter_markers("device")))
        if device is not None:
            item.add_marker(pytest.mark.xdist_group(f"device_{device}"))
    if not settings.SORT_TESTS:
        return
    order = _feature_order()
    selected = [item for item in items if _module_name(item) in order]
    dropped = [item for item in items if _module_name(item) not in order]
    if selected and dropped:
        config.hook.pytest_deselected(items=dropped)
        get_logger("conftest").info(
            "feature order runs " + ", ".join(order)
            + " | skipped " + ", ".join(sorted({_module_name(i) for i in dropped}))
        )
        items[:] = selected
    unlisted = len(order)
    positions = {id(item): index for index, item in enumerate(items)}

    def key(item):
        module = _module_name(item)
        return (
            order.get(module, unlisted),
            module.lower(),
            _natural_key(_tc_id(item)),
            positions[id(item)],
        )

    items.sort(key=key)


def pytest_runtest_setup(item):
    from helpers.reporter import reporter

    reporter.start_test(item.nodeid)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    from helpers.reporter import reporter

    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        item.test_failed = True
    setattr(item, f"report_{report.when}", report)
    if report.when == "call":
        error = str(call.excinfo.value) if call.excinfo else None
        if report.failed:
            from config.settings import settings

            if settings.SCREENSHOT_ON_FAILURE:
                item.failure_screenshot = reporter.capture_failure(item.name)
        finished = reporter.finish_test(report.outcome, error)
        if finished and finished["steps"]:
            report.sections.append(("steps", "\n".join(reporter.lines(finished))))
        pdf_path = reporter.save_pdf(finished)
        if pdf_path:
            item.pdf_report = pdf_path
            report.sections.append(("pdf", pdf_path))


def pytest_terminal_summary(terminalreporter):
    from config.settings import settings
    from helpers.reporter import reporter

    if settings.PDF_REPORT and reporter.pdf_paths and not settings.KEEP_EVIDENCE:
        reporter.cleanup_run()
    elif not settings.PDF_REPORT:
        reporter.cleanup_screenshots()
    path = reporter.save()
    if path:
        totals = reporter.payload()["totals"]
        terminalreporter.write_line(
            f"steps: {totals['steps']} | screenshots: {totals['screenshots']} | report: {path}"
        )
