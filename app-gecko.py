from flask import Flask, jsonify
from flask import request
import time
import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary


app = Flask(__name__)

# ---------- Selenium Run-----------
def  load_driver():
	options = webdriver.FirefoxOptions()
	
	# enable trace level for debugging 
	options.log.level = "trace"

	options.add_argument("-remote-debugging-port=9224")
	options.add_argument("-headless")
	options.add_argument("-disable-gpu")
	options.add_argument("-no-sandbox")

	binary = FirefoxBinary(os.environ.get('FIREFOX_BIN'))

	firefox_driver = webdriver.Firefox(
		firefox_binary=binary,
		executable_path=os.environ.get('GECKODRIVER_PATH'),
		options=options)

	return firefox_driver

@app.route('/', methods = ['GET'])
def data():
    driver = load_driver()

    product_name =  request.args['q']


    
    # Flipkart
    flipkart=[]
    prod = []
    price = []
    img = []

    
    driver.get("https://www.flipkart.com/") 
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input").click()
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[1]/div[2]/div[2]/form/div/div/input").send_keys(product_name)
    driver.find_element_by_xpath("/html/body/div/div/div[1]/div[1]/div[2]/div[2]/form/div/button").click()


    product = driver.find_elements_by_class_name('_4rR01T')
    price = driver.find_elements_by_xpath("//div[@class='_30jeq3 _1_WHN1']")
    images = driver.find_elements_by_xpath("//img[@class='_396cs4 _3exPp9']")



    print(product)
    for j in product:
        prod.append(j.text)
    for j in price:
        price.append(j.text)
    for j in images:
        img.append(j.get_attribute("src"))
    for i in range(len(prod)):
            d2 = {}
            d2['shopping_site']="flipkart"
            d2['product_name']=prod[i]
            d2['product_price']=int((price[i].lstrip("₹")).replace(",",""))
            d2['product_image'] = img[i]


            print(d2)
            flipkart.append(d2)


    """
     # amazon
    productlist = []
    pricelist = []
    imglist = []
    A = []

    driver.get("https://www.amazon.in/") # website name which we want to scrap
    driver.implicitly_wait(10) # waiting to quit
    driver.find_element(By.XPATH,"//input[contains(@id,'twotabsearchtextbox')]").send_keys(product_name) # Searching the product in amazon searchbar
    driver.find_element(By.XPATH,"//*[@id='nav-search-submit-button']").click() #//*[@id="nav-search-submit-button"]   
    try:
        product = driver.find_elements_by_xpath("//span[@class='a-size-medium a-color-base a-text-normal']") # product name
    except:
        product = driver.find_elements_by_xpath("//h2[@class='a-size-mini a-spacing-none a-color-base s-line-clamp-4']")
    price = driver.find_elements_by_xpath("//span[@class='a-price-whole']") # product price
    images = driver.find_elements_by_xpath("//img[@class='s-image']")
    for pro in product:
        productlist.append(pro.text)
    for p in price:
        pricelist.append(p.text)
    for image in images:
        imglist.append(image.get_attribute("src"))
    for i in range(len(productlist)):
        d = {}
        if(pricelist[i]==""):
            pass
        else:
            d['shopping_site']="amazon"
            d['product_name']=productlist[i]
            d['product_price']=int(pricelist[i].replace(",",""))
            d['product_image']=imglist[i]
            A.append(d)
    
    
    """

    driver.get("https://www.google.com/")
    title = driver.title
    driver.close()

    # final_list = A+B
    final_dict = sorted(flipkart, key = lambda i: i['product_price'])
    return jsonify(final_dict)

if  __name__ == "__main__":
	app.run(debug=True)
