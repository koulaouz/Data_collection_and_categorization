import time as t
import pandas as pd
import self as self
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver import ActionChains
import urllib
from bs4 import BeautifulSoup as BS
from io import BytesIO
import requests
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# =======
product = pd.DataFrame({},index=[0])
product['name'] = ''
product['super'] = ''
product['id'] = ''
product['ppu'] = '' # price per unit
product['supp'] = '' # supplementary price
product['img'] = '' 
product['imgURL'] = ''
new = product

current_image_index = 0

def scroll_down(browser):
    while True:
        try:
            tosa_apo = browser.find_element(By.CLASS_NAME, "current-page").text
            tosa = tosa_apo.split()[0]
            apo = tosa_apo.split()[3]
            if tosa == apo:
                break
            else:
                browser.execute_script("window.scrollTo(0,0)")
                t.sleep(0.5)
                browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")
                t.sleep(0.5)
        except:
            print("ERROR line 42 -------------------------")

def ParseProdList(prlist):
    for i in prlist:
        t.sleep(0.5)
        global product
        global new
        global current_image_index

        new['name'] = i.find_element(By.CLASS_NAME, "product__title").text
        new['super'] = 1
        new['id'] = current_image_index

        # gets the image URL
        src = i.find_element(By.TAG_NAME, "img").get_attribute("src")

        # ========
        # # Download the image and save it locally
        response = requests.get(src, stream = True)
        image = BytesIO(response.content)
        with open("images/1/image_" + str(current_image_index) + ".jpg", "wb") as f:   
            new['img'] = "images/1/image_" + str(current_image_index) + ".jpg"
            new['imgURL'] = src;
            current_image_index+=1         
            f.write(image.getvalue())

        # ========
        if not i.find_elements(By.CLASS_NAME, "price"):
            new['ppu'] = 'OOS'
        else:
            new['ppu'] = i.find_element(By.CLASS_NAME, "price").text

        if not i.find_elements(By.CLASS_NAME, "priceKil"):
            new['supp'] = 'NA'
        else:
            new['supp'] = i.find_element(By.CLASS_NAME, "priceKil").text
            

        product = product.append(new, ignore_index=True)

def browse_categories(num_cat, id, browser,wait):
    for i in range(1, num_cat+1):
        browser.execute_script("window.scrollTo(0,0);")
        t.sleep(2)
        element = browser.find_element(by=By.XPATH, value="/html/body/div[1]/div/aside/div/div[2]/div[4]/nav/ul/li[" + str(id) + "]/ul/li["  + str(i) +  "]/a")
        if i == 1:
            t.sleep(2)
        t.sleep(1)
        browser.execute_script("arguments[0].scrollIntoView(true);", element)
        t.sleep(1.5)
        elementToClick = wait.until(EC.element_to_be_clickable(element))
        elementToClick.click()
        t.sleep(6)
        scroll_down(browser)
        t.sleep(1)

        prodlist = browser.find_elements(By.CLASS_NAME, "product")
        t.sleep(6)
        print(current_image_index)
        ParseProdList(prodlist)
        t.sleep(2)

# =====================================

def Main(index):
    browser = webdriver.Firefox()
    browser.get('https://www.store1.com/') # Replaced link for copyright issues
    browser.maximize_window()
    wait = WebDriverWait(browser, 15)
    
    global current_image_index

    current_image_index = index
    # COOKIES HANDLER
    t.sleep(4) 
    element = browser.find_element(by=By.XPATH, value="/html/body/div[3]/div[1]/div[2]/button[3]")
    elementToClick = wait.until(EC.element_to_be_clickable(element))
    elementToClick.click()

    element = browser.find_element(by=By.XPATH, value="/html/body/div[1]/div/header/div[2]/div/nav/ul[1]/li[1]/a")
    elementToClick = wait.until(EC.element_to_be_clickable(element))
    elementToClick.click()

    t.sleep(5)

    listElement = browser.find_element(By.CLASS_NAME,"mainNav_ul")
    listOfCategories = listElement.find_elements(By.XPATH, "./li")
    numOfCategories = len(listOfCategories)

    for x in range(1,numOfCategories):
        t.sleep(5)
        categoryElement = browser.find_element(By.XPATH,"/html/body/div[1]/div/aside/div/div[2]/div[4]/nav/ul/li[" + str(x) + "]")
        classNamesOfElement = categoryElement.get_attribute("class")
        # if x==13 or x==22:
        if "separator-line" in classNamesOfElement:
            print("SKIPPED SEPARATING LINE.")
            browser.execute_script("window.scrollTo(0, 0);")
            t.sleep(1)
        else:
            element = browser.find_element(by=By.XPATH, value="/html/body/div[1]/div/aside/div/div[2]/div[4]/nav/ul/li[" + str(x) + "]/span/span")
            # browser.execute_script("arguments[0].scrollIntoView(true);", element)
            elementToClick = wait.until(EC.element_to_be_clickable(element))
            elementToClick.click()
            # SUB-CATEGORIES
            childList_element = browser.find_element(By.XPATH,"/html/body/div[1]/div/aside/div/div[2]/div[4]/nav/ul/li[" + str(x) + "]/ul")
            ch = childList_element.find_elements(By.XPATH, "./li")
            numOf_SUB_categories = len(ch)

            browse_categories(numOf_SUB_categories, x, browser,wait)

    product.to_excel('store1.xlsx', index=False)
    browser.quit()
    return current_image_index