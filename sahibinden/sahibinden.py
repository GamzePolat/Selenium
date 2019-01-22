from pymongo import MongoClient
from flask import Flask
import json
import urllib, json
from flask import jsonify
from selenium import webdriver
import time
client=MongoClient('127.0.0.1',27017)

#accesing db

db=client.mydb
browser = webdriver.Chrome("/home/gamzepolat/Belgeler/chromedriver_linux64/chromedriver")
url = "https://www.sahibinden.com/"
browser.get(url)
time.sleep(3)
nurl="https://www.sahibinden.com/kategori-vitrin?viewType=Gallery&category=3517"
browser.get(nurl)
time.sleep(3)
Url = "https://www.sahibinden.com/kategori-vitrin?viewType=Gallery&pagingOffset="
Url2 = "&category=3517"





lenOfPage = browser.execute_script(
    "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage;")
match = False
while (match == False):
    lastCount = lenOfPage
    time.sleep(3)
    lenOfPage = browser.execute_script(
        "window.scrollTo(0, document.body.scrollHeight); var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    if lastCount == lenOfPage:
        match = True

    time.sleep(3)

page_element = browser.find_elements_by_xpath("//*[@id='searchResultsSearchForm']/div/div[3]/div[4]/p")
time.sleep(3)
pageCount = 0
page = []
i = 0
carList= []
carDesc = []
carPr = []
carD = []
for pages in page_element:
    page.append(pages.text)
    pageno = str(page)
    pagesno = pageno.split(" ")[1]


while pageCount <= int(pagesno):
    sayfa = pageCount * 10 + i

    newUrl = Url + str(sayfa) + Url2

    browser.get(newUrl)
    time.sleep(3)
    carCodes = browser.find_elements_by_css_selector("div.searchResultsClassifiedId")
    carDescriptions = browser.find_elements_by_css_selector("a.classifiedTitle")
    carPrices = browser.find_elements_by_css_selector("div.searchResultsPriceValue > div")
    carDates = browser.find_elements_by_css_selector("div.searchResultsGallerySubContent > div")
    
    for carCode in carCodes:
        carList.append(carCode.text)
    for carDescription in carDescriptions:
        carDesc.append(carDescription.text)
    for carPrice in carPrices:
        carPr.append(carPrice.text)
    for carDate in carDates:
        carD.append(carDate.text)

    pageCount += 1
    i = i + 10
'''print(
    "carCodes:"+ carList[0],
    "carDesc:"+carDesc[0],
    "carPr:"+carPr[0],
    "carD:"+carD[0]
)'''
k=0
posts=db.carl
while k <= len(carList):
    post_data={
        'carCode':carList[k],
        'carDescription':carDesc[k],
        'carPrice':carPr[k],
        'carDate':carD[k]

    }
    
    result=posts.insert_one(post_data)
    k+=1
print('One Post: {0}' .format(result.inserted_id))

time.sleep(3)  
browser.close()
