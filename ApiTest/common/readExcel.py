import xlrd
import uuid
'''
    思路:
        从左往右，一格一格读取单元格
        如果碰到某个单元格是合并单元格，则进行解析
        获取sheet页中所有的合并单元格坐标信息
        判断要读取的该单元格坐标，是否在合并单元格坐标内
        如果在，读取该合并单元格的值并返回
'''
class ReadExcel():

    # @classmethod
    def read_excel(self,filename):
        # 打开文件
        workbook = xlrd.open_workbook(file_contents=filename.read())
        # 获取所有sheet
        print('打印所有sheet:', workbook.sheet_names())

        sheet2 = workbook.sheet_by_index(0)  # sheet索引从0开始
        rows_num = sheet2.nrows
        cols_num = sheet2.ncols
        big_l = []
        for r in range(1,rows_num):
            small_l = []
            for c in range(cols_num):
                cell_value = sheet2.row_values(r)[c]
                # print('第%d行第%d列的值：[%s]' % (r, c, sheet2.row_values(r)[c]))
                if (cell_value is None or cell_value == ''):
                    cell_value = (self.get_merged_cells_value(sheet=sheet2, row_index=r, col_index=c))
                # 动态设置各属性值
                small_l.append(cell_value)
            big_l.append(small_l)
        return big_l


    def get_merged_cells(self, sheet):
        """
        获取所有的合并单元格，格式如下：
        [(4, 5, 2, 4), (5, 6, 2, 4), (1, 4, 3, 4)]
        (4, 5, 2, 4) 的含义为：行 从下标4开始，到下标5（不包含）  列 从下标2开始，到下标4（不包含），为合并单元格
        :param sheet:
        :return:
        """
        return sheet.merged_cells


    def get_merged_cells_value(self, sheet, row_index, col_index):
        """
        先判断给定的单元格，是否属于合并单元格；
        如果是合并单元格，就返回合并单元格的内容
        :return:
        """
        merged = self.get_merged_cells(sheet)
        for (rlow, rhigh, clow, chigh) in merged:
            if (row_index >= rlow and row_index < rhigh):
                if (col_index >= clow and col_index < chigh):
                    cell_value = sheet.cell_value(rlow, clow)
                    # print('该单元格[%d,%d]属于合并单元格，值为[%s]' % (row_index, col_index, cell_value))
                    return cell_value
                    break
        return None


    def getUUID(self):
        return uuid.uuid1().hex

