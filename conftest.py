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


def pytest_collection_modifyitems(session, config, items):
    from config.settings import settings
    from helpers.logger import get_logger

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
