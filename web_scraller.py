from time import sleep
import mechanicalsoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait 
from selenium.common.exceptions import TimeoutException, ElementNotInteractableException, InvalidElementStateException
import pandas as pd

def get_driver():
    options=webdriver.ChromeOptions()
    #options.add_argument("--headless")

    driver = webdriver.Chrome(options=options)
    driver.set_window_size(1080, 500)
    url = "https://www.latlong.net/convert-address-to-lat-long.html"
    driver.get(url)

    location = driver.find_element(By.CLASS_NAME, "width70")
    location.send_keys("")

    try:
        WebDriverWait(driver, 10).until(lambda x: x.find_element(By.ID, "onetrust-accept-btn-handler")) 
        btn = driver.find_element(By.ID, "onetrust-accept-btn-handler")
        btn.click()
    except TimeoutException:
        pass

    sleep(2)
    return driver

def write_and_get_value(driver, loc, prev_value):
    try:
        location = driver.find_element(By.CLASS_NAME, "width70")
        location.clear()
        location.send_keys(loc)
    except InvalidElementStateException as e:
        sleep(5)
        location = driver.find_element(By.CLASS_NAME, "width70")
        location.clear()
        location.send_keys(loc)

    btn = driver.find_element(By.ID, "btnfind")
    btn.click()

    def got_long(x):
        lng = x.find_element(By.ID, "lng")
        return lng.get_attribute('value') != prev_value

    WebDriverWait(driver, 10, 3).until(got_long) 

    lat = driver.find_element(By.ID, "lat")
    lng = driver.find_element(By.ID, "lng")
    return lat.get_attribute('value'), lng.get_attribute('value')


def fun(row):
    return f"{row['Zone']}, {row['Borough']}, New York"

driver = get_driver()    
df = pd.read_csv("taxi_zone_updated.csv")
df = df[df['Borough'] != 'Unknown']
df['loc'] = df.apply(fun, axis=1)

prev_value = '0.000000'
for i, row in df.iterrows():
    if row['lat'] != 0:
        print(f"{row['LocationID']}: already_processed")
        continue
    try:
        lat, lng =  write_and_get_value(driver, row['loc'], prev_value)
        prev_value = lng

        print(f"{row['loc']}: {lat},{lng}")
        df.loc[df['LocationID']==row['LocationID'], 'lat'] = lat
        df.loc[df['LocationID']==row['LocationID'], 'lng'] = lng
    except ElementNotInteractableException as e:
        #driver = get_driver()
        pass
    except TimeoutException as e:
        print("============Change IP==================")
        break
    


print(df[df['lat']==0])

df.to_csv('taxi_zone_updated.csv', index=False)

driver.quit()