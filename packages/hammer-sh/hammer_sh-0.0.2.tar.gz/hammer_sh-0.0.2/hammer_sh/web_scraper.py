import requests
from bs4 import BeautifulSoup
import pandas as pd

base_url = "https://link.springer.com"


def extract_abstracts():
    urls_to_search = {
        "Computer Sience": 'https://link.springer.com/search?facet-discipline=%22Computer+Science%22&facet-content'
                           '-type=%22Article%22&facet-language=%22En%22',
        "Chemistry": 'https://link.springer.com/search?facet-discipline=%22Chemistry%22&facet-content-type=%22Article'
                     '%22&facet-language=%22En%22',
        'Medicine': 'https://link.springer.com/search?facet-discipline=%22Medicine+%26+Public+Health%22&facet-content'
                    '-type=%22Article%22&facet-language=%22En%22 '
    }

    data = {}
    for key, url_to_search in urls_to_search.items():
        data[key] = scrape_over_pages(url_to_search, 50)

    df = []
    for category, abstracts in data.items():
        for abstract in abstracts:
            df.append([category, abstract])

    df = pd.DataFrame(df)
    df.head()
    return df


def get_abstracts(article_links):
    abstracts = []
    for link in article_links:
        url = base_url + link['href']
        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")
        abstract = soup.find("div", {"id": "Abs1-content"})
        if abstract is not None:
            abstracts.append(abstract.text)
    return abstracts


def analyze_page(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    article_links = soup.findAll('a', class_="title", href=True)
    next_page_object = soup.findAll('a', class_="next", href=True)
    next_page_link = base_url + next_page_object[0]['href']
    return article_links, next_page_link


def scrape_over_pages(start_url, number_of_results):
    results = []
    url = start_url
    while len(results) < number_of_results:
        article_links, url = analyze_page(url)
        abstracts = get_abstracts(article_links)
        results = results + abstracts
    return results
