import argparse
import glob
import os
import sys

sys.path.append("functions")

try:
    import crawler as crwl
except ModuleNotFoundError:
    print("Could not find the necessary functions inside their folder...")
    sys.exit()


def get_args():
    parser = argparse.ArgumentParser()

    parser.add_argument("-s",
                        help="abbreviated name of the state to scrape",
                        choices = ["ac", "al", "ap", "am", "ba", "ce", "es", "go", "ma",
                                   "mt", "ms", "mg", "pa", "pb", "pr", "pe", "pi", "rj",
                                   "rn", "rs", "ro", "rr", "sc", "sp", "se", "to", "df"],
                        nargs = 1,
                        required=True,
                        action="store")


    parser.add_argument("-pt",
                        help="type of property to scrape (apartments or houses)",
                        choices=["apts", "houses"],
                        nargs = 1,
                        required=True,
                        action="store")


    parser.add_argument("-ct",
                        help="type of contract to scrape (rent or sale)",
                        choices=["rent", "sale"],
                        nargs = 1,
                        required=True,
                        action="store")
    
    parser.add_argument("-fn",
                        help="filename to use when saving the data",
                        nargs = 1,
                        required=False,
                        metavar = "filename",
                        action="store")

    args = parser.parse_args()

    return args


def create_database(state_name, property_type, contract_type, filename):
    """
    Create a database with data scraped from imovelweb.com.br considering only
    properties from a certain state, with a certain type and kind of contract.

    Args:
        state_name (str): Name of the state to scrape data from
        property_type (str): Type of property (houses or apts) to scrape
        contract_type (str): Type of contract (rent or sale) to scrape
        filename (str): Filename to use when saving the data
    """
    
    # Call the crawler and print a message when it finishes
    crwl.state_crawler(state_name, property_type, contract_type, filename)
    print(f"\nScraping done! Check data/{filename}.csv to see the results.")


if __name__ == "__main__":
    # If it does not exist, create the data folder
    os.makedirs("data", exist_ok=True)
    
    # Get the arguments passed by the user
    args = get_args()

    # If no filename was given, construct one based on the parameters
    if args.fn is None:
        filename = f"{args.s[0]}_{args.pt[0]}_{args.ct[0]}"
        print(f"File name not given. Using the default one: {filename}\n")
    else:
        filename = args.filename[0]
        
    # Check if the filename already exists
    if f"data/{filename}.csv" in glob.glob("data/*.csv"):
        print("Another file with the same name already exists, try again.")
        sys.exit()

    # Call the function to create the database
    create_database(args.s[0], args.pt[0], args.ct[0], filename)