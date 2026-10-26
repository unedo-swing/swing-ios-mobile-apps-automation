import getpass
import math
import re
import time
from pathlib import Path

from config.settings import ROOT_DIR, settings
from helpers.logger import get_logger
from helpers.reporter import reporter

log = get_logger("pdf")

COMPANY = "PT Silverwing Wisteria Indosport"
DEPARTMENT = "Dept. QA Automation Swing"
REPORT_LABEL = "Appium Report Testing"
REPORTING_BY = "Automation Team Swing"
TOOLS = "Appium - Python"
FOOTER_TEXT = "AUTOMATION TESTING REPORT - PT SILVERWING WISTERIA INDOSPORT"

LOGO = ROOT_DIR / "assets" / "swing_report_logo.png"
LOGO_WHITE = ROOT_DIR / "assets" / "swing_report_logo_white.png"

BRAND = (92, 0, 229)
BRAND_TINT = (226, 214, 253)
INK = (33, 33, 33)
GREY = (110, 110, 110)
LINE = (196, 196, 196)
BAND = (238, 240, 245)
PASS_COLOR = (26, 143, 68)
FAIL_COLOR = (198, 40, 40)

MARGIN = 18
HEADER_H = 34
FOOTER_H = 20
TOC_PER_PAGE = 20
IMAGE_MAX_H = 190
TABLE_IMAGE_H = 100
IMAGE_MAX_W = 150


def _slug(text, limit=70):
    cleaned = re.sub(r'[\\/:*?"<>|\n\r\t]+', " ", str(text)).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    return cleaned[:limit] or "report"


def _safe(text):
    return str(text).encode("latin-1", "replace").decode("latin-1")


def _image_size(path):
    try:
        from PIL import Image

        with Image.open(path) as image:
            return image.size
    except Exception:
        return None


def _clock(stamp):
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(stamp))


def _elapsed(seconds):
    total = int(seconds or 0)
    return f"{total // 3600:02d}:{total % 3600 // 60:02d}:{total % 60:02d}"


def _status_of(entry):
    return "FAILED" if entry.get("failed") else "PASSED"


