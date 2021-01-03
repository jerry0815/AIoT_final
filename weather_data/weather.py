from selenium import webdriver
from selenium.webdriver.support.ui import Select
import time 
import os
import shutil

def getLatestFilename():
    downloadPath = 'C:/Users/Jerry/Downloads/'
    try:
        filename = max([f for f in os.listdir(downloadPath)], key=lambda  x:os.path.getmtime(os.path.join(downloadPath, x)))
    except:
        filename = max([f for f in os.listdir(downloadPath)], key=lambda  x:os.path.getmtime(os.path.join(downloadPath, x))) #因為避免在執行這行程式時，中間突然又在下載好了一個CSV檔時會出現錯誤，所以再執行一次
    return filename

def changName(fileName):
    while True:
        name = getLatestFilename()
        if name.endswith('.csv'):
            print(name)
            break
    downloadPath = 'C:/Users/Jerry/Downloads/'
    newPath = 'D:/jerry/台科/綠能/weather_data/'
    shutil.move('{0}{1}'.format(downloadPath, name), '{0}{1}'.format(newPath, fileName))        

day = [31,29,31,30,31,30,31,31,30,31,30,31]
if __name__ == "__main__":
    browser = webdriver.Chrome('chromedriver.exe')
    browser.get("https://e-service.cwb.gov.tw/HistoryDataQuery/index.jsp")
    while True:
        try:
            browser.find_element_by_id('Button_North').click()
            break
        except:
            pass
    time.sleep(1.5)
    
    for m in range(1,13):
        d = day[m-1]
        if d < 10:
            d1 = "0" + str(d)
        else:
            d1 = str(d) 
        if m < 10:
            m1 = "0" + str(m)
        else:
            m1 = str(m)
        time.sleep(0.5)
        for item in Select(browser.find_element_by_id('stationCounty')).options:
            # print(item.text)
            if item.text.find('新竹縣') != -1:
                Select(browser.find_element_by_id('stationCounty')).select_by_visible_text(item.text)
                break
        for item in Select(browser.find_element_by_id('station')).options:
            # print(item.text)
            if item.text.find('新竹') != -1:
                Select(browser.find_element_by_id('station')).select_by_visible_text(item.text)
                print('2020-' + m1 + "-" + d1)
                browser.find_element_by_id('datepicker').clear()
                browser.find_element_by_id('datepicker').send_keys('2020-' + m1 + "-" + d1)
                browser.find_element_by_id('doquery').click()

                windows = browser.window_handles
                browser.switch_to_window(windows[-1])
                browser.find_element_by_xpath("//input[@src='images/downloadCSV_2.png']").click()
                browser.close()

                time.sleep(0.5)
                browser.switch_to_window(windows[0])

                changName("2020-" + m1 + "-" + d1 + ".csv")
                break
    browser.quit()