import os 
import requests as r
import time
from datetime import datetime
from gpiozero import LED
from scrape import request_page, scrape
from postgres_class import PostgresMonster 


def main(): 
    """
    Scrape Earthtreks webpage to find number of people at gym.
    Depending on # people, turn on traffic light colors on pi.
    Send all scraped information to a Postgres database.

    Keyword Arguments:  
        None

    Returns: 
        None
    """ 
    
    report_num = 0 # Initialize # climbers to zero 
    led = LED(1) # Initialize LED to 1 where no light exists  
    time.sleep(10) # Allow time for internet to boot before scraping 
    
    while True:
        
        # Scraping Golde webpage and requesting HTML 
        soup = request_page('https://portal.rockgympro.com/portal/public/dd6' \
                             '0512aa081d8b38fff4ddbbd364a54/occupancy?&ifram' \
                             'eid=occupancyCounter&fId=1255')
        num_climbers, capacity = scrape(soup)

        # This block executes if # climbers changes and updates
        if num_climbers != report_num:
            
            now = datetime.now() 
            dt_string = "'" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "'"

            report_num = num_climbers
            percent_full = round(report_num / capacity, 2)

            led = led.close()

            # Turning on the LED light 
            if percent_full <= 0.45: 
                led = LED(11)
                led.on()
            elif percent_full > 0.45 and report_num <= 0.667: 
                led = LED(10)
                led.on()
            elif percent_full > 0.667:  
                led = LED(9)
                led.on()
            else: 
                print('Something has gone terribly wrong.' \
                      'There are only three colors on this stoplight!')

            # Inserting data into the Postgres database 
            pgmon = PostgresMonster(dbname='earthtreks', 
                                    user='postgres', 
                                    password='password',  
                                    host='localhost', 
                                    port='5432')

            cursor, connection = pgmon.create_cursor_and_connection()
            pgmon.insert_rows('INSERT INTO ' \
                            'earthtreks.public.time_series_golden' \
                            '(datetime, num_climbers, capacity, percent_full)' \
                            'VALUES ({}, {}, {}, {})'.format(dt_string,
                                                             report_num,
                                                             capacity,
                                                             percent_full))

            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    
    

if __name__ == '__main__': 
    main() 
