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
from selenium.webdriver.firefox.options import Options

current_image_index = 0

def ParseProdList(prlist): # function to catalog each item and its description
    t.sleep(2)
    for i in prlist:
        t.sleep(0.2)
        global product
        global new
        global current_image_index

        new['name'] = i.find_element(By.CLASS_NAME, "woocommerce-loop-product__title").text
        new['super'] = 3
        new['id'] = current_image_index

        if not i.find_elements(By.CLASS_NAME, "price"):
            new['ppu'] = 'OOS'
        else:
            if not i.find_elements(By.CLASS_NAME, "sale_price"):
                new['ppu'] = i.find_element(By.CLASS_NAME, "price").text
                new['supp'] = i.find_element(By.CLASS_NAME, "kilo-price.m-0").text
            else:
                new['ppu'] = i.find_element(By.CLASS_NAME, "sale_price").text
                new['supp'] = i.find_element(By.CLASS_NAME, "first-kilo-price.m-0").text        

        # gets the image URL
        src = i.find_element(By.TAG_NAME, "img").get_attribute("src")
        # ========
        # # Download the image and save it locally
        response = requests.get(src, stream = True)
        image = BytesIO(response.content)
        with open("images/3/image_" + str(current_image_index) + ".jpg", "wb") as f:   
            new['img'] = "images/3/image_" + str(current_image_index) + ".jpg"
            new['imgURL'] = src
            current_image_index+=1
            f.write(image.getvalue())
        # ======== 
        
        product = product.append(new, ignore_index=True)

def browse_categories(browser,wait):
    while True:
        t.sleep(2)
        prodlist = browser.find_elements(By.CLASS_NAME, "type-product")
        t.sleep(4)
        ParseProdList(prodlist)
        t.sleep(2)
        try:
            nextBtn = browser.find_element(By.CLASS_NAME, "next.page-numbers")
            el = wait.until(EC.element_to_be_clickable(nextBtn))
            el.click()
            t.sleep(4)
        except:
            break

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

    my_options = Options()
    # my_options.headless = True

    browser = webdriver.Firefox(options=my_options)
    browser.get('https://store2.com') # Replaced link for copyright issues

    global current_image_index
    current_image_index = index

    wait = WebDriverWait(browser, 15)

    t.sleep(8) # deny cookie policy
    try:
        element = browser.find_element(By.CLASS_NAME, "css-k8o10q") 
        ActionChains(browser).click(element).perform()
        t.sleep(1)
    except:
        print("No cookies pop up found")


    t.sleep(1) # close T.K. pop up
    try:
        element = browser.find_element(By.XPATH, "/html/body/div[3]/div/div/div/form/span/span[1]/span/span[1]/span")
        ActionChains(browser).click(element).perform()
        t.sleep(1)
        inputField = browser.find_element(By.XPATH, "/html/body/span[2]/span/span[1]/input")
        inputField.send_keys("73100")
        inputField.send_keys(Keys.ENTER)
        t.sleep(8)
        element = browser.find_element(By.ID, "submit-tk")
        ActionChains(browser).click(element).perform()
        t.sleep(10)
    except:
        print('T.K. button not found')


    # go to categories page
    t.sleep(2)
    element = browser.find_element(By.XPATH, "/html/body/div[4]/header/div/div[3]/div/nav/div[1]/div/ul/li[1]/a")
    ActionChains(browser).click(element).perform()


    # find each item category and browse through them with the browse_categories funtion
    t.sleep(16)
    listElement = browser.find_element(By.CLASS_NAME, "wpb_category_n_menu_accordion_list")
    listOfCategories = listElement.find_elements(By.XPATH, "./li")
    numOfCategories = len(listOfCategories)

    categoryElement = browser.find_element(By.XPATH, "/html/body/div[3]/div[1]/div/div/div/main/div/div[1]/div[3]/div/div/ul/li[3]/a")
    elementToClick = wait.until(EC.element_to_be_clickable(categoryElement))
    elementToClick.click()
    browse_categories(browser,wait)

    # start at 5 because at the time of running this script, eshop page had 1,2,3 categories of duplicated items,
    # and category 4 is already browsed outside the loop because of different XPATH
    for x in range(5, numOfCategories+10):
        t.sleep(2)
        try:
            categoryElement = browser.find_element(By.XPATH, "/html/body/div[4]/div[1]/div/div/div/main/div/div[1]/div[3]/div/div/ul/li[" + str(x) + "]/a")
            elementToClick = wait.until(EC.element_to_be_clickable(categoryElement))
            elementToClick.click()
            t.sleep(8)
            print(x)
            browse_categories(browser,wait)
        except:
            print("Skipped => ", x)

    product.to_excel('store2.xlsx', index=False)
    browser.quit()
    # No need to return the index