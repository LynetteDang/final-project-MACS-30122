import json
import requests
import bs4
import re


def clean_education(education, name):
    old_edu = education
    education = education.replace("Ph.D.", "PhD")
    education = education.replace("Ph.D", "PhD")
    education = education.replace("doctorate", "PhD")
    education = education.replace("Doctorate", "PhD")
    education = education.replace("Doctorat d'Etat", "PhD")
    education = education.split("\n\t")
    if len(education) > 1 or len(education[0]) < 60:
        education = [edu for edu in education if 'PhD' in edu]
        if education:
            education = education[0]
            # pull out degree
            degree = 'PhD'
            year = re.findall('[0-9][0-9][0-9]*[0-9]*', education)
            if year:
                year = year[0]
            else:
                year = "n/a"
            school = re.findall(
                r"[A-Z][a-z]+\s*[A-Za-z]*\s*of\s[A-Za-z]+", education)
            if school:
                school = school[0]
            else:
                school = re.findall(
                    r"[A-Z][a-z]+\s[A-Za-z]*\s*University", education)
                if school:
                    school = school[0]
                else:
                    school = re.findall(
                        r"[A-Z]*\s*[a-z]*\s*[A-Z][a-z]+", education)
                    school = [s for s in school if s.split(
                        " ")[0] not in name and "Ph" not in s]
                    if school:
                        school = " ".join(school)
                    else:
                        school = re.findall(r"[A-Z][A-Z]+", education)
                        if school:
                            school = school[0]
            return (degree, school, year)
    else:
        return old_edu


def find_education_easy(url):
    """
    Pull out education information from a given faculty member URL

    inputs:
        url (str): url to visit
    Returns: doctorate education (str) for the faculty member
    """
    # search for any 'p' containing education data!!
    request = requests.get(url)
    soup = bs4.BeautifulSoup(request.text, "html.parser")
    poss_text = soup.find_all('p')
    # if data != None:
    #    poss_text = data.find_all('p')
    # else:
    #    poss_text = []
    education = [p.text for p in poss_text
                 if 'Ph.D' in p.text or 'Doctorat' in p.text
                 or 'PhD' in p.text or 'BA' in p.text
                 or 'MA' in p.text or 'MS' in p.text
                 or 'M.A' in p.text or 'M.S' in p.text
                 or 'BS' in p.text or "bachelor's" in p.text
                 or 'B.A' in p.text or 'B.S' in p.text
                 or "master's" in p.text or 'doctorate' in p.text]
    return education


def find_universities(faculty_data, filename):
    """
    Pull out links from faculty_sites and find universities

    Inputs: faculty_sites (dict)
    Returns: No return, creates json with new dict containing universities
    """
    # pull out and visit pages
    for name, data in faculty_data.items():
        if data['Linked Page'] != 'No Link':
            url = data['Linked Page']
            education = find_education_easy(url)
        # couldn't find from linked page
        if not education:
            url = data['Directory Page']
            education = find_education_easy(url)
        if education:
            # clean education
            faculty_data[name]['University'] = education[0]

    for name, data in faculty_data.items():
        edu = clean_education(data['University'], name)
        if isinstance(edu, tuple):
            faculty_data[name]['University'] = edu

    # write json file
    with open(f'data/{filename}.json', 'w') as f:
        f.write(json.dumps(faculty_data))
