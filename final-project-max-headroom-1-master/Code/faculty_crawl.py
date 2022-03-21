import json
import requests
import re
import bs4
import Code.util as util
import Code.website_fuctions as website_fuctions


def url_management(current_url, url):
    """
    Processes URLs for passing to crawler. Removes fragments then converts from
    relative to absolute url.

    Input:
        current_url - string - url of the page target url scraped from
        url - string - target url for conversion

    Output:
        url - string - fully cleaned and ready for validation check
    """
    url = util.remove_fragment(url)
    url = util.convert_if_relative_url(current_url, url)

    return url


def url_scrape(soup, url, limiting_domain):
    """
    Pulls all URLs from soup and returns list of valid pages.

    Input:
        soup - soup - the full soup of the scraped page
        url - string - url of the scraped page
        limiting_domain - string - the url of the 'root' domain

    Output:
        linklst - list of strings - list of all valid urls for scraping
    """

    if limiting_domain == "harris.uchicago.edu/directory":
        return website_fuctions.harris_links(soup, url, limiting_domain)

    elif limiting_domain == "socialsciences.uchicago.edu/directory":
        return website_fuctions.ssd_links(soup, url, limiting_domain)


def page_scrape(url):
    """
    scrapes webpage and returns soup

    Input:
        url - string - the url of the webpage to be scraped

    Output:
        soup - soup - soup of entire page
    """
    headers = {
        "User-Agent": "web scraper for classroom purposes \
                helbing@uchicago.edu"
    }
    response = requests.get(url, headers=headers)
    response_txt = response.text
    soup = bs4.BeautifulSoup(response_txt, "html.parser")
    return soup


def page_content(soup, url, limiting_domain):
    """
    takes a page soup and pulls professor names and links

    Input:
        soup - soup - full page soup

    Output:
        content - dict - a dictionary with professor name as key
            "Linked Page": the website on their directory page
            "Directory Page": the visited directory page (where this is
                              scraping from)
            "University": will eventually be the university information
    """
    if limiting_domain == "harris.uchicago.edu/directory":
        return website_fuctions.harris_content(soup, url)

    elif limiting_domain == "socialsciences.uchicago.edu/directory":
        return website_fuctions.ssd_content(soup, url)


def go(num_pages_to_crawl, index_filename, starting_url, limiting_domain):
    """
    Crawl the college directory and generates a json file.

    Inputs:
        num_pages_to_crawl: the number of pages to process during the crawl
        index_filename: the name for the json.
        college: 

    Outputs: 
        json file of the index_filename.

    The websites, in dictionary format, not because it's for use this way, but 
    so in case, it's just easier to work with.
        # start_lim_dom_dic = {
         "Social Sciences": (
             "https://socialsciences.uchicago.edu/directory",
             "socialsciences.uchicago.edu/directory",
        ),
        "Harris": (
            "https://harris.uchicago.edu/directory",
            "harris.uchicago.edu/directory",
        ),
    }
    """

    # construct queue and load start
    crawler = [starting_url]
    visited_pages = []
    faculty_here = {}

    # visit up to specified number of pages or stop when queue empty
    while len(visited_pages) < num_pages_to_crawl and len(crawler) > 0:
        page_to_vist = crawler.pop(0)
        print("Page to Visit: ", page_to_vist)
        print(f"The current length of crawler: {len(crawler)}")
        print(f"The number of pages visited: {len(visited_pages)}")
        # skip previously visited pages
        if page_to_vist not in visited_pages:
            # update list of visited pages
            visited_pages.append(page_to_vist)
            # load content of page into soup object
            soup = page_scrape(page_to_vist)
            # pulls list of valid links
            linklst = url_scrape(soup, page_to_vist, limiting_domain)
            # update master faculty_here with new titles: {content} from page
            faculty_here.update(page_content(soup, page_to_vist, limiting_domain))
            # update queue of links to visit
            for link in linklst:
                if link not in crawler and link not in visited_pages:
                    crawler.append(link)

    write_txt(faculty_here, f"Code/data/{index_filename}")


def write_txt(faculty, index_filename):
    """
    writes a file name with data
    """

    with open(f"{index_filename}.txt", "w") as f:
        f.write(json.dumps(faculty))

    with open(f"{index_filename}.json", "w") as f:
        f.write(json.dumps(faculty))
