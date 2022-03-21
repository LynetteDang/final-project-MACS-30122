import plotly.express as px
import pandas as pd
from matplotlib.pyplot import figure
import re
import matplotlib.pyplot as plt
import copy
# %matplotlib inline
from Code.helpers.analysis_util import extract_university, get_universities,\
    IVY, TOP_20, get_university, get_university_total, get_count


edu = pd.read_json("Code/data/faculty_edu_cleaned_partial.json").T

# to separate the dataframe into three:
# edu_cleaned contains professor's credentials we have managed to extract professor's credentials
# edu_missing contains professor's credentials we haven't been able to extract yet
# edu_cleanup contains professor's credentials we need to extract from paragraph
missing = []
have_info = []
more_cleanup = []
for loc, uni in enumerate(edu["University"]):
    if isinstance(uni, str):
        index = edu.index[loc]
        missing.append(index)
        if uni == "Still Working on This":
            more_cleanup.append(index)
    else:
        index = edu.index[loc]
        have_info.append(index)
edu_cleaned = edu.drop(missing)
edu_missing = edu.drop(have_info)
edu_cleanup = edu_missing.drop(more_cleanup)

credentials = list(edu_cleaned["University"])
universities = []
for uni in enumerate(edu_cleanup["University"]):
    universities.append(extract_university(uni[1]))
universities.append(get_universities(credentials, universities))
while("" in universities):
    universities.remove("")
universities = universities[:-1]

for index, row in edu_cleaned.iterrows():
    row['University'][1] = get_university(row['University'][1])
    row['University'] = row['University'][1]
edu_cleaned = edu_cleaned[edu_cleaned['University'] != "Still Working on This"]
edu_cleaned = edu_cleaned[edu_cleaned['University'] != 'Paul Staniland']
edu_cleaned = edu_cleaned[edu_cleaned['University']
                          != 'Department of Psychology']
edu_cleaned = edu_cleaned[edu_cleaned['University']
                          != "Arthur Professor of Political"]
edu_cleanup = edu_cleanup[edu_cleanup['University'] != '']
frames = [edu_cleaned, edu_cleanup]
# output to csv
edu_final = pd.concat(frames)
edu_final.to_csv('Code/data/edu_final.csv')

result = get_university_total(universities)
ivy_count = get_count(result, IVY)

result = pd.DataFrame(result, columns=['University', "Count of Professors"])
result.to_csv('Code/data/university_frequency.csv')

# Data Visualization
result10 = result.head(10)
fig = px.bar(result10, x='University', y='Count of Professors', range_y=[
             0, 45], title="Social Science Division -- Top 10 Institutions Professors Acquired Their PhD")
fig.show()

result_copy = copy.deepcopy(result)
result_copy.loc[result_copy['Count of Professors'] <
                11, 'University'] = 'Other Universities'
fig2 = px.pie(result_copy, values='Count of Professors', names='University',
              title="Social Science Division -- Top 5 Institutions VS Other Universities")
fig2.show()

result_copy_2 = copy.deepcopy(result)
list_ivy = []
for row in result_copy_2['University']:
    if row in IVY:
        list_ivy.append(True)
    else:
        list_ivy.append(False)
result_copy_2.loc[list_ivy, 'University'] = 'Ivy League'
result_copy_2.loc[result_copy_2['University'] != "Ivy League",
                  'University'] = 'Other Universities'
fig3 = px.pie(result_copy_2, values='Count of Professors', names='University',
              title="Social Science Division -- Ivy League VS Other Universities")
fig3.show()

result_copy_3 = copy.deepcopy(result)
list_foreign = []
for row in result_copy_3['University']:
    if row == "University of Franche" or row == "University of Campinas"\
            or row == "University of London" or row == "University of Tokyo"\
            or row == "Oxford University" or row == "McGill University"\
            or row == "University of Paris" or row == "University of Vienna"\
            or row == "University of Cambridge" \
            or row == "Leiden University" \
            or row == "Australian National University":
        list_foreign.append(True)
    else:
        list_foreign.append(False)
result_copy_3.loc[list_foreign, 'University'] = 'Foreign Universities'
result_copy_3.loc[result_copy_3['University'] != 'Foreign Universities',
                  'University'] = 'American Universities'
fig4 = px.pie(result_copy_3, values='Count of Professors', names='University',
              title="Social Science Division -- Foreign Universities VS American Universities")
fig4.show()

result_copy_4 = copy.deepcopy(result)
list_top20 = []
for row in result_copy_4['University']:
    if row in TOP_20:
        list_top20.append(True)
    else:
        list_top20.append(False)
result_copy_4.loc[list_top20, 'University'] = 'Top-20 Ranked Institutions'
result_copy_4.loc[result_copy_4['University'] != 'Top-20 Ranked Institutions',
                  'University'] = 'Other Institutions'
fig5 = px.pie(result_copy_4, values='Count of Professors',
              names='University', title="Social Science Division -- Top-20 Ranked Institutions VS Other Institutions (Global)")
fig5.show()
