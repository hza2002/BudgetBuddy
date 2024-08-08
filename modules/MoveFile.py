# Move File
import os
import shutil
import tkinter
from tkinter import filedialog


class AddFile:
    """ 弹出窗口实现选择将文件复制到指定文件夹
    Attributes:
        file: 返回选中的文件地址
        folder: 返回选中的文件夹地址，如:/Users/ghot/Desktop/个人/

    Returns:
        addFile(): 弹出窗口选择文件
        toFolder(): 弹出窗口选择文件夹
        copyfile(): 弹出窗口选择文件和文件夹，实现复制操作
    """

    def add_file(self):
        # 生成窗口以选择文件
        choose_file = tkinter.Tk()
        choose_file.withdraw()  # 隐藏窗口
        filepath = filedialog.askopenfilename()  # 获得选择好的文件
        return filepath

    def to_folder(self):
        # 生成窗口以选择文件夹
        choose_dir = tkinter.Tk()
        choose_dir.withdraw()  # 隐藏窗口
        folderpath = filedialog.askdirectory() + "/"  # 获得选择好的文件夹
        return folderpath

    def copyfile(self, srcfile, dstpath):
        # 复制文件到指定目录
        # srcfile 需要复制、移动的文件
        # dstpath 目的地址
        fpath, fname = os.path.split(srcfile)  # 分离文件名和路径
        shutil.copy(srcfile, dstpath + fname)  # 复制文件
        print("copy %s -> %s" % (srcfile, dstpath + fname))


if __name__ == "__main__":
    new = AddFile()
