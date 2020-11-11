import os 
import requests as r
import time
from datetime import datetime
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
    num_climbers - int that represents the number of climbers. 
    """ 
    page_str = str(page_text).split()
    
    for idx, string in enumerate(page_str): 
        if string == "'GOL'":
            num_climbers = int(page_str[idx + 8].replace(',', '')) 
            return num_climbers

def main(): 
    """Tracks changes in number of climbers at EarthTreks.
       Scrapes data from EarthTreks webpage & INSERTS INTO Postgres DB
       For now, runs on an infinite loop
    """ 
    report_num = 0
    
    while True:
        soup = request_page('https://portal.rockgympro.com/portal/public/dd60512aa081d8b38fff4ddbbd364a54/occupancy?&iframeid=occupancyCounter&fId=1255')
        num_climbers = scrape(soup)
        if num_climbers != report_num:
            
            now = datetime.now() 
            dt_string = "'" + str(now.strftime("%d/%m/%Y %H:%M:%S")) + "'"

            report_num = num_climbers
           
            pgmon = PostgresMonster(dbname='earthtreks', user='postgres', password=os.environ.get('POSTGRES_PASSWORD'),  host='localhost', port='5432')
            cursor, connection = pgmon.create_cursor_and_connection()
            
            pgmon.insert_rows('INSERT INTO earthtreks.public.time_series_golden (datetime, num_climbers) VALUES ({}, {})'.format(dt_string, report_num))
            print('{} climbers are at EarthTreks'.format(report_num))
        
        else: 
            pass
    

if __name__ == '__main__': 
    main() 
