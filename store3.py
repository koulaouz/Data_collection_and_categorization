from io import BytesIO
import time as t
import pandas as pd
import requests
import self as self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import urllib
from bs4 import BeautifulSoup as BS
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

current_image_index = 0

def scroll_down(browser):
    while True:
        try:
            browser.find_element(By.CLASS_NAME, "sc-gbh03z-9.bldYsO") # not available products appear last
            break
        except:
            try:
                browser.find_element(By.CLASS_NAME, "sc-ak6cwf-18.flLzsr") # loading more
            except:
                break
            browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

def ParseProdList(prlist):
    for i in prlist:
        t.sleep(0.25)
        global current_image_index
        global product
        global new

        new['name'] = i.find_element(By.CLASS_NAME, "sc-y4jrw3-11.bdHXOv").text #CHECKED
        new['super'] = 2
        new['id'] = current_image_index
        try:
            new['ppu'] = i.find_element(By.CLASS_NAME, "sc-1qeaiy2-2.jRcVje").text
            new['supp'] = i.find_element(By.CLASS_NAME, "sc-1qeaiy2-3.eRQrsg").text
        except:
            try:
                new['ppu'] = i.find_element(By.CLASS_NAME, "sc-1qeaiy2-2.oTEfA").text
                new['supp'] = i.find_element(By.CLASS_NAME, "sc-1qeaiy2-3.eRQrsg").text
            except:
                new['ppu'] = 'OOS'
                new['supp'] = 'OOS'


        try:
            src = i.find_element(By.CLASS_NAME, "sc-y4jrw3-1.bDBcGF").get_attribute("src")
            # # Download the image and save it locally
            response = requests.get(src, stream = True)
            image = BytesIO(response.content)
            with open("images/2/image_" + str(current_image_index) + ".jpg", "wb") as f:   
                new['img'] = "images/2/image_" + str(current_image_index) + ".jpg"
                new['imgURL'] = src
                current_image_index+=1         
                f.write(image.getvalue())
        except:
            print('No img')

        product = product.append(new, ignore_index=True)

product = pd.DataFrame({},index=[0])
product['name'] = ''
product['super'] = ''
product['id'] = ''
product['ppu'] = '' #price per unit
product['supp'] = '' # supplementary price
product['img'] = ''
product['imgURL'] = ''
new = product

def Main(index):

    browser = webdriver.Firefox()
    browser.get('https://store3.com') # Replace link for copyright issues
    browser.maximize_window()

    wait = WebDriverWait(browser, 15)
    
    global current_image_index
    current_image_index = index

    # cookies
    element = browser.find_element(By.XPATH, "/html/body/div[2]/div/div[5]/div/div/div/div[1]/button/div/div")
    elementToClick = wait.until(EC.element_to_be_clickable(element))
    elementToClick.click()

    # handle pop up    
    t.sleep(1)
    body = browser.find_element(By.XPATH, "/html/body")
    body.send_keys(Keys.ESCAPE)
    t.sleep(3)

    #Open eshop dropdown to access the categories
    t.sleep(4)
    element = browser.find_element(By.XPATH, "/html/body/div[1]/div/header/div/div[2]/div[2]/div/div/div[1]/div/button/span")
    ActionChains(browser).click(element).perform()
    #Click category
    t.sleep(4)
    listElement = browser.find_element(By.CLASS_NAME, "sc-1ns5dex-3.eBbPLC")
    listOfCategories = listElement.find_elements(By.CLASS_NAME, "sc-1l7fdca-0.dqembg")
    numOfCategories = len(listOfCategories)

    t.sleep(1)
    for x in range(1, numOfCategories + 1):
        if (x==6 or x==10 or x==12):
            element = browser.find_element(By.XPATH, "/html/body/div[1]/div/header/div/div[2]/div[2]/div/div/div[1]/div/div[2]/div/div[1]/div[2]/div[" + str(x) + "]/a/div[2]") #οπωροπολειο
            elementToClick = wait.until(EC.element_to_be_clickable(element))
            elementToClick.click()
            t.sleep(6)
            #Browse category
            scroll_down(browser)
            prodlist = browser.find_elements(By.CLASS_NAME, "sc-y4jrw3-0.gTTPXD")
            ParseProdList(prodlist)
            element = browser.find_element(By.XPATH, "/html/body/div[1]/div/header/div/div[2]/div[2]/div/div/div[1]/div/button/span")
            elementToClick = wait.until(EC.element_to_be_clickable(element))
            elementToClick.click()

    product.to_excel('store3.xlsx', index=False)
    browser.quit()
    return current_image_index