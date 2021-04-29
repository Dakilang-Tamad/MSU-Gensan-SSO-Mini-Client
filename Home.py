import os
import tkinter as tk
from tkinter import*
from tkinter.ttk import*
import tkinter.messagebox
import urllib.request
import webbrowser
from selenium import webdriver
from time import *
import ctypes
from win10toast import ToastNotifier
from selenium.webdriver.chrome.options import Options


#function that opens a link to default browser
def open_url(url):
    link = url
    try:
        browser = webbrowser.get('chrome')
        browser.open_new(link)
    except:
        webbrowser.open_new(link)

#function that checks if a certain file exists in the directory
def check_file(file_name):
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file == file_name:
                return True
    return False


#function that checks the site connectivity
def connect(host='https://sso.msugensan.edu.ph'):
    tkinter.messagebox.showinfo("Loading...", "Please wait while trying to connect to host site.")
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False

#function that logins and scrapes data from the site
#currently bugged on conversion
def login(mail, word):
    try:
        
        popup = ToastNotifier()
        
        #raises notifications
        ctypes.windll.user32.MessageBoxW(0,"The login sequence will now start. Please wait until the main window changes.", "Warning", 0)
        ctypes.windll.user32.MessageBoxW(0,"A terminal window will appear for the login sequence. Please do not close that window until the sequence is over i.e. the main window changes screens or an error occurs.", "WARNING", 1)
        
        #sets options to run web driver as headless (no display)
        options = Options()
        options.add_argument("--headless")
        options.add_argument("--gpuless")
        
        #opens webdriver
        driver = webdriver.Chrome(executable_path='chromedriver.exe', options=options)
        driver.get('https://sso.msugensan.edu.ph')
        main_window = driver.current_window_handle
        
        #temporarily sleeps the program to wait for site load
        sleep(5) 

        popup.show_toast("Login process", "Opening host site", duration=3)
        
        #find site button by xml path then cick
        grade_button = driver.find_element_by_class_name('abcRioButtonContentWrapper')
        grade_button.click()

        sleep(5)
        
        #transfers handle to new popup login window
        for handle in driver.window_handles:
            if handle != main_window:
                login_page = handle

        driver.switch_to.window(login_page)

        popup.show_toast("Login process", "Entering email", duration=3)

        e_mail = mail
        
        #inputs email address then proceed
        try:
            email = driver.find_element_by_id('identifierId')
            email.send_keys(e_mail)
            next = driver.find_element_by_xpath('//div[@id="identifierNext"]')
            next.click()
        except:
            email = driver.find_element_by_id('Email')
            email.send_keys(e_mail)
            next = driver.find_element_by_xpath('//input[@id="next"]')
            next.click()

        sleep(5)

        popup.show_toast("Login process", "Entering password", duration=3)

        pass_word = word
        
        #inputs password the proceed
        try:
            password = driver.find_element_by_xpath('//input[@jsname="YPqjbf"]')
            password.send_keys(pass_word)
            next = driver.find_element_by_xpath('//div[@jsname="Njthtb"]')
            next.click()
        except:
            password = driver.find_element_by_id('password')
            password.send_keys(pass_word)
            next = driver.find_element_by_xpath('//input[@id="submit"]')
            next.click()

        sleep(10)
        
        #return handle back to main web window
        driver.switch_to.window(main_window)

        popup.show_toast("Scraping process", "Accessing grades", duration=3)

        sleep(10)
        
        #navigate to grades page
        grade_button = driver.find_element_by_xpath('//a[@id="view_grade"]')
        grade_button.click()

        sleep(5)

        popup.show_toast("Scraping process", "Scraping grades", duration=3)
        
        #locating different identifiers and data
        subcodes = driver.find_elements_by_xpath('//td[@data-label="Subject code"]')
        sections = driver.find_elements_by_xpath('//td[@data-label="Section"]')
        grades = driver.find_elements_by_xpath('//td[@data-label="Grade"]')
        descriptions = driver.find_elements_by_xpath('//td[@data-label="Description"]')
        subcodes2 = []
        sections2 = []
        grades2 = []
        descriptions2 = []
        
        #Store data to arrays
        for i in subcodes:
            subcodes2.append(i.text)
        for i in sections:
            sections2.append(i.text)
        for i in grades:
            grades2.append(i.text)
        for i in descriptions:
            descriptions2.append(i.text)
        
        #creates new files and stores the data
        sub_file = open("user_files\suject_codes.txt", "w")
        sec_file = open("user_files\section_codes.txt", "w")
        gr_file = open("user_files\grades.txt", "w")
        des = open("user_files\descriptions.txt", "w")

        for i in subcodes2:
            sub_file.writelines(i + "\n")
        for i in sections2:
            sec_file.writelines(i + "\n")
        for i in grades2:
            gr_file.writelines(i + "\n")
        for i in descriptions2:
            des.writelines(i + "\n")

        driver.close()

        return True

    except:
        return False


