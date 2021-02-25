import os
import tkinter as tk
from tkinter import*
from tkinter.ttk import*
import tkinter.messagebox
import urllib.request
import webbrowser
from login_and_scrape import login


def open_url(url):
    link = url
    try:
        browser = webbrowser.get('chrome')
        browser.open_new(link)
    except:
        webbrowser.open_new(link)

def check_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == file_name:
                return True
    return False


def connect(host='https://sso.msugensan.edu.ph'):
    tkinter.messagebox.showinfo("Loading...", "Please wait while trying to connect to host site.")
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

class MiniClient(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self._frame = None
        self.switch_frame(S0)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()


class S0(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.MSU = PhotoImage(file=r"resources\MSU_logo.png")
        self.logo = self.MSU.subsample(2, 2)

        self.BG = PhotoImage(file=r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master, image=self.BG)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)

        self.label2 = Label(master, text="Logo", bg=None, image=self.logo, justify=CENTER)
        self.label2.place(x=340, y=100)

        self.label = Label(master, text="Log in with Google:", bg=None, justify=CENTER)
        self.label.place(x=400 ,y=475)

        self.photo = PhotoImage(file=r"resources\gg_logo.png")
        self.image = self.photo.subsample(2, 2)

        self.login_button = Button(master, text="Log in with Google", width=50, image=self.image, command=lambda: self.login(master) if connect() else self.login_error())
        self.login_button.place(x=400, y=500)


    def login_error(self):
            tkinter.messagebox.showinfo("Warning", "Cannot connect to host site. Please check your internet connection and try again.")

    def login(self,master):
        if check_file("email.txt"):
            file1 = open("user_files\login_data\email.txt")
            file2 = open("user_files\login_data\password.txt")
            email = file1.readline()
            password = file2.readline()
            if login(email, password):
                MiniClient.switch_frame(master,S2)
            else:
                tkinter.messagebox.showinfo("Error", "Cannot login to Student Portal. This might be due to a connection problem or something else.")

class S1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file=r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master, image=self.BG)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)


class S2(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file = r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master,image = self.BG)
        self.bg.place(x=0,y=0,relwidth = 1, relheight = 1)

        self.grades = Button(master, text="GRADES",command=lambda: master.switch_frame(S3))
        self.grades.place(x=250, y=15, height=125, width=500)

        self.inc = Button(master, text="INC Grade Monitor", command=lambda: master.switch_frame(S4))
        self.inc.place(x=250, y=160, height=125, width=500)

        self.cor = Button(master, text="Certificate of Registration", command=lambda: master.switch_frame(S5))
        self.cor.place(x=250, y=310, height=125, width=500)

        self.links = Button(master, text="Other Links", command=lambda: master.switch_frame(S6))
        self.links.place(x=250, y=460, height=125, width=500)


class S3(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file = r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master,image = self.BG)
        self.bg.place(x=0,y=0,relwidth = 1, relheight = 1)

        self.menu = Button(master, text="Back to Main Menu", command=lambda: master.switch_frame(S2))
        self.menu.place(x=850, y=550, height=50, width=150)


class S4(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file = r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master,image = self.BG)
        self.bg.place(x=0,y=0,relwidth = 1, relheight = 1)

        self.menu = Button(master, text="Back to Main Menu", command=lambda: master.switch_frame(S2))
        self.menu.place(x=850, y=550, height=50, width=150)

class S5(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file = r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master,image = self.BG)
        self.bg.place(x=0,y=0,relwidth = 1, relheight = 1)

        self.menu = Button(master, text="Back to Main Menu", command=lambda: master.switch_frame(S2))
        self.menu.place(x=850, y=550, height=50, width=150)

class S6(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file = r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master,image = self.BG)
        self.bg.place(x=0,y=0,relwidth = 1, relheight = 1)

        self.menu = Button(master, text="Back to Main Menu", command=lambda: master.switch_frame(S2))
        self.menu.place(x=850, y=550, height=50, width=150)

        self.vle = Button(master, text="Virtual Learning Environment", command=lambda: open_url("vle.msugensan.edu.ph"))
        self.vle.place(x=250, y=15, height=125, width=500)

        self.elib = Button(master, text="E-Library", command=lambda: open_url("http://msulib.msugensan.edu.ph"))
        self.elib.place(x=250, y=160, height=125, width=500)

        self.git = Button(master, text="Github Repository", command=lambda: open_url("https://github.com/Dakilang-Tamad/MSU-Gensan-SSO-Mini-Client"))
        self.git.place(x=250, y=310, height=125, width=500)


if __name__ == "__main__":
    app = MiniClient()
    app.title("MSU Student Portal Mini Client")
    app.geometry("1000x600")
    app.resizable(False, False)
    icon = PhotoImage(file=r"resources\MSU_logo.png")
    app.iconphoto(False, icon)
    app.mainloop()

