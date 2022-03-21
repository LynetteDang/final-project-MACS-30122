import plotly.express as px
import pandas as pd
from matplotlib.pyplot import figure
import re
import matplotlib.pyplot as plt
import copy
# %matplotlib inline
from Code.helpers.analysis_util import extract_university, get_universities,\
    IVY, TOP_20, get_university, get_university_total, get_count

edu = pd.read_json("Code/data/harris_faculty_edu_cleaned_partial.json").T

# to separate the dataframe into three:
# edu_cleaned contains professor's credentials we have managed to extract professor's credentials
# edu_missing contains professor's credentials we haven't been able to extract yet
# edu_cleanup contains professor's credentials we need to extract from paragraph

edu_cleanup_lecturer = edu[edu['Type of Employ'] == "lecturer"]
edu_cleanup_faculty = edu[edu['Type of Employ'] == "faculty"]

frames = [edu_cleanup_lecturer, edu_cleanup_faculty]
edu_cleanup = pd.concat(frames)

for index, row in edu_cleanup.iterrows():
    row['University'] = extract_university(row['University'])
edu_cleanup = edu_cleanup[edu_cleanup['University'] != '']
edu_cleanup = edu_cleanup[edu_cleanup['University'] != 'State University']
edu_cleanup.to_csv('Code/data/harris_final.csv')
universities = []
for uni in enumerate(edu_cleanup["University"]):
    universities.append(get_university(uni[1]))
result = get_university_total(universities)
ivy_count = get_count(result, IVY)

result = pd.DataFrame(result, columns=['University', "Count of Professors"])
result.to_csv('Code/data/harris_university_frequency.csv')

# Data Visualization
result_top = result[:5]
fig = px.bar(result_top, x='University', y='Count of Professors', range_y=[0, 10],
             title="Harris -- Top 5 Institutions Professors Acquired Their PhD (With Ties)")
fig.show()

result_copy = copy.deepcopy(result)
result_copy.loc[result_copy['Count of Professors'] <
                3, 'University'] = 'Other Universities'
fig2 = px.pie(result_copy, values='Count of Professors', names='University',
              title="Harris -- Top 5 Institutions (With Ties) VS Other Universities")
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
fig3 = px.pie(result_copy_2, values='Count of Professors',
              names='University', title="Harris -- Ivy League VS Other Universities")
fig3.show()

result_copy_3 = copy.deepcopy(result)
list_foreign = []
for row in result_copy_3['University']:
    if row == "University of Toronto" or row == "Keio University" or \
            row == 'University of Wales' or row == 'York University' or \
        row == 'European University' or row == "Kyoto University" \
            or row == 'Peking University':
        list_foreign.append(True)
    else:
        list_foreign.append(False)
result_copy_3.loc[list_foreign, 'University'] = 'Foreign Universities'
result_copy_3.loc[result_copy_3['University'] != 'Foreign Universities',
                  'University'] = 'American Universities'
fig4 = px.pie(result_copy_3, values='Count of Professors', names='University',
              title="Harris -- Foreign Universities VS American Universities")
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
              names='University', title="Harris -- Top-20 Ranked Institutions VS Other Institutions (Global)")
fig5.show()
