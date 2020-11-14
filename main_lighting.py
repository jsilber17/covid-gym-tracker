import os 
import requests as r
import time
from datetime import datetime
from gpiozero import LED
from scrape import request_page, scrape 


def main(): 
    """ Add docstring here """ 

    report_num = 0
    led = LED(1)

    while True:
        soup = request_page('https://portal.rockgympro.com/portal/public/dd60512aa081d8b38fff4ddbbd364a54/occupancy?&iframeid=occupancyCounter&fId=1255')
        num_climbers, capacity = scrape(soup)
        if num_climbers != report_num:
            
            report_num = num_climbers
            percent_full = round(report_num / capacity, 2)
            
            led.close()

            if report_num <= 20:
                led = LED(11)
                led.on()
            elif report_num > 20 and report_num <= 30:
                led = LED(10)
                led.on()
            elif report_num > 30:
                led = LED(9)
                led.on()
            else: 
                print('Something has gone terribly wrong. There are only three colors on this stoplight!') 
                
            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    
if __name__ == '__main__': 
    main() 
