# List With Bar
import tkinter


class Listwithbar:
    """ 生成一个带垂直滚动条的列表框
    
    Attributes:
        top: 所属对象
        list: 初始化列表
        title: 标题
        newList(): 更新 listbox 的项目，函数传入 list 参数
    """

    def __init__(self, top, list=[], title=""):
        self.window = tkinter.LabelFrame(top, text=title, labelanchor="n", font=("微软雅黑", 20))
        self.window.columnconfigure((0, 3), weight=1)
        self.__lb = tkinter.Listbox(self.window, width=115, height=9)
        self.__scr = tkinter.Scrollbar(self.window)
        self.__lb.config(yscrollcommand=self.__scr.set)
        self.__scr.config(command=self.__lb.yview)

        for i in list:
            self.__lb.insert(tkinter.END, "第%s项" % i)

        self.__lb.grid(row=0, column=1, sticky=tkinter.EW)
        self.__scr.grid(row=0, column=2, sticky=tkinter.N + tkinter.S + tkinter.E)

    def new_list(self, list):
        self.__lb.delete(0, "end")
        for item in list:
            self.__lb.insert("end", item)  # 插入新的项目


if __name__ == "__main__":
    app = tkinter.Tk()
    newTk = Listwithbar(app, [i for i in range(20)], title="text")
    newTk.new_list([i for i in range(50)])
    newTk.window.grid()
    app.mainloop()
