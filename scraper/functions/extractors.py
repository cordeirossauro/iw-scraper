import re


def find_substring(substring, string):
    """
    Find a substring inside a string and return it.
    If there is no match, return 0.

    Args:
        substring (str): Substring to find (supports regex)
        string (str): String to search

    Returns:
        match (str): The first occurence of the substring inside the string,
                     or 0 if there is no match
    """
    
    try:
        match = re.findall(substring, string)[0]
    except IndexError:
        match = '0'

    return match


def details_extractor(property_raw):
    # Get the link to the listing
    link = property_raw["data-to-posting"]

    # Get the text of the tag containing the price of the property
    price_raw = property_raw.find("span", {"class": "firstPrice"}).get_text()
    # Extract the price from the text and convert it to a float
    price = float(find_substring("[0-9.]+", price_raw).replace(".", ""))

    try:
        # Try to get the text of the tag containing the condo fee
        condo_fee_raw = property_raw.find("span", {"class": "postingCardExpenses"}).get_text()
        # Try to extract the condo fee from the text and convert it to a float
        condo_fee = float(find_substring("[0-9.]+", condo_fee_raw).replace(".", ""))
    except AttributeError:
        # Some properties don't have a condo fee, so in these cases define its value as 0
        condo_fee = 0

    # Get the text of the tag containing the full addres of the property
    address_raw = property_raw.find("span", {"class": "postingCardLocation"}).get_text()
    # Split the text on the commas to separete the district from the city
    address_raw = [x.strip("\n ") for x in address_raw.split(",")]

    # Define the district and city
    district = address_raw[0]
    city = address_raw[1]    

    # Get the text of the tag containing the details of the property
    details_raw = property_raw.find("ul", {"class": "postingCardMainFeatures"})
    details = details_raw.get_text().replace("\n", "").replace("\t", "")

    # Extract the details from the text
    area = int(find_substring("(\d+) m²", details))
    bedrooms = int(find_substring("(\d+) quarto", details))
    bathrooms = int(find_substring("(\d+)ban", details))
    garage_spots = int(find_substring("(\d+)vaga", details))
    
    return [link, price, condo_fee, district,
            city, area, bedrooms, bathrooms,
            garage_spots]