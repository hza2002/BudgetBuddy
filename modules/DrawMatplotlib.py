# DrawMatplotlib
import tkinter

import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

matplotlib.use('TkAgg')


class Draw:
    """使用 matplotlib 在 tkinter 画布上制图
    """

    def __init__(self, root, x=[], y=[]):
        self.x = x
        self.y = y
        # self.button["command"] = self.LineChart
        # self.button["command"] = self.BarChart
        self.f = Figure(figsize=(11, 6), dpi=75)  # figsize定义图像大小，dpi定义像素
        self.f_plot = self.f.add_subplot(111)  # 定义画布中的位置
        self.canvs = FigureCanvasTkAgg(self.f, root)  # f是定义的图像，root是tkinter中画布的定义位置
        self.canvs.get_tk_widget().grid(row=0, column=0)

    def line_chart(self):  # 折线图
        self.f_plot.clear()
        self.f_plot.plot(self.x, self.y)
        self.canvs.draw()

    def bar_chart(self):  # 柱状图
        self.f_plot.clear()
        self.f_plot.bar(self.x, self.y)
        self.canvs.draw()


if __name__ == "__main__":
    root = tkinter.Tk()
    button = tkinter.Button(root, text="test")
    button.grid(row=1, column=0, sticky=tkinter.NS)
    a = Draw(root, x=[1, 2, 3, 4], y=[6, 7, 8, 9])
    button["command"] = a.bar_chart
    a.bar_chart()
    root.mainloop()
