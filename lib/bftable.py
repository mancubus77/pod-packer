from beautifultable import BeautifulTable


class BTable:
    """
    BeautifulTable class to create and format tables
    """

    def __init__(self):
        self.table = BeautifulTable()
        self.table.set_style(BeautifulTable.STYLE_GRID)

    def create_heading(self, headings: list):
        self.table.columns.header = headings

    def append_row(self, row: list):
        self.table.rows.append(row)

    def is_headings(self):
        return False if len(self.table.columns.header) == 0 else True

    def __str__(self):
        return f"{self.table}"