class PdfReport:
    def __init__(self, name, tc_id=None):
        self.name = name
        self.tc_id = tc_id
        self.created = time.time()
        self.path = None
        self.failed = False

    def title(self):
        title = f"{self.tc_id} {self.name}" if self.tc_id else str(self.name)
        return f"FAILED - {title}" if self.failed else title

    def _document(self):
        from fpdf import FPDF

        report = self

        class Document(FPDF):
            def header(self):
                if self.page_no() == 1:
                    return
                if LOGO.exists():
                    self.image(str(LOGO), x=MARGIN, y=12, h=9)
                self.set_xy(MARGIN + 54, 10.5)
                self.set_font("helvetica", "", 13)
                self.set_text_color(*INK)
                self.cell(95, 6, _safe(COMPANY))
                self.set_xy(MARGIN + 54, 17)
                self.set_font("helvetica", "", 8.5)
                self.set_text_color(*GREY)
                self.cell(95, 5, _safe(DEPARTMENT))
                self.set_xy(MARGIN + 54, 22)
                self.cell(95, 5, _safe(REPORT_LABEL))
                self.set_xy(self.w - MARGIN - 60, 10.5)
                self.set_font("helvetica", "", 9)
                self.cell(60, 6, _safe(time.strftime("%A %d %B %Y", time.localtime(report.created))),
                          align="R")
                self.set_draw_color(*INK)
                self.set_line_width(0.6)
                self.line(MARGIN, HEADER_H - 5, self.w - MARGIN, HEADER_H - 5)
                self.set_line_width(0.2)
                self.set_text_color(*INK)
                self.set_xy(MARGIN, HEADER_H)

            def footer(self):
                if self.page_no() == 1:
                    return
                self.set_fill_color(*BAND)
                self.rect(MARGIN, self.h - FOOTER_H, self.w - 2 * MARGIN - 16, 12, style="F")
                self.rect(self.w - MARGIN - 14, self.h - FOOTER_H, 14, 12, style="F")
                self.set_font("helvetica", "", 8)
                self.set_text_color(*GREY)
                self.set_xy(MARGIN, self.h - FOOTER_H + 3)
                self.cell(self.w - 2 * MARGIN - 16, 6, _safe(FOOTER_TEXT), align="C")
                self.set_xy(self.w - MARGIN - 14, self.h - FOOTER_H + 3)
                self.cell(14, 6, str(self.page_no()), align="C")
                self.set_text_color(*INK)

        return Document(unit="mm", format="A4")

    def _cover(self, pdf, test):
        pdf.add_page()
        pdf.set_fill_color(*BRAND)
        pdf.rect(0, 0, pdf.w, pdf.h, style="F")
        if LOGO_WHITE.exists():
            pdf.image(str(LOGO_WHITE), x=pdf.w - MARGIN - 48, y=MARGIN, w=48)
        pdf.set_text_color(255, 255, 255)
        pdf.set_xy(MARGIN, MARGIN + 2)
        pdf.set_font("helvetica", "", 15)
        pdf.cell(110, 8, _safe(COMPANY), new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(MARGIN)
        pdf.set_font("helvetica", "", 10)
        pdf.cell(110, 6, _safe(DEPARTMENT), new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(MARGIN, 108)
        pdf.set_font("helvetica", "B", 38)
        pdf.cell(0, 17, "AUTOMATION", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(MARGIN)
        pdf.cell(0, 17, "REPORT", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(MARGIN)
        pdf.set_font("helvetica", "", 12)
        pdf.cell(0, 8, "Testing summary report", new_x="LMARGIN", new_y="NEXT")
        pdf.ln(3)
        pdf.set_x(MARGIN)
        pdf.set_font("helvetica", "", 15)
        pdf.multi_cell(pdf.w - 2 * MARGIN, 9, _safe(f"Scenario : {self.title()}"),
                       new_x="LMARGIN", new_y="NEXT")

        if str(test["status"]).lower() == "failed" and test.get("error"):
            pdf.set_x(MARGIN)
            pdf.set_font("helvetica", "", 10)
            pdf.multi_cell(pdf.w - 2 * MARGIN, 5, _safe(f"Failure : {test['error']}"),
                           new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(MARGIN, pdf.h - 76)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(0, 7, "Reporting By", align="R", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(MARGIN)
        pdf.set_font("helvetica", "", 16)
        pdf.cell(0, 9, _safe(REPORTING_BY), align="R", new_x="LMARGIN", new_y="NEXT")

        pdf.set_xy(MARGIN, pdf.h - 46)
        pdf.set_font("helvetica", "", 11)
        pdf.cell(80, 6, "Tools :", new_x="LMARGIN", new_y="NEXT")
        pdf.set_x(MARGIN)
        pdf.set_font("helvetica", "", 16)
        pdf.cell(80, 9, _safe(TOOLS))
        pdf.set_font("helvetica", "", 10)
        pdf.set_xy(pdf.w - MARGIN - 80, pdf.h - 38)
        pdf.cell(80, 6, _safe(time.strftime("%A %d %B %Y", time.localtime(self.created))), align="R")
        pdf.set_text_color(*INK)

    def _toc(self, pdf, outline):
        entries = [(section.name, section.page_number) for section in outline]
        pdf.set_y(HEADER_H)
        pdf.set_font("helvetica", "", 20)
        pdf.set_text_color(*BRAND)
        pdf.cell(0, 12, "Table of Content", new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*BRAND)
        pdf.line(MARGIN, pdf.get_y(), MARGIN + 70, pdf.get_y())
        pdf.ln(6)
        pdf.set_text_color(*INK)
        pdf.set_font("helvetica", "", 11)
        width = pdf.w - 2 * MARGIN
        for index, (label, page) in enumerate(entries, start=1):
            if index > 1 and (index - 1) % TOC_PER_PAGE == 0:
                pdf.add_page()
                pdf.set_y(HEADER_H)
            link = pdf.add_link(page=page)
            top = pdf.get_y()
            pdf.set_x(MARGIN)
            pdf.cell(width - 14, 9, _safe(f"{index}. {label}"), link=link)
            pdf.cell(14, 9, str(page), align="R", link=link, new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*LINE)
            pdf.line(MARGIN, top + 9, pdf.w - MARGIN, top + 9)
            pdf.ln(1.5)

    def _section_title(self, pdf, text):
        pdf.set_font("helvetica", "", 13)
        pdf.set_text_color(*GREY)
        pdf.cell(0, 9, _safe(text), new_x="LMARGIN", new_y="NEXT")
        pdf.set_draw_color(*BRAND)
        pdf.line(MARGIN, pdf.get_y(), MARGIN + 70, pdf.get_y())
        pdf.set_text_color(*INK)
        pdf.ln(6)

    def _meta_row(self, pdf, left_label, left_value, right_label, right_value):
        half = (pdf.w - 2 * MARGIN) / 2
        pdf.set_font("helvetica", "", 9.5)
        pdf.cell(34, 6, _safe(left_label))
        pdf.cell(4, 6, ":")
        pdf.cell(half - 38, 6, _safe(left_value))
        pdf.cell(32, 6, _safe(right_label))
        pdf.cell(4, 6, ":")
        pdf.cell(half - 36, 6, _safe(right_value), new_x="LMARGIN", new_y="NEXT")

    def _summary(self, pdf, test):
        steps = [entry for entry in test["steps"] if entry.get("evidence")]
        started = test.get("started_at") or self.created
        duration = test.get("duration") or 0
        status = "FAILED" if str(test["status"]).lower() == "failed" else "PASSED"
        pdf.set_font("helvetica", "", 15)
        pdf.cell(34, 10, "Scenario")
        pdf.cell(4, 10, ":")
        pdf.multi_cell(0, 10, _safe(self.title()), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(2)
        self._meta_row(pdf, "Total Test Step", f"{len(steps)} / {len(steps)} Test Step",
                       "Aplication ID", settings.BUNDLE_ID or "-")
        self._meta_row(pdf, "Scenario Status", status, "Platform Name",
                       f"{settings.PLATFORM_NAME} - {settings.TARGET}")
        self._meta_row(pdf, "Execution Start", _clock(started), "Host Name", getpass.getuser())
        self._meta_row(pdf, "Execution End", _clock(started + duration),
                       "Execution Time", _elapsed(duration))
        pdf.ln(4)
        if status == "FAILED":
            self._failure(pdf, test, steps)
        pdf.ln(2)
        self._summary_table(pdf, steps)

    def _failure(self, pdf, test, steps):
        failed = next((entry for entry in reversed(steps) if entry.get("failed")), None)
        reason = test.get("error") or "No failure message was captured for this run"
        pdf.set_fill_color(253, 236, 236)
        pdf.set_draw_color(*FAIL_COLOR)
        top = pdf.get_y()
        pdf.set_font("helvetica", "B", 10)
        pdf.set_text_color(*FAIL_COLOR)
        pdf.cell(0, 7, "FAILURE REASON", new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.set_font("helvetica", "", 9)
        pdf.set_text_color(*INK)
        if failed:
            pdf.multi_cell(0, 5, _safe(f"Failed at step {steps.index(failed) + 1}: {failed['text']}"),
                           new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.multi_cell(0, 5, _safe(reason), new_x="LMARGIN", new_y="NEXT", fill=True)
        pdf.rect(MARGIN, top, pdf.w - 2 * MARGIN, pdf.get_y() - top)
        pdf.ln(2)

    def _table_head(self, pdf):
        pdf.set_fill_color(*BRAND_TINT)
        pdf.set_font("helvetica", "", 10)
        pdf.set_text_color(*INK)
        width = pdf.w - 2 * MARGIN
        pdf.cell(16, 10, "No", align="C", fill=True)
        pdf.cell(width - 46, 10, "Test Step", align="C", fill=True)
        pdf.cell(30, 10, "Status", align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

    def _summary_table(self, pdf, steps):
        width = pdf.w - 2 * MARGIN
        self._table_head(pdf)
        pdf.set_font("helvetica", "", 9.5)
        for index, entry in enumerate(steps, start=1):
            if pdf.get_y() + 9 > pdf.h - FOOTER_H - 6:
                pdf.add_page()
                self._table_head(pdf)
                pdf.set_font("helvetica", "", 9.5)
            status = _status_of(entry)
            top = pdf.get_y()
            pdf.set_text_color(*INK)
            pdf.cell(16, 9, str(index), align="C")
            pdf.cell(width - 46, 9, _safe(entry["text"])[:78])
            pdf.set_text_color(*(FAIL_COLOR if status == "FAILED" else PASS_COLOR))
            pdf.cell(30, 9, status, align="C", new_x="LMARGIN", new_y="NEXT")
            pdf.set_draw_color(*LINE)
            pdf.line(MARGIN, top + 9, pdf.w - MARGIN, top + 9)
        pdf.set_text_color(*INK)

    def _evidence(self, pdf, test):
        pdf.add_page()
        self._section_title(pdf, "TEST CASE EVIDENCE IMAGE")
        for index, entry in enumerate([e for e in test["steps"] if e.get("evidence")], start=1):
            self._evidence_block(pdf, entry, index)

    def _table_block(self, pdf, entry, index):
        rows = str(entry.get("table") or "").splitlines()
        shot = entry.get("screenshot")
        size = _image_size(shot) if shot and Path(shot).exists() else None
        image_h = image_w = 0
        if size:
            width, height = size
            image_h = min(TABLE_IMAGE_H, IMAGE_MAX_W * height / width)
            image_w = image_h * width / height
        if pdf.get_y() + image_h + len(rows) * 4.6 + 22 > pdf.h - FOOTER_H - 6:
            pdf.add_page()
        pdf.start_section(_safe(entry["text"]))
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(*INK)
        pdf.cell(0, 8, _safe(f"{index}. {entry['text']}"), new_x="LMARGIN", new_y="NEXT")
        if image_h:
            try:
                pdf.image(shot, x=(pdf.w - image_w) / 2, h=image_h)
            except Exception as exc:
                pdf.set_font("helvetica", "I", 8)
                pdf.multi_cell(0, 5, _safe(f"screenshot not embedded: {exc}"),
                               new_x="LMARGIN", new_y="NEXT")
            pdf.ln(3)
        pdf.set_font("courier", "", 8)
        for row in rows:
            pdf.set_text_color(*(FAIL_COLOR if row.endswith("FAIL") else INK))
            pdf.cell(0, 4.6, _safe(row), new_x="LMARGIN", new_y="NEXT")
        pdf.set_text_color(*INK)
        pdf.ln(6)

    def _evidence_block(self, pdf, entry, index):
        if entry.get("kind") == "table":
            return self._table_block(pdf, entry, index)
        shot = entry.get("screenshot")
        size = _image_size(shot) if shot and Path(shot).exists() else None
        image_h = image_w = 0
        if size:
            width, height = size
            image_h = min(IMAGE_MAX_H, IMAGE_MAX_W * height / width)
            image_w = image_h * width / height
        if pdf.get_y() + image_h + 22 > pdf.h - FOOTER_H - 6:
            pdf.add_page()
        pdf.start_section(_safe(entry["text"]))
        pdf.set_font("helvetica", "", 11)
        pdf.set_text_color(*INK)
        pdf.cell(0, 8, _safe(f"{index}. {entry['text']}"), new_x="LMARGIN", new_y="NEXT")
        if image_h:
            try:
                pdf.image(shot, x=(pdf.w - image_w) / 2, h=image_h)
            except Exception as exc:
                pdf.set_font("helvetica", "I", 8)
                pdf.multi_cell(0, 5, _safe(f"screenshot not embedded: {exc}"),
                               new_x="LMARGIN", new_y="NEXT")
        status = _status_of(entry)
        detail = entry["text"] if entry["value"] is None else f"{entry['text']} = {entry['value']}"
        pdf.ln(2)
        pdf.set_font("helvetica", "", 9.5)
        pdf.cell(14, 6, "Desc :")
        pdf.set_text_color(*(FAIL_COLOR if status == "FAILED" else PASS_COLOR))
        pdf.cell(20, 6, f"[{status}]")
        pdf.set_text_color(*INK)
        pdf.multi_cell(0, 6, _safe(detail), new_x="LMARGIN", new_y="NEXT")
        pdf.ln(6)

    def save(self, test, directory=None):
        try:
            from fpdf import FPDF  # noqa: F401
        except ImportError:
            log.warning("fpdf2 is not installed, pdf report skipped")
            return None
        folder = Path(directory) if directory else Path(settings.REPORT_DIR) / "pdf"
        folder.mkdir(parents=True, exist_ok=True)
        self.failed = str(test.get("status")).lower() == "failed"
        self.path = folder / f"{_slug(self.title())}.pdf"

        steps = [entry for entry in test["steps"] if entry.get("evidence")]
        test = dict(test, steps=steps)
        pdf = self._document()
        pdf.set_auto_page_break(auto=True, margin=FOOTER_H + 6)
        pdf.set_margins(MARGIN, HEADER_H, MARGIN)
        pdf.set_title(_safe(self.title()))
        self._cover(pdf, test)
        pdf.add_page()
        pdf.insert_toc_placeholder(self._toc,
                                   pages=max(1, math.ceil(len(steps) / TOC_PER_PAGE)))
        self._summary(pdf, test)
        self._evidence(pdf, test)
        pdf.output(str(self.path))
        log.info(f"pdf report saved {self.path}")
        return str(self.path)


def init_pdf(name, tc_id=None, screenshots=None):
    if not settings.PDF_REPORT:
        reporter.pdf = None
        reporter.force_screenshots = False
        reporter.note(f"pdf report disabled {tc_id or name}")
        return None
    report = PdfReport(name, tc_id)
    reporter.pdf = report
    reporter.force_screenshots = True if screenshots is None else bool(screenshots)
    reporter.note(f"pdf report {tc_id or name}")
    return report
