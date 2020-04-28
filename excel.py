import xlsxwriter


class Excel(object):
    def __init__(self, filename):
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()

        self.row = 0

    def write_title(self, columns):
        bold = self.workbook.add_format({'bold': True})
        self.write(data=columns, bold=bold)

    def write(self, data, bold=None):
        column = 0

        for column_data in data:
            self.worksheet.write(self.row, column, column_data, bold)
            column += 1

        self.row += 1

    def close(self):
        self.workbook.close()
