from openpyxl.styles import Font, colors, Alignment, Border, Side

from mark_excel.write import Write


class MarkExcel(object):
    def __init__(self, height=30, width=20, font=None, align=None, border=None):
        # height：单元格的高度
        self.height = height
        # width：单元格的宽度
        self.width = width
        # 字体设置
        self.font = font if font else Font(name='等线', size=11, italic=False, color=colors.BLACK, bold=False)
        # 是否居中显示
        self.align = align if align else Alignment(horizontal='center', vertical='center', wrap_text=True)
        # 边框设置
        self.border = border if border else Border(left=Side(border_style='thin', color='000000'),
                                                   right=Side(border_style='thin', color='000000'),
                                                   top=Side(border_style='thin', color='000000'),
                                                   bottom=Side(border_style='thin', color='000000'))

        self.LINE = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P", "Q", "R", "S",
                     "T", "U", "V", "W", "X", "Y", "Z"]
        self.write = Write(self)
