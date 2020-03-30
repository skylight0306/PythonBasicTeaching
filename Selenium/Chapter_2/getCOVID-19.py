# -*- coding: utf-8 -*-
import json
import time
import os
import sys

from selenium import webdriver
from urllib.request import urlretrieve
import time

driver = webdriver.Firefox(executable_path = os.getcwd() + '/geckodriver')

ConfirmedDict = {}
ConfirmedKeyList = ['編號', '確診日', '年齡', '身份', '狀況']

def Main():
    # 主要執行區塊

    driver.get('https://infogram.com/--1h8j4xgy7x1d6mv')  # 取得URL 開啟瀏覽器
    # UrlBaseName = getUrlBaseName(buy_url=i)  # 取得URL的最後'/'後面的參數值 + 日期為資料夾名稱
    time.sleep(3)  # 等待個5秒
    moveBottom()
    getDataList = getConfirmed()

    # listToStr(get_list=getDataList)


    # downloadImgDict(dirs_str = UrlBaseName, save_img_dict = getContentsPhoto())  # 將取得到的圖片儲存到相對應的資料夾底下
    # data_str = dataIntegration(getTitleName(), getContentName(), getPriceTotal(), getContentsText(), getStandardEquipment(), getProductSpecification(), str(i))  # 將所有取得到的資料放在一起
    # writeFile(dir_str = UrlBaseName, write_str = data_str)  # 最後將資料寫到對應的資料夾內，另名為note.txt
    driver.quit()  # 關閉瀏覽器，收工搞定


def dataIntegration(*args):
    # 將取得的 標題 內容 金額 其他備註 整合起來
    data_str = '*' * 10 + '\n'
    data_list = []
    args = list(args)
    for arg in args:
        data_list.append(data_str + arg)
    all_data_str = '\n'.join(data_list)
    print(all_data_str)
    return all_data_str


def getConfirmed():
    getDataList = []
    EachConfirmedList = []
    Confirmed = driver.find_elements_by_css_selector(".igc-table-scrollable tbody tr")
    times = 0
    for i in Confirmed:
        times = times + 1
        EachConfirmedList.append(i.text)
        print(i.text)
        listToStr = ''.join(EachConfirmedList)
        strTolist = listToStr.split()
        mergeEachListToDict = dict(zip(['編號', '確診日', '年齡', '身份', '狀況'], strTolist))
        getEachDict = {EachConfirmedList[0]: mergeEachListToDict}
        ConfirmedDict.update(getEachDict)
        EachConfirmedList = []
        # if (times % 5 == 0) and (times != 0):
        #     mergeEachListToDict = dict(zip(['編號', '確診日', '年齡', '身份', '狀況'], ' '.join(EachConfirmedList)))
        #     getEachDict = {EachConfirmedList[0]: mergeEachListToDict}
        #     ConfirmedDict.update(getEachDict)
        #     EachConfirmedList = []

    print(ConfirmedDict)
    # print(times)


def getUrlBaseName(buy_url):
    # 取得URL，Base Name
    getUrlName = os.path.basename(buy_url)
    getUrlName = getUrlName + '_' + str(time.strftime("%m%d%Y%I%M%S"))
    print('getUrlName: %s' % getUrlName)
    return getUrlName


def writeFile(dir_str, write_str):
    # 寫入到Url資料夾下的note.txt
    fp = open(os.getcwd() + "/" + dir_str + "/note.txt", "w")
    fp.write(write_str)
    fp.close()


def getContentsText():
    # 取得 本商品詳細介紹 文字
    ContentsTextList = []
    contents_data = driver.find_elements_by_css_selector("#IntroContainer dd")
    for content_data in contents_data:
        ContentsTextList.append(content_data.text)
    ContentsTextStr = '\n'.join(ContentsTextList)
    print('getContentsText: %s' % ContentsTextStr)
    return ContentsTextStr


def getContentsPhoto():
    # 取得 本商品詳細介紹 全部圖片
    ContentsImgList = []
    ContentsImgListName = []
    contents_data = driver.find_elements_by_css_selector("#IntroContainer dd img")
    for content_data in contents_data:
        ContentsImgList.append(content_data.get_attribute("src"))
        ContentsImgListName.append(os.path.basename(content_data.get_attribute("src")))
    ContentsDict = dict(zip(ContentsImgListName, ContentsImgList))
    print('ContentsDict: %s' % ContentsDict)
    return ContentsDict


def getTitleName():
    # 取得網頁商品標題名稱
    title_name = driver.find_element_by_id("NickContainer").text
    print('getTitleName: %s' % title_name)
    return title_name


def getContentName():
    # 取得網頁商品大綱內容
    content_name = driver.find_element_by_id("SloganContainer").text
    print('content_name: %s' % content_name)
    return content_name


def getPriceTotal():
    # 取得網頁商品金額
    price = driver.find_element_by_id("PriceTotal").text
    print('getPriceTotal: %s' % getPriceTotal)
    return price


def getTitlePhotoUrl():
    # 取得網頁商品圖片連結
    title_photo_url = driver.find_element_by_css_selector("#ImgContainer img").get_attribute("src")
    print('title_photo_url: %s' % title_photo_url)
    return title_photo_url


def getStandardEquipment():
    # 取得標準配件資訊
    standard_equipment = driver.find_element_by_css_selector("#EquipContainer").text
    print('standard_equipment: %s' % standard_equipment)
    return standard_equipment


def getProductSpecification():
    # 取得 商品規格資訊
    product_specification = driver.find_element_by_css_selector("#StmtContainer").text
    print('product_specification: %s' % product_specification)
    return product_specification


def getTitlePhotoName():
    # 取得網頁商品圖片的名稱
    title_photo_url = driver.find_element_by_css_selector("#ImgContainer img").get_attribute("src")
    title_photo_url_name = os.path.basename(title_photo_url)
    print('title_photo_url_name: %s' % title_photo_url_name)
    return title_photo_url_name


def downloadImgDict(dirs_str, save_img_dict):
    # 下載多個圖片到本地端，透過URL Base name 建立資料夾。

    os.makedirs(os.getcwd() + '/' + str(dirs_str), exist_ok = True)  # 建立目錄存放檔案
    for imgName, imgUrl in save_img_dict.items():
        saveFilePath = os.getcwd() + '/' + str(dirs_str) + '/' + str(imgName)
        urlretrieve(imgUrl, saveFilePath)  # 儲存圖片
        print("下載檔案至: " + saveFilePath)
    print("下載完成。")


def moveBottom():
    # 滑動到最下方
    js = "var q=document.documentElement.scrollTop=100000"
    driver.execute_script(js)
    print("滑動到頁面最下方")


if __name__ == '__main__':
    Main()

