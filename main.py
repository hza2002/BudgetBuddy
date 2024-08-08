# Budget Buddy
# 记账数据保存在 data.csv
# 格式为：日期，金额，收/支，交易对象，备注
import os
import tkinter
import tkinter.ttk

from modules import MoveFile, Listwithbar, DrawMatplotlib, DateSelectionColumn


def process_data():  # data 账目以时间顺序重新排序，日期近的在上
    f = open("./data/data.csv", mode="r", encoding="UTF-8")
    templist = []
    for line in f:
        templist.append(line.replace("\n", ""))
    f.close()
    templist.sort()
    f = open("./data/data.csv", mode="w+", encoding="UTF-8")
    for i in templist:
        f.write(i + "\n")
    f.close()


def show_in_list(*args):  # 将所选日期区间的所有账目显示在列表中
    process_data()
    f = open("./data/data.csv", mode="r", encoding="UTF-8")
    start = startDate.chooseYear.var.get(
    ) + "-" + startDate.chooseMonth.var.get(
    ) + "-" + startDate.chooseDay.var.get() + " 00:00:00"
    end = endDate.chooseYear.var.get() + "-" + endDate.chooseMonth.var.get(
    ) + "-" + endDate.chooseDay.var.get() + " 00:00:00"
    list = []
    for i in f:
        temp = i.replace("\n", "").split(",")
        if start <= temp[0] <= end:
            list.append(i.replace(",", "  "))
    listbox.new_list(list)


def statement(*args):  # 绘制损益表
    process_data()
    f = open("./data/data.csv", mode="r", encoding="UTF-8")
    start = startDate.chooseYear.var.get() + "-" + (
        startDate.chooseMonth.var.get()).rjust(2, "0") + "-" + (
                startDate.chooseDay.var.get()).rjust(2, "0") + " 00:00:00"
    end = endDate.chooseYear.var.get() + "-" + (
        endDate.chooseMonth.var.get()).rjust(2, "0") + "-" + (
              endDate.chooseDay.var.get()).rjust(2, "0") + " 00:00:00"
    list = []
    cost = income = 0
    for i in f:
        temp = i.replace("\n", "").split(",")
        if start <= temp[0] <= end:
            list.append(i.replace(",", "  "))
            if temp[2] == "支出":
                cost += float(temp[1])
            elif temp[2] == "收入":
                income += float(temp[1])
    listbox.new_list(list)
    f.close()
    chart.x = ["Income", "Expenditure"]
    chart.y = [income, cost]
    chart.bar_chart()


def balance(*args):  # 绘制资产负债表
    process_data()
    f = open("./data/data.csv", mode="r", encoding="UTF-8")
    start = startDate.chooseYear.var.get() + "-" + (
        startDate.chooseMonth.var.get()).rjust(2, "0") + "-" + (
                startDate.chooseDay.var.get()).rjust(2, "0") + " 00:00:00"
    end = endDate.chooseYear.var.get() + "-" + (
        endDate.chooseMonth.var.get()).rjust(2, "0") + "-" + (
              endDate.chooseDay.var.get()).rjust(2, "0") + " 00:00:00"
    list = []
    listy = []
    cost = income = 0
    for i in f:
        temp = i.replace("\n", "").split(",")
        if start <= temp[0] <= end:
            list.append(i.replace(",", "  "))
            if temp[2] == "支出":
                cost += float(temp[1])
            elif temp[2] == "收入":
                income += float(temp[1])
            listy.append(income - cost)
    listbox.new_list(list)
    f.close()
    chart.x = [str(i[5:10]) for i in list]
    chart.y = listy
    chart.line_chart()


def add_we_chat(*args):  # 添加微信账本
    window = MoveFile.AddFile()
    filepath, filename = os.path.split(window.add_file())
    if filepath and filename:
        window.copyfile(filepath + "/" + filename, "./data/backups/WeChat/")
        f = open("./data/backups/WeChat/" + filename, mode="r", encoding="UTF-8")
        ls = []
        row = 0
        for line in f:
            if row <= 17:
                row += 1
            else:
                line = line.replace("\n", "")
                ls.append(line.split(","))
        f.close()
        date = open("./data/data.csv", mode="a", encoding="UTF-8")
        for line in ls:
            string = line[0] + "," + (line[5]).replace(
                "¥", "") + "," + line[4] + "," + line[2] + "," + line[3] + "\n"
        date.write(string)
        process_data()


