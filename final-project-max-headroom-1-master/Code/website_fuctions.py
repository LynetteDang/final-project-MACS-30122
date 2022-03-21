"""
Clean container for all website specific functions so as not to clutter up the
crawler
"""

import bs4
import Code.util as util
import Code.faculty_crawl as faculty_crawl

"""
Harris specific functions
"""


def harris_links(soup, url, limiting_domain):
    """
    fuction to pull link for next page to visit.

    Input:
        soup - soup - the full soup of the scraped page
        url - string - url of the scraped page
        limiting_domain - string - the url of the 'root' domain
    
    Output:
        linklst - list of strings - list of all valid urls for scraping
    """
    linklst = []

    links = soup.find("li", class_="pager__item pager__item--next")
    if links:
        # print(links)
        links = links.find("a")
        # print(links)
        temp_url = links.get("href")
        # print(temp_url)
        temp_url = faculty_crawl.url_management(url, temp_url)  # clean url
        # print(temp_url)
        if util.is_url_ok_to_follow(temp_url, limiting_domain):  # is valid?
            linklst.append(temp_url)

    return linklst


def harris_content(soup, url):
    """
    takes a page soup and pulls professor names and links

    Input:
        soup - soup - full page soup
        url - url of page visited

    Output:
        content - dict - a dictionary with professor name as key
            "Linked Page": the website on their directory page
            "Directory Page": the visited directory page (where this is
                scraping from)
            "Type of Employ": If specifically scrapable, faculty, staff, PhD 
                student, etc.
            "Position": the specific position information
            "School": which school is it SSD or Harris or other
            "University": will eventually be the university information

    """
    content = {}

    check = soup.find_all("div", class_="teaser-table--border clearfix")
    for person in check:
        if person:  # error check
            # stores professor name
            name_title_link = person.find(
                "div",
                class_="teaser-table--first-column col-directory-1 teaser-table-column-padding",
            )
            type_employ = (
                name_title_link.find("div", class_="teaser-table--profile-type")
                .text.strip()
                .lower()
            )
            # pulls faculty page url and name
            link = name_title_link.find("h2", class_="teaser-table--title")
            # name and page both in "a" href=
            link = link.find("a")
            # stores name
            name = link.text
            # stores link
            link = link.get("href")
            link = faculty_crawl.url_management(url, link)
            # stores position information
            position = (
                person.find(
                    "div",
                    class_="field field--name-field-job-title field--type-string field--label-hidden field__item",
                )
                .text.strip()
                .lower()
            )

        # stores professor name as key, faculty page = linked page
        # director page is visited page (scraped page)
        # University still a work in progress
        content[name] = {
            "Linked Page": link,
            "Directory Page": url,
            "Type of Employ": type_employ,
            "Position": position,
            "School": "Harris",
            "University": "No data this step",
        }
    return content


"""
Social Science Division website specific functions
"""


def ssd_links(soup, url, limiting_domain):
    """
    fuction to pull link for next page to visit.

    Input:
        soup - soup - the full soup of the scraped page
        url - string - url of the scraped page
        limiting_domain - string - the url of the 'root' domain
    
    Output:
        linklst - list of strings - list of all valid urls for scraping
    """
    linklst = []

    links = soup.find_all("div", class_="col-lg-9 col-md-6")

    for link in links:
        link = link.find("a")
        # Pulls link string
        temp_url = link.get("href")
        temp_url = faculty_crawl.url_management(url, temp_url)  # clean url
        if temp_url is None:  # error check, passes on None
            continue
        if util.is_url_ok_to_follow(temp_url, limiting_domain):  # is valid?
            linklst.append(temp_url)

    next_page = soup.find("li", class_="pager__item pager__item--next")
    if next_page is not None:
        next_page = next_page.find("a")
        next_page = next_page.get("href")
        next_page = faculty_crawl.url_management(url, next_page)  # clean url
        if util.is_url_ok_to_follow(next_page, limiting_domain):  # is valid?
            linklst.append(next_page)

    return linklst


def ssd_content(soup, url):
    """
    takes a page soup and pulls professor names and links

    Input:
        soup - soup - full page soup
        url - url of page visited

    Output:
        content - dict - a dictionary with professor name as key
            "Linked Page": the website on their directory page
            "Directory Page": the visited directory page (where this is
                scraping from)
            "Type of Employ": If specifically scrapable, faculty, staff, PhD 
                student, etc.
            "Position": the specific position information
            "School": which school is it SSD or Harris or other
            "University": will eventually be the university information
    """
    content = {}

    # pulls block with professor name and faculty page
    check = soup.find("div", class_="col-lg-9 col-md-8 faculty-text")

    if check is not None:  # error check
        # stores professor name
        name = check.find("h2").text
        # pulls position information
        position = (
            check.find("span", class_="university d-none d-md-block")
            .text.strip()
            .lower()
        )
        # SSD doesn't have this field
        type_employ = "SSD doesn't have this field"
        # pulls faculty page url
        link = check.find("a")
        if link is not None:
            link = link.get("href")
            # checks if useable url
            if util.is_url_ok_to_follow(link, None, False):
                true_link = link
            else:
                true_link = "No Link"

        else:
            true_link = "No Link"

        # stores professor name as key, faculty page = linked page
        # director page is visited page (scraped page)
        content[name] = {
            "Linked Page": true_link,
            "Directory Page": url,
            "Type of Employ": type_employ,
            "Position": position,
            "School": "SSD",
            "University": "No data this step",
        }

    return content
