#!/usr/bin/env python3

from influxdb import InfluxDBClient
from datetime import datetime
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
import time
import json

# you will of course need to customise usernames/passwords
# not very secure at present
anglia_username = "someone@someone.com"
anglia_password = "password123"

influxdb_username = "openhab"
influxdb_password = "password123"
influxdb_url = "127.0.0.1"
influxdb_port = 8086

# if you set debug_mode to True then chrome runs in a window, so you can see what the script is doing
# and it sends text updates to the terminal
# if you send False then it's silent, save for sending "Done!" if the script succeeds
debug_mode = False

webpage = r"https://my.anglianwater.co.uk/"

opts = Options()
opts.headless = not debug_mode


def PrintDebug(text):
    if debug_mode is True:
        print(text)


driver = Chrome(options=opts)
driver.set_window_size(1600, 1200)


driver.get(webpage)

PrintDebug("logging in")
sbox = driver.find_element_by_id("existUser")
sbox.send_keys(anglia_username)

sbox = driver.find_element_by_id("existPass")

sbox.send_keys(anglia_password)

button = driver.find_element_by_id("existingLogIn")
button.click()


PrintDebug("Selecting usage")

button = driver.find_element_by_id("btnViewUsage")
button.click()

PrintDebug("selecting hourly")
button = driver.find_element_by_xpath('//*[@id="dbserialnumber"]/div/div[1]/div[1]/label/span')
button.click()


time.sleep(2)
PrintDebug("saving page")

html = driver.page_source
driver.quit()

startdata = html.find("var myUsageDetails_days = ") + 26
enddata = html.find(";;", startdata)
result = html[startdata: enddata]

data = json.loads(result.replace("'", '"'))

json_body = []

for x in data:
    date_object = datetime.strptime(x['groupDate'] + " " + x['time'], "%d-%b-%Y %H:%M")
    
    item = {"measurement": "anglia_water_usage", "time": date_object, "fields": {"value": x["usage"] * 1000}}

    json_body.append(item)


# print(json_body)

client = InfluxDBClient(influxdb_url, influxdb_port, influxdb_username, influxdb_password, 'openhab_db')

client.write_points(json_body)

print("Done!")
