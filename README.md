# imovelweb Scraper

## Description

This web scraper takes data from the properties listed on [imovelweb](https://www.imovelweb.com.br/) based on three parameters given by the user:

1. State: The abbreviation of the state name to scrape ([here](https://brazil-help.com/brazilian_states.htm) is a list with all the states);
2. Property Type: The type of property to scrape. The user can choose to scrape information on houses or apartments (apts);
3. Contract Type: The type of contract to scrape. The user can choose to scrape information on properties listed for sale or for rent.

After choosing a combination of the three parameters above, the program will start running and scraping data from all the properties satisfy the user's conditions. The informations taken from the website are:

- **Link**: The link to the listing;
- **Price**: The price of the property (either a sale price or a rent price);
- **Condo Fee**: The condo fee of the property (not all properties have one, so in these cases the value will be 0);
- **District**: The district where the property is located;
- **City**: The city where the property is located;
- **Area**: The total area of the property;
- **Bedrooms**: The number of bedrooms in the property;
- **Bathrooms**: The number of bathrooms in the property;
- **Garage Spots**: The number of garage spots in the property;

The data is saved to a .csv file after each page is scraped (21 properties at a time), so even if the process is stopped midway through, the information already obtained is not lost.

## Usage

Before using the code, the user can install all the requires packages using [pipenv](https://pipenv.pypa.io/en/latest/) by running the following command inside the iw-scraper folder:

```
pipenv install
```

After that, to activate the environment containing all the packages:

```
pipenv shell
```

Finally, the scraper can be used by navigating to the scraper/ folder and calling the main.py file:

```
python main.py -s STATE -pt PROPERTY_TYPE -ct CONTRACT_TYPE
```

For example, to scrape the apartments listed for rent in the state of São Paulo, the user would call:

```
python main.py -s sp -pt apts -ct rent
```

By default, the scraper saves the data to a file named after the three parameters given (in the example above, the filename would be sp_apts_rent.csv), but the user can choose another name with the optional -fn option.

## Problems

Even though the scraper already works (at least to a certain extent), it is still in the development phase, and the main problems that it faces are:

1. Sometimes the scraper triggers a CAPTCHA response from the webpage, and in these cases the scraping cannot go ahead. Unfortunately, the only solution for now is to wait some time and try again.
2. After que 1000th page, the website redirects all other pages to the first one. Because of this, the scraper can only get the data from the properties on the first 1000 pages (21000 properties in total, since there are 21 per page).
3. A lot of properties appear in more than one page, so the final database has repeated rows. To solve this, the final step on the scraping process is to load the whole database and remove the repeated listings based on their link (unique id of a listing).
