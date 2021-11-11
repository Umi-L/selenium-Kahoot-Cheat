import urllib.request as ur
import json
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def ElementExists(xpath):
    try:
        driver.find_element_by_xpath(xpath)
    except (NoSuchElementException,StaleElementReferenceException):
        return False
    return True


PATH = "C:\Program Files (x86)\chromedriver.exe"

gameid = input("Enter game id: ")
gKey = input("Enter game pin: ")
nName = input("Enter nick-name: ")

url = "https://play.kahoot.it/rest/kahoots/" + gameid
q = json.loads(ur.urlopen(url).read())["questions"]
colours_list = ["red", "blue", "yellow", "green"]

driver = webdriver.Chrome(PATH)
driver.get('https://kahoot.it/v2/')

aList = []

for index, slide in enumerate(q):
    if slide.get("type") == "quiz":
        for i in range(len(slide.get("choices"))):
            if slide["choices"][i]["correct"] == True:
                print("Question number: {}\n{}\n{}\n".format(
                    index + 1, slide["choices"][i].get("answer"), colours_list[i]))
                aList.append(colours_list[i])
    else:
        aList.append(-1)

gKeyBox = driver.find_element_by_xpath('//*[@id="game-input"]')
gKeyBox.send_keys(gKey)

next = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[3]/div[2]/main/div/form/button')
next.click()

time.sleep(1)

nNameBox = driver.find_element_by_xpath('//*[@id="nickname"]')
nNameBox.send_keys(nName)

next = driver.find_element_by_xpath('//*[@id="root"]/div[1]/div/div[3]/div[2]/main/div/form/button')
next.click()

while True:
    time.sleep(0.2)
    if ElementExists('//*[@id="root"]/div[1]/main/div[1]/div/div[1]'):
        try:
            qNum = int(driver.find_element_by_xpath('//*[@id="root"]/div[1]/main/div[1]/div/div[1]').text.split(" of")[0])
            #print(aList[qNum-1])
            if ElementExists('//*[@id="root"]/div[1]/main/div[3]/div[1]/span'):
                outputText = driver.find_element_by_xpath('//*[@id="root"]/div[1]/main/div[3]/div[1]/span')
                driver.execute_script("arguments[0].innerText = '"+aList[qNum-1]+"'", outputText)


        except (ValueError,StaleElementReferenceException) as ex:
            if ElementExists('//*[@id="root"]/div[1]/main/div[3]/div[1]/span'):
                outputText = driver.find_element_by_xpath('//*[@id="root"]/div[1]/main/div[3]/div[1]/span')
                driver.execute_script("arguments[0].innerText = 'N/A'", outputText)


