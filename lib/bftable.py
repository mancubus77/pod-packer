from beautifultable import BeautifulTable


class BTable:
    def __init__(self):
        self.table = BeautifulTable()

    def create_heading(self, headings: list):
        self.table.column_headers = headings

    def append_row(self, row: list):
        self.table.append_row(row)

    def is_headings(self):
        return False if len(self.table.column_headers) == 0 else True

    def __str__(self):
        return f"{self.table}"
