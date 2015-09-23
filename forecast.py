#!/usr/bin/python

# Weather forecast for Raspberry Pi w/Adafruit Mini Thermal Printer.
# Retrieves data from Yahoo! weather, prints current conditions and
# forecasts for next two days.  See timetemp.py for a different
# weather example using nice bitmaps.
# Written by Adafruit Industries.  MIT license.
#
# Required software includes Adafruit_Thermal and PySerial libraries.
# Other libraries used are part of stock Python install.
#
# Resources:
# http://www.adafruit.com/products/597 Mini Thermal Receipt Printer
# http://www.adafruit.com/products/600 Printer starter pack

from __future__ import print_function
import urllib, time
from Adafruit_Thermal import *
from xml.dom.minidom import parseString

# WOEID indicates the geographic location for the forecast.  It is
# not a ZIP code or other common indicator.  Instead, it can be found
# by 'manually' visiting http://weather.yahoo.com, entering a location
# and requesting a forecast, then copy the number from the end of the
# current URL string and paste it here.
WOEID = '976815'

# Select the units for degrees (Fahrenheit, f or Celsius, c).
# Changing the temperature unit also changes the other units. Imperial
# for Fahrenheit and Metric for Celsius.
tempUnit = 'c'

days = {
    'Mon': 'Ma',
    'Tue': 'Di',
    'Wed': 'Woe',
    'Thu': 'Do',
    'Fri': 'Vr',
    'Sat': 'Zat',
    'Sun': 'Zo'
}

conditions = ["Tornado", "Tropische storm", "Orkaan", "Zware onweersbuien", "Onweersbuien", "Regen en sneeuw", "Regen en ijzel", "Sneeuw en ijzel", "Aanvriezende motregen", "Motregen", "Aanvriezende regen", "Buien", "Buien", "Sneeuwvlagen", "Lichte sneeuwbuien", "Stuivende sneeuw", "Sneeuw", "Hagel", "IJzel", "Stof", "Mistig", "Nevel", "Nevel", "Stormachtig", "Winderig", "Koud", "Bewolk", "Wisselend bewolkt", "Wisselend bewolkt", "Gedeeltelijk bewolkt", "Gedeeltelijk bewolkt", "Helder", "Zonnig", "Mooi", "Mooi", "Regen en hagel", "Heet", "Plaatselijke buien", "Onweersbuien", "Onweersbuien", "Buien", "Zware sneeuwval", "Sneeuwbuien", "Zware sneeuwval", "Gedeeltelijk bewolkt", "Onweersbuien", "Sneeuwbuien", "Onweersbuien"]

# Dumps one forecast line to the printer
def forecast(idx):
	tag     = 'yweather:forecast'
	day     = days[dom.getElementsByTagName(tag)[idx].getAttribute('day')]
	lo      = dom.getElementsByTagName(tag)[idx].getAttribute('low')
	hi      = dom.getElementsByTagName(tag)[idx].getAttribute('high')
	cond    = dom.getElementsByTagName(tag)[idx].getAttribute('code')
	printer.boldOn()
	printer.print(day + ':')
	printer.boldOff()
	printer.feed(1)
	printer.print('Min. ' + lo)
	printer.print(deg)
	printer.print(' / Max. ' + hi)
	printer.print(deg)
	printer.feed(1)
	printer.println(conditions[int(cond)])

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)
deg     = chr(0xf8) # Degree symbol on thermal printer

# Fetch forecast data from Yahoo!, parse resulting XML
dom = parseString(urllib.urlopen(
        'http://weather.yahooapis.com/forecastrss?u=' + tempUnit +
        '&w=' + WOEID).read())

# Print heading
printer.inverseOn()
printer.print('{:^32}'.format(
  dom.getElementsByTagName('description')[0].firstChild.data))
printer.feed(1)
printer.inverseOff()

# Print current conditions
printer.feed(1)
printer.boldOn()
printer.print('{:^32}'.format('Weersomstandigheden:'))
printer.boldOff()
printer.print('{:^32}'.format(
  dom.getElementsByTagName('pubDate')[0].firstChild.data))
temp = dom.getElementsByTagName('yweather:condition')[0].getAttribute('temp')
cond = dom.getElementsByTagName('yweather:condition')[0].getAttribute('code')
currentConds = temp + deg + ' ' + conditions[int(cond)]
printer.boldOn()
printer.print('{:^32}'.format(currentConds))
printer.println(' ' + conditions[int(cond)])
printer.boldOff()
printer.feed(1)

# Print forecast
printer.boldOn()
printer.print('{:^32}'.format('Voorspelling:'))
printer.boldOff()
forecast(0)
printer.feed(1)
forecast(1)

printer.feed(3)
