from pdb import line_prefix
from plistlib import UID
from pydoc import pager
from unittest.util import unorderable_list_difference
from numpy import uint
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os
#import pyautogui
PATH = "C:/Users/xu35k6jo6/Desktop/chromedriver.exe"
driver = webdriver.Chrome(PATH)
#搜尋
driver.get("https://cylis.lib.cycu.edu.tw/")

book_name = input('請輸入書名:')
anthor = input('需要搜尋作者嗎?(Y\\N):')
if anthor == 'Y':
    book_anthor = input('請輸入作者')
    book_search = driver.find_element(By.NAME,'searcharg')
    book_search.send_keys('t:('+ book_name +') and a:('+ book_anthor +')',Keys.ENTER)
else:
    book_search = driver.find_element(By.NAME,'searcharg')
    book_search.send_keys('t:('+ book_name +')',Keys.ENTER)
try:
    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="rightSideCont"]/table[1]/tbody/tr[1]/td/div/form/div[2]/input'))
    )
    mode = 1
    E_Books = input("需要限制為可外借藏館嗎?(Y\\N):")
    if E_Books == 'Y':
        e_books = driver.find_element(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[1]/td/div/form/div[2]/input')
        e_books.click()
        search_btn = driver.find_element(By.NAME,'SUBMIT')
        search_btn.click()
except:
    mode = 3
#查詢完成頁面跳轉後
#XXX:會卡5~10秒 非必要
try:
    WebDriverWait(driver, 5).until(#                  //*[@id="bibDisplayContent"]/div[1]/div/i[1]
            EC.presence_of_element_located((By.CLASS_NAME, 'bibSearchtoolMessage'))
        )
    result = driver.find_elements(By.CLASS_NAME,'bibSearchtoolMessage')
    for Result in result:
        print('共',Result.text + '依日期排序')
except:
    WebDriverWait(driver, 5).until(#                  //*[@id="bibDisplayContent"]/div[1]/div/i[1]
            EC.presence_of_element_located((By.CLASS_NAME, 'browseSearchtoolMessage'))
        )
    result = driver.find_elements(By.CLASS_NAME,'browseSearchtoolMessage')
    for Result in result:
        print('共',Result.text + '依日期排序')

    

#判斷讀者搜尋的書是否僅有一本 一本的話mode為1 兩本或以上mode為2
if mode!=3:
    try:
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bibInfoData"))
        )
        mode = 1

    except:
        mode = 2
# print('MODE=',mode)
#僅有一本
if mode == 1:
    line = 2
    booknameline = 1
    findbooknameline = True
    onlyonebook = driver.find_elements(By.XPATH,'//*[@id="bibDisplayLayout"]/tbody/tr/td[1]/table[1]/tbody/tr/td/table/tbody/tr['+ str(booknameline)+']/td[1]')
    for firstbook in onlyonebook:
        while(findbooknameline):
            onlyonebook = driver.find_elements(By.XPATH,'//*[@id="bibDisplayLayout"]/tbody/tr/td[1]/table[1]/tbody/tr/td/table/tbody/tr['+ str(booknameline)+']/td[1]')
            for Firstbook in onlyonebook:
                if Firstbook.text == '書名':
                    findbooknameline = False
                    onlyonebook = driver.find_elements(By.XPATH,'//*[@id="bibDisplayLayout"]/tbody/tr/td[1]/table[1]/tbody/tr/td/table/tbody/tr['+ str(booknameline)+']/td[2]')
                    for Firstbook in onlyonebook:
                        print('您搜尋的藏書只有一本')
                        print('書名:',Firstbook.text) 
                else:
                    print(booknameline)
                    booknameline +=1 

        library = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[1]')
        booknum = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[2]')
        booknumber = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[3]')
        stock = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[4]')
        for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
            havestock = 1
            print('館藏地:' + '[%-20s]' % Library.text + '，索書號:' + '[%-10s]' %Booknum.text + '，條碼:' + '[%-7s]' %Booknumber.text + '，架上情況:'+ '[%-10s]' %Stock.text + ',')
            havemore2 = 1
            while(havemore2 == 1):
                havemore2 = 0
                line+=1
                library = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[1]')
                booknum = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[2]')
                booknumber = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[3]')
                stock = driver.find_elements(By.XPATH,'//*[@id="bibDisplayContent"]/div[4]/table/tbody/tr/td/table[2]/tbody/tr['+ str(line)+']/td[4]')
                for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
                    havemore2 = 1
                    print('館藏地:' + '[%-20s]' % Library.text + '，索書號:' + '[%-10s]' %Booknum.text + '，條碼:' + '[%-7s]' %Booknumber.text + '，架上情況:'+ '[%-10s]' %Stock.text + ',')

#兩本或以上
elif mode == 2:
    DOIT = True
    num = 1
    while(DOIT):
        line = 3
        #藏書名稱
        book_stockname = driver.find_elements(By.CLASS_NAME,'briefcitTitle')
        #架上情況
        print("以下為圖書館藏書的前五十筆搜尋結果:")
        for Book_stockname in book_stockname:
            havestock = 0 #有藏書的話=1
            print('第' + str(num) , '個搜尋結果:' +Book_stockname.text + ':')
            num+=1
            library = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[1]')
            booknum = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[2]')
            booknumber = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[3]')
            stock = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[4]')
            for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
                havestock = 1
                if havestock == 1:
                    line2 = 2
                    havemore2 = 1
                    while(havemore2 == 1):
                        havemore2 = 0
                        library = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[1]')
                        booknum = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[2]')
                        booknumber = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[3]')
                        stock = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[3]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[4]')
                        for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
                            havemore2 = 1
                            print('館藏地:' + '[%-20s]' % Library.text + '，索書號:' + '[%-10s]' %Booknum.text + '，條碼:' + '[%-7s]' %Booknumber.text + '，架上情況:'+ '[%-10s]' %Stock.text + ',')
                        if havemore2 == 1:
                            line2 +=1

            if havestock == 0 :
                library = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[1]')
                booknum = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[2]')
                booknumber = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[3]')
                stock = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[2]/td[4]')
                for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
                    havestock = 1
                    if havestock == 1:
                        line2 = 2
                        havemore2 = 1
                        while(havemore2 == 1):
                            havemore2 = 0
                            library = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[1]')
                            booknum = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[2]')
                            booknumber = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[3]')
                            stock = driver.find_elements(By.XPATH,'//*[@id="rightSideCont"]/table[1]/tbody/tr[2]/td/table/tbody/tr[' + str(line) +']/td/table/tbody/tr/td[2]/div[2]/table/tbody/tr[' + str(line2) + ']/td[4]')
                            for Library,Booknum,Booknumber,Stock in zip(library,booknum,booknumber,stock):
                                havemore2 = 1
                                print('館藏地:' + '[%-20s]' % Library.text + '，索書號:' + '[%-10s]' %Booknum.text + '，條碼:' + '[%-7s]' %Booknumber.text + '，架上情況:'+ '[%-10s]' %Stock.text + ',')
                            if havemore2 == 1:
                                line2 +=1
                if havestock == 0:
                    print('這是電子書唷')
            line+=1

        if num %50 == 1 and num>=50:
            next = input("需要列出更多搜尋結果嗎?(Y\\N)")
            if next == 'Y':
                DOIT = True
                nextpage = driver.find_element(By.XPATH,'//*[@id="id_icon_paging_prev"]')
                nextpage.click()
            else: 
                DOIT = False
        else:
            DOIT = False
#找不到
else :
    print("抱歉><搜尋不到你想找的書")
print("謝謝使用唷!!")
driver.quit()