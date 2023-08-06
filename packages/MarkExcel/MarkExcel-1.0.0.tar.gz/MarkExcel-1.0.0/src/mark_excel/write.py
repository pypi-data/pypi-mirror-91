class Write(object):
    def __init__(self, mark_excel):
        self.mark_excel = mark_excel

    def merge_one_row(self, sheet, row_index, value, length):
        """
        合并写入一行
        :param sheet:要写入的sheet
        :param row_index:要写入第几行，从1开始计数
        :param value:写入的值
        :param length:合并单元格数量
        :return:
        """
        # 合并一行中的几个单元格
        sheet.merge_cells('A{}:{}{}'.format(row_index, self.mark_excel.LINE[length - 1], row_index))
        sheet.cell(row_index, 1).value = value
        sheet.row_dimensions[row_index].height = self.mark_excel.height
        sheet['A{}'.format(row_index)].alignment = self.mark_excel.align

    def one_row(self, sheet, row_index, alist):
        """
        正常情况下 写入一行数据
        :param sheet: 要写入的sheet
        :param row_index: 要写入第几行，从1开始计数
        :param alist: 要写入的数组
        :return:
        """
        # 首先设置一下这一行的高度
        sheet.row_dimensions[row_index].height = self.mark_excel.height
        for i, x in enumerate(alist):
            # 将数据写入指定单元格
            sheet.cell(row_index, i + 1).value = x
            # 设置该列的宽度
            sheet.column_dimensions[self.mark_excel.LINE[i]].width = self.mark_excel.width
            # 设置该列的对齐方式
            sheet['{}{}'.format(self.mark_excel.LINE[i], row_index)].alignment = self.mark_excel.align
