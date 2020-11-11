import os 
import requests as r
import time
from datetime import datetime
from postgres_class import PostgresMonster 

def request_page(url): 

    page = r.get(url).text 
    return page 

def scrape(page_text): 

    page_str = str(page_text).split()
    for idx, string in enumerate(page_str): 
        if string == "'GOL'":
            num_climbers = int(page_str[idx + 8].replace(',', '')) 
            return num_climbers

def main(): 
    
    report_num = 0
    
    while True:
        soup = request_page('https://portal.rockgympro.com/portal/public/dd60512aa081d8b38fff4ddbbd364a54/occupancy?&iframeid=occupancyCounter&fId=1255')
        num_climbers = scrape(soup)
        if num_climbers != report_num:
            
            now = datetime.now() 
            dt_string = "'" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "'"

            report_num = num_climbers
           
            pgmon = PostgresMonster(dbname='earthtreks', user='postgres', password='Bocaj123!',  host='localhost', port='5432')
            cursor, connection = pgmon.create_cursor_and_connection()
            
            pgmon.insert_rows('INSERT INTO earthtreks.public.time_series_golden (datetime, num_climbers) VALUES ({}, {})'.format(dt_string, report_num))
            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    

if __name__ == '__main__': 
    main() 