def add_alipay(*args):  # 添加支付宝账本
    window = MoveFile.AddFile()
    filepath, filename = os.path.split(window.add_file())
    print(filepath)
    print(filename)
    if filepath and filename:
        window.copyfile(filepath + "/" + filename, "./data/backups/Alipay/")
        f = open("./data/backups/Alipay/" + filename, mode="r", encoding="gbk")
        ls = []
        row = 0
        for line in f:
            if row <= 2:
                row += 1
            else:
                line = line.replace("\n", "")
                templist = line.split(",")
                if templist[0][0] == "-":
                    break
                if templist[0][0] == "其" or templist[6] == "交易关闭":
                    continue
                else:
                    ls.append(templist)
        f.close()
        data = open("./data/data.csv", mode="a", encoding="UTF-8")
        for line in ls:
            string = line[10].rstrip() + "," + line[5].replace(
                " ", "") + "," + line[0].replace(" ", "") + "," + line[1].replace(
                " ", "") + "," + line[3].replace(" ", "") + "\n"
            data.write(string)
        process_data()


def add_item():  # 添加某条记账
    class Addaccountbook(tkinter.Toplevel):  # 增加账本弹窗
        def __init__(self):
            super().__init__()  # 重点
            self.title('添加账本')
            self.setupUI()

        def setupUI(self):
            # 整体框架
            window = tkinter.Frame(self)
            window.grid(row=0)

            dateframe = tkinter.LabelFrame(window, relief="groove")
            dateframe.grid(row=1, column=0, columnspan=2, sticky=tkinter.NSEW)

            # 时间选择栏
            date_selection_column = DateSelectionColumn.DateSelectionColumn(
                dateframe)
            self.year = date_selection_column.chooseYear.var.get()
            self.month = date_selection_column.chooseMonth.var.get()
            self.day = date_selection_column.chooseDay.var.get()

            # 选择收/支
            self.kind = tkinter.StringVar()
            self.kind.set("支出")
            kindlabel = tkinter.Label(window, relief="flat", text='选择收/支:')
            kindlabel.grid(row=2, column=0)
            entermoney = tkinter.ttk.Combobox(window, textvariable=self.kind, state="readonly", value=["支出", "收入"])
            entermoney.grid(row=2, column=1)

            # 输入金额
            self.addmoney = tkinter.StringVar()
            moneylabel = tkinter.Label(window, relief="flat", text='请输入金额:')
            moneylabel.grid(row=3, column=0)
            entermoney = tkinter.Entry(window, bd=5, textvariable=self.addmoney, borderwidth=1)
            entermoney.grid(row=3, column=1)

            # 输入交易对象
            self.addstore = tkinter.StringVar()
            storelabel = tkinter.Label(window, relief="flat", text='请输入交易对象:')
            storelabel.grid(row=4, column=0)
            enterstore = tkinter.Entry(window, bd=5, textvariable=self.addstore, borderwidth=1)
            enterstore.grid(row=4, column=1)

            # 输入备注
            self.addremark = tkinter.StringVar()
            remarklabel = tkinter.Label(window, relief="flat", text='请输入备注:')
            remarklabel.grid(row=5, column=0)
            enterremark = tkinter.Entry(window, bd=5, textvariable=self.addremark, borderwidth=1)
            enterremark.grid(row=5, column=1)

            # 确定按钮
            completebtn = tkinter.Button(self, text='确定', command=self.on_click)
            completebtn.grid(row=6, column=0, columnspan=2)

        def on_click(self):  # 确定按钮函数功能
            f = open("./data/data.csv", mode="a", encoding="UTF-8")
            date = self.year + "-" + self.month + "-" + self.day + " 00:00:00" + ","
            money = self.addmoney.get() + "," + self.kind.get() + "," + self.addstore.get() + "," + '"' + self.addremark.get() + '"'
            f.write(date + money + "\n")
            f.close()
            process_data()
            self.quit()
            self.destroy()

    var_box = tkinter.messagebox.askyesno(title='系统提示', message='是否需要新增账目')  # 返回'True','False'
    if var_box:
        app = Addaccountbook()
        app.mainloop()


