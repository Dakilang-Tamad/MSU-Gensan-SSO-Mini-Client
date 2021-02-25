from selenium import webdriver
from time import *
import ctypes
from selenium.webdriver.chrome.options import Options

def login(mail, word):
    try:

        ctypes.windll.user32.MessageBoxW(0,"The login sequence will now start. Please wait until the main window changes.", "Warning", 0)
        ctypes.windll.user32.MessageBoxW(0,"A terminal window will appear for the login sequence. Please do not clode that window until the sequence is over i.e. the main window changes screens.", "WARNING", 1)

        options = Options()
        options.add_argument("--headless")
        options.add_argument("--disable-gpu")

        driver = webdriver.Chrome('chromedriver.exe', options=options)
        driver.get('https://sso.msugensan.edu.ph')
        main_window = driver.current_window_handle


        grade_button = driver.find_element_by_class_name('abcRioButtonContentWrapper')
        grade_button.click()

        sleep(5)

        for handle in driver.window_handles:
            if handle != main_window:
                login_page = handle

        driver.switch_to.window(login_page)

        e_mail = mail

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

        pass_word = word

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

        driver.switch_to.window(main_window)

        sleep(10)

        grade_button = driver.find_element_by_xpath('//a[@id="view_grade"]')
        grade_button.click()

        sleep(5)

        subcodes = driver.find_elements_by_xpath('//td[@data-label="Subject code"]')
        sections = driver.find_elements_by_xpath('//td[@data-label="Section"]')
        grades = driver.find_elements_by_xpath('//td[@data-label="Grade"]')
        subcodes2 = []
        sections2 = []
        grades2 = []

        for i in subcodes:
            subcodes2.append(i.text)
        for i in sections:
            sections2.append(i.text)
        for i in grades:
            grades2.append(i.text)

        driver.close()

        sub_file = open("user_files\suject_codes.txt", "w")
        sec_file = open("user_files\section_codes.txt", "w")
        gr_file = open("user_files\grades.txt", "w")

        for i in subcodes2:
            sub_file.writelines(i + "\n")
        for i in sections2:
            sec_file.writelines(i + "\n")
        for i in grades2:
            gr_file.writelines(i + "\n")

        return True

    except:
        return False
