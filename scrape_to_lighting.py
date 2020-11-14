import os 
import requests as r
import time
from datetime import datetime
from gpiozero import LED
from postgres_class import PostgresMonster 

def request_page(url):
    """Request a webpage.

    Keyword arguments: 
    url -- the url of the webpage requested 

    Returns: 
    page -- the text (HTML)  of the page requested

   """

    page = r.get(url).text 
    return page 

def scrape(page_text):
    """Scrape the webpage text for number of Golden climbers.

    Keyword arguments: 
    page_text -- The text of the webpage requested

    Returns: 
    num_climbers -- int that represents the number of climbers. 
    
    """ 

    page_str = str(page_text).split()
    
    for idx, string in enumerate(page_str): 
        if string == "'GOL'":
            num_climbers = int(page_str[idx + 8].replace(',', ''))
            capacity = int(page_str[idx + 5].replace(',', '')) 
            return (num_climbers, capacity)


def main(): 
    """ Add docstring here """ 

    report_num = 0
    
    while True:
        soup = request_page('https://portal.rockgympro.com/portal/public/dd60512aa081d8b38fff4ddbbd364a54/occupancy?&iframeid=occupancyCounter&fId=1255')
        num_climbers, capacity = scrape(soup)
        if num_climbers != report_num:
            
            now = datetime.now() 
            dt_string = "'" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "'"

            report_num = num_climbers
            percent_full = round(report_num / capacity, 2)

            if report_num <= 35:
                led = LED(11)
                led.on()
            elif report_num > 35 and report_num <= 42:
                led = LED(10)
                led.on()
            elif report_num >= 43:
                led = LED(9)
                led.on()
            else: 
                print('Something has gone terribly wrong. There are only three colors on this stoplight!') 
                

            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    
if __name__ == '__main__': 
    main() 