#master window
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


#startup window
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
                tkinter.messagebox.showwarning("Error", "Cannot login to Student Portal. This might be due to a connection problem or the site is currently unavailable.")
        else:
            MiniClient.switch_frame(master, S1)

class S1(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.BG = PhotoImage(file=r"resources\BG.png")
        self.BG = self.BG.zoom(1)
        self.bg = Label(master, image=self.BG)
        self.bg.place(x=0, y=0, relwidth=1, relheight=1)
        tkinter.messagebox.showinfo("Note", "Input data will not be permanently stored without user permission.")
        self.e_tag = tk.Entry(master)
        self.p_tag = tk.Entry(master, show="*")
        self.mail = Label(master, text="Email:", bg=None, justify=CENTER)
        self.word = Label(master, text="Password:", bg=None, justify=CENTER)
        self.e_tag.place(x=430, y=250)
        self.p_tag.place(x=430, y=300)
        self.mail.place(x=430, y=230)
        self.word.place(x=430, y=280)
        self.enter = Button(master, text="Log in", command=lambda: self.login_function(master))
        self.enter.place(x=453, y=330)

    def login_function(self, master):
        email = self.e_tag.get()
        password = self.p_tag.get()
        response = tkinter.messagebox.askyesno("Confirm", "Do you want to store your credentials for future auto login?")
        if response:
            file1 = open('user_files\login_data\email.txt', "w")
            file2 = open('user_files\login_data\password.txt', "w")
            file1.write(email)
            file2.write(password)
            tkinter.messagebox.showinfo("Alert", "Your credentials were stored at user_file\login_data of the local directory")
        if login(email, password):
            MiniClient.switch_frame(master, S2)
        else:
            tkinter.messagebox.showwarning("Error","Cannot login to Student Portal. This might be due to a connection problem or something else.")
            MiniClient.switch_frame(master, S0)



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

        self.buttons = []
        self.subCodes = []
        self.grades = []
        self.secs = []
        self.desc = []

        self.sub_file = open("user_files\suject_codes.txt","r")
        self.sec_file = open("user_files\section_codes.txt", "r")
        self.gr_file = open("user_files\grades.txt", "r")
        self.desc_file = open("user_files\descriptions.txt", "r")

        self.tst = self.sub_file.readline()
        while self.tst != '':
            self.subCodes.append(self.tst)
            self.grades.append(self.gr_file.readline())
            self.secs.append(self.sec_file.readline())
            self.desc.append(self.desc_file.readline())
            self.tst = self.sub_file.readline()

        self.max = len(self.subCodes)
        self.x = 0
        self.y = 15
        for i in range(self.max):
            self.button = Button(master, text = self.subCodes[i], command=lambda a=i: self.show_grade(a))
            self.check1 = i % 10
            if i == 0:
                self.x = 15
            else:
                self.x = self.x + 100
            if self.check1 == 0:
                self.x = 15
                self.y = self.y + 60
            self.button.place(x=self.x, y=self.y)
            self.buttons.append(self.button)

        self.menu = Button(master, text="Back to Main Menu", command=lambda: master.switch_frame(S2))
        self.menu.place(x=850, y=550, height=50, width=150)

    def show_grade(self, index):
        tkinter.messagebox.showinfo("Grade Summary",
                                    "Description: " + self.desc[index] +
                                    "\n Section: " + self.secs[index] +
                                    "\n Grade: " + self.grades[index])


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