# 创建窗口
root = tkinter.Tk()
root.title('Budget Buddy')  # 定义窗口名
root.resizable(False, False)  # 设置窗体不可放缩
root.iconphoto(False, tkinter.PhotoImage(file='assets/icon.png'))  # 窗体图标

# 设置窗口初始位置在屏幕居中
winWidth, winHeight = 1080, 720  # 设置窗口大小
x = int((root.winfo_screenwidth() - winWidth) / 2)
y = int((root.winfo_screenheight() - winHeight) / 2)
root.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

# 顶部说明栏
textLabel = tkinter.Label(root, text="账 目 资 金 管 理 系 统", bg="black", fg="white", font=("微软雅黑", 40))
textLabel.grid(row=0, column=0, columnspan=3, sticky=tkinter.NSEW)

# 功能区
functionFrame = tkinter.LabelFrame(root, text="功能区", labelanchor="n", font=("微软雅黑", 20))
functionFrame.grid(row=1, column=0, sticky=tkinter.NSEW)
functionFrame.rowconfigure((0, 1, 2, 3), weight=1)

# 生成报表按钮
buttonFrame = tkinter.LabelFrame(functionFrame, text="生成报表", labelanchor="n")
buttonFrame.grid(row=1, column=0, sticky=tkinter.EW)
buttonFrame.columnconfigure((0, 1, 2), weight=1)

balanceSheet = tkinter.Button(buttonFrame, text=" 资产负债表 ", command=balance)
balanceSheet.grid(row=0, column=1, sticky=tkinter.NS)
statementSheet = tkinter.Button(buttonFrame, text="损益表", command=statement)
statementSheet.grid(row=1, column=1, sticky=tkinter.NS)

# 增加账目按钮
BookFrame = tkinter.LabelFrame(functionFrame, text="增加账目", labelanchor="n")
BookFrame.grid(row=2, column=0, sticky=tkinter.EW)
BookFrame.columnconfigure((0, 1, 2), weight=1)

addOne = tkinter.Button(BookFrame, text="记一笔账", command=add_item)
addOne.grid(row=0, column=1, sticky=tkinter.NSEW)
addWeChatBook = tkinter.Button(BookFrame, text="导入微信账单", command=add_we_chat)
addWeChatBook.grid(row=1, column=1, sticky=tkinter.NSEW)
addAlipayBook = tkinter.Button(BookFrame, text="导入支付宝账单", command=add_alipay)
addAlipayBook.grid(row=2, column=1, sticky=tkinter.NSEW)

# 日期选择栏
dateFrame = tkinter.LabelFrame(functionFrame, relief="groove", text="日期选择栏", labelanchor="n",
                               font=("微软雅黑", 17))
dateFrame.grid(row=0, column=0)
dateFrame.columnconfigure((0, 1, 2, 3), weight=1)
startframe = tkinter.LabelFrame(dateFrame, relief="groove", text="开始日期", labelanchor="n")
startframe.grid(row=0, column=0, sticky=tkinter.NS)
startDate = DateSelectionColumn.DateSelectionColumn(startframe)

endframe = tkinter.LabelFrame(dateFrame, relief="groove", text="结束日期", labelanchor="n")
endframe.grid(row=1, column=0, sticky=tkinter.NS)
endDate = DateSelectionColumn.DateSelectionColumn(endframe)

# 数据图像画布
canvasframe = tkinter.LabelFrame(root, relief="groove", text="资产报表", labelanchor="n", font=("微软雅黑", 20))
canvasframe.grid(row=1, column=1, sticky=tkinter.NSEW)
canvas = tkinter.Canvas(master=canvasframe, relief="groove", bg="white")
canvas.grid(row=0, column=0, sticky=tkinter.NSEW)
chart = DrawMatplotlib.Draw(canvas)  # 创建画图对象

# 具体账目列表
listbox = Listwithbar.Listwithbar(root, title="所选时间区间具体账目表")
listbox.window.grid(row=2, column=0, columnspan=2, sticky=tkinter.NSEW)

root.mainloop()
