# Date Selection Column
import calendar
import datetime
import tkinter
import tkinter.ttk


class Choosedate:
    """定义类选择日期
    
    Attributes:
            labelframe: 包含 label 和 combobox
            label: 指示 combobox
            var: combobox 的变量，归属于全局窗口
            combobox: 选择框
    """

    def __init__(self, name, list, top):
        self.window = top
        self.labelframe = tkinter.LabelFrame(self.window, relief="flat")
        self.label = tkinter.Label(self.labelframe, relief="flat", text=name, font=("微软雅黑", 16))
        self.label.grid(row=0, column=0)
        self.var = tkinter.StringVar(self.window)
        self.combobox = tkinter.ttk.Combobox(
            self.labelframe, textvariable=self.var, state="readonly", value=list, width=4)
        self.combobox.grid(row=0, column=1)


class DateSelectionColumn:
    def __init__(self, top):
        self.window = top
        self.dateframe = tkinter.LabelFrame(self.window, relief="groove")
        self.dateframe.columnconfigure((0, 1, 2), weight=1)
        self.dateframe.grid(row=0, column=1, columnspan=2, sticky=tkinter.NSEW)

        # 选择年份
        self.chooseYear = Choosedate("年", [i for i in range(1980, 2030)], self.window)
        self.chooseYear.var.set(datetime.datetime.today().year)
        self.chooseYear.labelframe.grid(row=0, column=0)
        # 选择月份
        self.chooseMonth = Choosedate("月", [i + 1 for i in range(12)], self.window)
        self.chooseMonth.var.set(datetime.datetime.today().month)
        self.chooseMonth.labelframe.grid(row=0, column=1)
        # 选择日期
        self.chooseDay = Choosedate("日", [], self.window)
        self.chooseDay.var.set(datetime.datetime.today().day)
        self.chooseDay.labelframe.grid(row=0, column=2)

        # 更改年月时自动更新日期列表
        self.chooseYear.combobox.bind("<<ComboboxSelected>>", self.changeList)
        self.chooseMonth.combobox.bind("<<ComboboxSelected>>", self.changeList)

        self.changeList()  # 初始化日期列表

    def changeList(self, *args):
        """将 calendar 生成的某月二维列表转化为日期一维列表并赋值给日期列表"""
        list = []
        for i in calendar.monthcalendar(int(self.chooseYear.var.get()),
                                        int(self.chooseMonth.var.get())):
            for j in range(7):
                if i[j] != 0: list.append(i[j])
        self.chooseDay.combobox["value"] = list


if __name__ == "__main__":
    DateSelection = tkinter.Tk()
    DateSelection.title("Date Selection Column")
    ADateSelectionColumn = DateSelectionColumn(DateSelection)

    DateSelection.mainloop()
