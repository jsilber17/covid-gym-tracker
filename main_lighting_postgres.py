import os 
import requests as r
import time
from datetime import datetime
from gpiozero import LED
from scrape import request_page, scrape
from postgres_class import PostgresMonster 


def main(): 
    """ Add docstring here """ 

    report_num = 0
    led = LED(1)
    time.sleep(10)
    
    while True:
        soup = request_page('https://portal.rockgympro.com/portal/public/dd60512aa081d8b38fff4ddbbd364a54/occupancy?&iframeid=occupancyCounter&fId=1255')
        num_climbers, capacity = scrape(soup)
        if num_climbers != report_num:
            
            now = datetime.now() 
            dt_string = "'" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "'"

            report_num = num_climbers
            percent_full = round(report_num / capacity, 2)

            led = led.close()

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
                print('Something has gone terribly wrong. There are only three colors on this stoplight!')

            pgmon = PostgresMonster(dbname='earthtreks', 
                                    user='postgres', 
                                    password='password',  
                                    host='localhost', 
                                    port='5432')

            cursor, connection = pgmon.create_cursor_and_connection()
            pgmon.insert_rows('INSERT INTO earthtreks.public.time_series_golden (datetime, num_climbers, capacity, percent_full) VALUES ({}, {}, {}, {})'.format(dt_string, 
                                                                                                                                                                 report_num, 
                                                                                                                                                                 capacity, 
                                                                                                                                                                 percent_full))
            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    
    

if __name__ == '__main__': 
    main() 
