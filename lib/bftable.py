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


# ]
# for node in node_list.node_list:
#     table.append_row(
#         [
#             node.app,
#             len(node.pods),
#             node.cpu_used,
#             (node.cpu_used / node.cpu_total) * 100,
#             node.mem_used,
#             (node.mem_used / node.mem_total) * 100,
#         ]
#     )
# print(table)
