from bs4 import BeautifulSoup
from collections import OrderedDict
import pandas as pd
import re
import requests
import sys

sys.path.append("functions")

try:
    import extractors as ext
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    sys.exit()


def page_scraper(page_link, session):
    """
    Scrape information from a imovelweb page and return a pandas DataFrame
    with the collected data.

    Args:
        page_link (str): Full link to the imovelweb page to scrape
        session (requests.Session): Session object used to make the request

    Returns:
        properties_df (DataFrame): 
            Columns:
                Name: link, dtype: str
                Name: price, dtype: float64
                Name: condo fee, dtype: float64
                Name: district, dtype: str
                Name: city, dtype: str
                Name: area, dtype: int64
                Name: bedrooms, dtype: int64
                Name: bathrooms, dtype: int64
                Name: garage_spots, dtype: int64
    """
    
    # Initialize the DataFrame that will receive the scraped data
    properties_df = pd.DataFrame(columns = ["link", "price", "condo fee", "district",
                                            "city", "area", "bedrooms", "bathrooms",
                                            "garage_spots"])
    
    # Send the request to the given page_link and parse the response
    headers = OrderedDict({"accept-encoding": "gzip, deflate",
                           "accept": "*/*",
                           "connection": "keep-alive",
                           "user-agent": "Mozilla/5.0 "})
    
    page = session.get(page_link, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")

    # Get the tags containing the properties' information
    properties_raw = soup.find_all("div", {"class": "postingCard"})

    # Loop through all the properties on the page
    property_count = 0
    for property_raw in properties_raw:
        # Extract the details from the tags
        property_details = ext.details_extractor(property_raw)
        # Add the details to the DataFrame
        properties_df.loc[property_count, :] = property_details
        
        property_count += 1
        
        
    return properties_df


def get_number_pages(page_link, properties_per_page, session):
    """
    Scrape information from a imovelweb page and return the total number 
    of pages with the same [state, property_type, contract_type] parameter 
    combination.
    
    Args:
        page_link (str): Full link to the imovelweb page to scrape
        properties_per_page (int): Number of properties per page
        session (requests.Session): Session object used to make the request

    Returns:
        total_pages (int): Total number of pages
    """
    
    import math
    
    # Send the request to the given page_link and parse the response
    headers = OrderedDict({"accept-encoding": "gzip, deflate",
                           "accept": "*/*",
                           "connection": "keep-alive",
                           "user-agent": "Mozilla/5.0 "})
    
    page = session.get(page_link, headers = headers)
    soup = BeautifulSoup(page.content, "html.parser")
    
    # Get the tag containing the total number of properties
    total_listings_raw = soup.find("h1", {"class": "list-result-title"}).get_text()
    # Extract the number of properties from the tag
    total_listings = int(re.findall("[0-9.]+", total_listings_raw)[0].replace(".", ""))
    # Divide the number of properties by the number of properties per page to get the number of pages
    total_pages = math.ceil(total_listings/properties_per_page)

    return total_pages