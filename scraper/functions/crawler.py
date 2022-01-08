import pandas as pd
import random
import requests
import sys
import time

from requests.api import request

sys.path.append("functions")

import scrapers as scrp
import progress_bar as pb


def state_crawler(state_name, property_type, contract_type, filename):
    """
    Crawl through all the imovelweb pages with a certain [state, property_type and contract_type]
    parameter combination, scrape the information of each property and save it to a csv file.

    Args:        
        state_name (str): Name of the state (abbreviated)
        property_type (str): Type of property (casas (houses) or apartamentos (apartments))
        contract_type (str): Type of contract (aluguel (rent) or compra (sale))
        filename (str): Filename to use when saving the data
    """

    # Translate the terms used by the user into the terms used by the website
    ARGUMENTS = {"apts": "apartamentos", "houses": "casas",
                 "rent": "aluguel", "sale": "compra"}
    
    STATES = {"ac": "acre", "al": "alagoas", "ap": "amapa", "am": "amazonas", "ba": "bahia",
              "ce": "ceara", "es": "espirito-santo", "go": "goias", "ma": "maranhao",
              "mt": "mato-grosso", "ms": "mato-grosso-do-sul", "mg": "minas-gerais", "pa": "para",
              "pb": "paraiba", "pr": "parana", "pe": "pernambuco", "pi": "piaui", 
              "rj": "rio-de-janeiro", "rn": "rio-grande-do-norte", "rs": "rio-grande-do-sul",
              "ro": "rondonia", "rr": "roraima", "sc": "santa-catarina", "sp": "sao-paulo",
              "se": "sergipe", "to": "tocantins", "df": "brasilia-df"}
    
    property_type = ARGUMENTS[property_type]
    contract_type = ARGUMENTS[contract_type]
    state_name = STATES[state_name]

    # Initialize the requests session
    session = requests.Session()

    # Construct the link to the initial listings page
    page_link = (f"https://www.imovelweb.com.br/"
                 f"{property_type}-{contract_type}-{state_name}"
                 f"-ordem-visitas-maior.html")
    
    # Get the total number of pages that will be scraped
    total_pages = scrp.get_number_pages(page_link, 21, session)
    
    # After page 1000, all the pages redirect back to the first, 
    # so we can only scrape the first 1000 ones.
    if total_pages > 1000:
        total_pages = 1000
        
        
    time.sleep(2.0)

    # Initialize a progress bar
    progress_bar = pb.ProgressBar(total_steps = total_pages, 
                                  bar_size = 33, 
                                  message = "Scraping Pages:")

    # Loop through all the pages
    for page_number in range(1, total_pages + 1):
        # Update the progress bar and print it to the screen
        progress_bar.update_bar(current_step = page_number)
        progress_bar.print_bar()

        # Construct the link to the specific page
        page_link = (f"https://www.imovelweb.com.br/"
                     f"{property_type}-{contract_type}-{state_name}"
                     f"-pagina-{page_number}.html")
        
        # Scrape the data of all the properties on the page
        properties_df = scrp.page_scraper(page_link, session)

        # Append the data to the csv file
        if page_number == 1:
            properties_df.to_csv(path_or_buf = f"data/{filename}.csv", mode = "a",
                                 index = False)
        else:
            properties_df.to_csv(path_or_buf = f"data/{filename}.csv", mode = "a",
                                 header = False, index = False)            
        
        # Sleep for an interval between 0.1 and 0.5 second(s)
        time.sleep(0.1 + (0.4 * random.random()))
        
    # Open the saved database to delete the duplicated entries
    database = pd.read_csv(f"data/{filename}.csv")
    database = database.drop_duplicates("link")
    
    # Save the final database
    database = database.to_csv(f"data/{filename}.csv", index = False)
    