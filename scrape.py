import os 
import requests as r

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

