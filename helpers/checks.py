from helpers import amounts
from helpers.logger import get_logger
from helpers.reporter import reporter

log = get_logger("verify")

HEADERS = ("FIELD", "EXPECTED", "FOUND", "RESULT")
WIDTH = 46


def _cell(value):
    text = " ".join(str("" if value is None else value).split())
    return text if len(text) <= WIDTH else text[: WIDTH - 1] + "…"


class CheckTable:
    def __init__(self, title):
        self.title = title
        self.rows = []

    def add(self, field, expected, found, passed):
        self.rows.append((_cell(field), _cell(expected), _cell(found), bool(passed)))
        return passed

    def equal(self, field, expected, found):
        return self.add(field, expected, found, str(expected).strip() == str(found).strip())

    def contains(self, field, expected, found):
        return self.add(field, expected, found, str(expected).strip().casefold() in str(found or "").casefold())

    def amount(self, field, expected, found):
        return self.add(field, expected, found,
                        abs(amounts.to_number(expected)) == abs(amounts.to_number(found)))

    def truthy(self, field, found):
        return self.add(field, "any value", found, bool(str(found or "").strip()))

    def failures(self):
        return [row for row in self.rows if not row[3]]

    def text(self, rows=None, title=True):
        rows = self.rows if rows is None else rows
        widths = [max(len(HEADERS[index]), *(len(row[index]) for row in rows)) if rows
                  else len(HEADERS[index]) for index in range(3)]
        line = "  ".join(header.ljust(width) for header, width in zip(HEADERS, widths)) + "  RESULT"
        out = ([self.title] if title else []) + [line, "-" * len(line)]
        for field, expected, found, passed in rows:
            cells = (field.ljust(widths[0]), expected.ljust(widths[1]), found.ljust(widths[2]))
            out.append("  ".join(cells) + ("  PASS" if passed else "  FAIL"))
        return "\n".join(out)

    def report(self):
        for line in self.text().splitlines():
            log.info(line)
        reporter.table(self.title, self.text(title=False))
        return self

    def verify(self):
        self.report()
        failed = self.failures()
        assert not failed, f"{self.title} does not match\n{self.text(failed, title=False)}"
        return self
