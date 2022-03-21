import plotly.express as px
import pandas as pd
from matplotlib.pyplot import figure
import re
import matplotlib.pyplot as plt
import copy
# %matplotlib inline

# Extract ivy league schools
IVY = ["Brown University", "Columbia University",
       "Cornell University", "Dartmouth College",
       "Harvard University", "Princeton University",
       "University of Pennsylvania", "Yale University"]

# Extract top 20 schools
world_rank = pd.read_csv("Code/data/world_ranking.csv")
top_20 = list(world_rank[:20]['institution'])
for index, uni in enumerate(top_20):
    if "University of California" in uni:
        top_20[index] = "University of California"
TOP_20 = top_20


def extract_university(description):
    '''
    From a paragraph of description (string), extract the institution one has
    earned their phD from
    Input:
        description- string - description of one's educational background

    Output:
        match - the name of the institution one has earned their phD from
        if there is no match, return empty string
    '''
    phd_patterns = ['[A-Za-z,"\- ]+Ph\.D[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+Ph\.D.[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+PhD[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+P.h.D[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+phd[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+doctorate[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+doctoral degree[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+Doctorate[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+Juris Doctor[A-Za-z,"\- ]+',
                    '[A-Za-z,"\- ]+Doctorat d\'Etat[A-Za-z,"\- ]+']
    phd_pattern = '({})'.format('|'.join(phd_patterns))
    matches = re.findall(phd_pattern, description)
    if matches:
        sentence_phd = matches[0]
        university_patterns = ['[A-Z][a-z]* University',
                               'University of [A-Z][a-z]*',
                               '[A-Z][a-z]* Institute',
                               '[A-Z][a-z]* Institute of [A-Z][a-z]*']
        university_pattern = '({})'.format('|'.join(university_patterns))
        match = re.findall(university_pattern, sentence_phd)
        if match:
            match = match[0]
            return match
    return ''


def get_universities(credentials, universities):
    '''
    For each of professors that we have acquired credentials for, extract
    the institution they have earned their phD from

    Input:
        credentials- list of list - list of [degree, university, year] for each
        professor

    Output:
        universities - list - list of universities, with duplicates
    '''
    for degree, university, year in credentials:
        if university == "MIT":
            university = 'Massachusetts Institute of Technology'
        if university == 'D Chicago':
            university = "University of Chicago"
        if university == "D Michigan":
            university = "University of Michigan"
        if university == "D California" or "UC " in university:
            university = 'University of California'
        if "Harvard" in university:
            university = 'Harvard University'
        if "Stanford" in university:
            university = 'Stanford University'
        if "Gill" in university:
            university = 'McGill University'
        if university:
            universities.append(university)
    return universities


def get_university(university):
    '''
    For each of professors that we have acquired credentials for, extract
    and clean up the name of the institution

    Input:
        university - the university professor gets his/her phD degree from

    Output:
        university - the cleaned-up/formatted name of the university
    '''
    if university == "MIT":
        university = 'Massachusetts Institute of Technology'
    if university == 'D Chicago':
        university = "University of Chicago"
    if university == "D Michigan":
        university = "University of Michigan"
    if university == "D California" or "UC " in university:
        university = 'University of California'
    if "Harvard" in university:
        university = 'Harvard University'
    if "Stanford" in university:
        university = 'Stanford University'
    if "Paul" in university or "Professor" in university:
        university = "Still Working on This"
    if "City University" in university:
        university = "City University of New York"
    if university == 'University of North':
        university = 'University of North Carolina'
    return university


def get_university_total(universities):
    '''
    Get the total amount of professors graduated from eachuniversities, store
    in a list of tuples (university, count) in descending order of count

    Input:
        universities - list - list of universities professor have earned their
        phD from

    Output:
        result - list of tuples - a list of tuples (university, count)
        in descending order of count
    '''
    result = {}
    for uni in universities:
        if uni:
            result[uni] = result.get(uni, 0) + 1
    result = sorted(result.items(), key=lambda x: x[1], reverse=True)
    for i, v in enumerate(result):
        if v[0] == 'Paul Staniland' or v[0] == 'Department of Psychology' or v[0] == "Arthur Professor of Political" or v[0] == "State University":
            result.pop(i)
    return result


def get_count(result, list_of_schools):
    '''
    Get the total count of a given list of schools (eg: ivy leagues, top 20)

    Input:
        result - list of tuples - a list of tuples (university, count)
        in descending order of count
        list_of_schools - list (constant) - a given list of schools

    Output:
        count - total count of a given list of schools (eg: ivy leagues, top 20)
    '''
    count = 0
    for r in result:
        if r[0] in list_of_schools:
            count = count + r[1]
    return count
