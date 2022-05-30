# Anglia-Water-usage-scraper-for-InfluxDB
If you're a customer of Anglia Water with a smart water meter, this logs onto the Anglia website, scrapes recent usage data, and puts it into influxDB 

Anglia Water have a great website which lets you sign up to hourly water usage charts. Works really well - only fault is the lack of an API.

This is a substitute for that - it uses Selenium to log onto the website, extracts the recent hourly data, and adds it into influxDB.  I use this with openHAB, but could be used as part of any home automation setup.

Dependencies:
- a customer of Anglia Water with a smart water meter.
- you must have opted for hourly data on the website, and able to see the charts yourself if you log into the website
- an influxDB 1.x installation
- python packages: Selenium and influxdv - so 'python3 -m pip install selenium InfluxDB-Python'
- the Selenium chromedriver - instructions here: https://chromedriver.chromium.org/getting-started

I'm putting this into the public domain with no copyright claimed.
