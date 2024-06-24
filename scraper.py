""" 
    Resources:
    - https://www.zippia.com/advice/average-cost-of-groceries-by-state/
"""
import os

import pandas as pd
import requests
from bs4 import BeautifulSoup

RTDIR = os.path.dirname(__file__)

def scrape_website(url: str) -> BeautifulSoup:
    """ Scrape the html document from the website

    Args:
        url (str): The URL to scrape the link from

    Returns:
        BeautifulSoup: A parsed and objectified version of the html document from the link.
    """
    # Perform the request
    response = requests.get(url=url, timeout=10)

    # Check if the HTTP request was successful
    if response.status_code == 200:
        return BeautifulSoup(response.text, 'html.parser')

    print('Failed to retrieve HTML.')
    return None

def parse_html(soup: BeautifulSoup) -> pd.DataFrame:
    """ Extracts useful information from the parsed HTML.

    Args:
        html (BeautifulSoup): HTML file that has been received and parsed by BeautifulSoup

    Returns:
        pd.DataFrame: DataFrame that was constructed and formatted from html data
    """
    # Find all links that contain an href
    links = soup.find_all('a', href=True)

    # For each link, check whether it contains a Wordle option
    option_list = []
    for link in links:
        if "/unscramble/" in link['href']:
            # option_list.append(link.text)
            option_list.append(link.text)

    options = pd.Series(option_list)
    return options


def parse_table(soup: BeautifulSoup) -> pd.DataFrame:
    """ Scrapes a table from the webpage into a pandas dataframe

    Args:
        html (BeautifulSoup): HTML file that has been received and parsed by BeautifulSoup

    Returns:
        pd.DataFrame: DataFrame that was constructed and formatted from the table
    """
    tbl = soup.find("table")
    df = pd.read_html(str(tbl))[0]

    return df

if __name__ == "__main__":
    URL = "https://www.zippia.com/advice/average-cost-of-groceries-by-state/"
    HTML = scrape_website(url=URL)
    db = parse_table(soup=HTML)
    # db.to_csv(path_or_buf=f"{RTDIR}/groceries.csv", index=False, header=False)
    print(db)
