import json
import pandas as pd


# import graph-tool network package
from graph_tool.all import *
import json
import pandas as pd
g = collection.data["celegansneural"]
state = minimize_nested_blockmodel_dl(g)


from demographicx import GenderEstimator
from demographicx import EthnicityEstimator


def infer_gender_race(df):
    """
    Use a Python package for gender and race/ethnicity estimation based on BERT
    subword tokenization and embedding: https://github.com/sciosci/demographicx
    
    Input: 
      df: dataframe of faculty data ('harris_final.csv' 
    or 'edu_final.csv')
    
    Return a dataframe with 4 new columns: 'Gender Estimates', 
      'Predicted Gender', 'Ethnicity Estimates', 'Predicted Ethnicity'.
    """
    df.rename(columns={"Unnamed: 0": "Faculty Name"}, inplace=True)
    
    # estimate gender
    gender_estimator = GenderEstimator()
    df['Gender Estimates'] = df['Faculty Name'].apply(\
        lambda x: gender_estimator.predict(x))
    df['Predicted Gender'] = df['Gender Estimates'].apply(\
        lambda x: get_max_values(x))
    
    # estimate ethnicity
    ethnicity_estimator = EthnicityEstimator()
    df['Ethnicity Estimates'] = df['Faculty Name'].apply(\
        lambda x: ethnicity_estimator.predict(x))
    df['Predicted Ethnicity'] = df['Ethnicity Estimates'].apply(\
        lambda x: get_max_values(x))
    
    return df


def get_max_values(dic):
    """
    A helper function to extract the maximum value from a dictionary 
    of prediction results.
    Return the key of the maxiumum value in a dictionary.
    """
    if 'unknown' in dic:
        del dic['unknown']
    max_value = max(dic.values())
    max_key = [k for k, v in dic.items() if v == max_value]
    return max_key[0]


def link_university_ranking(df, ranking_filename):
    """
    Link faculty dataframe with university ranking.
    
    Input: 
      df: a faculty dataframe from social science division or harris
      ranking_filename: name of the csv file storing university ranking data
    
    Return a tuple, the first item is a dataframe, with each row index 
      being a university, one column "Number of Faculty" and another column
      "Ranking"; the second item is a list of university row index 
      where linkage fails and university ranking is stored as None.
    """
    ranking = pd.read_csv(ranking_filename)
    
    # build a dictionary that maps university name to world rank
    uni_rank_dict = {}
    for i, row in ranking.iterrows():
        uni = row['institution']
        uni_rank_dict[uni] = row['world_rank']
    
    # build a dictionary that maps university to faculty counts
    uni_counts = {}
    for uni in df['University']:
        if not uni in uni_counts.keys():
            uni_counts[uni] = 1
        else:
            uni_counts[uni]+=1
    
    uni_rank = pd.DataFrame.from_dict(uni_counts, 
                                      orient='index', 
                                      columns=['Number of Faculty'])
    ranks_col = []
    error = []
    for index in uni_rank.index:
        try:
            ranks_col.append(uni_rank_dict[index])
        except:
            ranks_col.append(None)
            error.append(index)
            
    uni_rank['Ranking'] = ranks_col    
    return uni_rank, error


def add_faculty_lst(df, uni_rank):
    """
    Add a list of faculty names and row index to the uni_rank dataframe
    for further network analysis.
    Input:
      df: a faculty dataframe from social science division or harris
      uni_rank: a dataframe, with each row index being a university, 
      one column "Number of Faculty" and another column "Ranking."
    
    Return the modified uni_rank dataframe with two new columns: 'Index List'
      'Faculty List'.
    """
       
    faculty_name_lsts = []
    index_lsts = []
    for index in uni_rank.index:
        name_lst = []
        index_lst = []
        for i, row in df.iterrows():
            if row['University'] == index:
                name_lst.append(row['Faculty Name'])
                index_lst.append(i)
        faculty_name_lsts.append(name_lst)
        index_lsts.append(index_lst)
    
    uni_rank['Index List'] = index_lsts
    uni_rank['Faculty List'] = faculty_name_lsts
    
    return uni_rank
        

def get_faculty_neworks(df, uni_rank, gender=False, race=False):
    """
    Produce a network graph of faculty clustered by unversity they 
    graduate from. Each node represents a faculty; if they graduate from the
    same university, we link them with one edge.
    
    Input:
      df: a faculty dataframe from social science division or harris
      uni_rank: a dataframe, with each row index being a university, 
      one column "Number of Faculty" and another column "Ranking."
      gender: a boolean value of whether nodes will be colored 
        based on faculty gender
      race: a boolean value of whether nodes will be colored 
        based on faculty race
    """
    # change data type ready for future analysis
    uni_rank['Number of Faculty'] = uni_rank['Number of Faculty'].astype('int')
    uni_rank['Ranking'] = uni_rank['Ranking'].astype('int')
    
    g = Graph(directed=False)
    v_rank = g.new_vertex_property('int')
    v_name = g.new_vertex_property('string')
    v_index = g.new_vertex_property('int')
    v_gender = g.new_vertex_property('string')
    v_race = g.new_vertex_property('string')
    g.vertex_properties["rank"] = v_rank
    g.vertex_properties["name"] = v_name
    g.vertex_properties["index"] = v_index
    g.vertex_properties["gender"] = v_gender
    g.vertex_properties["race"] = v_race
    
    # create color codes
    genders = {'male': 1, 'female': 0}
    ethnics = {'white': 1, 'black': 0, 'asian': 0.75, 'hispanic': 0.25}
    
    # loop over every university
    for i, row in uni_rank.iloc[1:, :].iterrows():
      # loop over every faculty graduate from the same university
      for index in row['Index List']:
        # every faculty is a vertex
        v = g.add_vertex()
        g.vp.rank[v] = - row['Ranking']
        g.vp.name[v] = df['Faculty Name'][index]
        g.vp.index[v] = index
        g.vp.gender[v] = genders[df['Predicted Gender'][index]]
        g.vp.race[v] = ethnics[df['Predicted Ethnicity'][index]]
        
    
    # if faculty graduate from the same university, we link them with one edge
    for v1 in g.vertices():
        for v2 in g.vertices():
            if (g.vp.rank[v1] == g.vp.rank[v2] 
                and g.vp.index[v1] < g.vp.index[v2]):
                  e = g.add_edge(v1, v2)
                    
                    
    pos = graph_tool.draw.sfdp_layout(g)
    rank = graph_tool.draw.prop_to_size(g.vertex_properties['rank'])
    deg = g.degree_property_map("total")
    control = g.new_edge_property("vector<double>")

    # display the graph
    # original graph
    if not race and not gender:
        graph_draw(g, pos=pos, vertex_size=rank, 
                   vertex_fill_color=rank, vorder=rank,
                   vertex_text_position=0.5, vertex_text=g.vp.name,
                   edge_color=[0.19, 0.203,0.110, 0.6], 
                   edge_pen_width=0.5, fit_view=0.75,
                   fit_view_ink=True,adjust_aspect=True, output_size=(700,700),
                   edge_control_points=control, nodesfirst=True);
        
    if gender:
        gender= g.vertex_properties['gender']
        # color spectrum: white -> men; black -> women
        graph_draw(g, pos=pos, vertex_size=rank, 
               vertex_fill_color=gender, vorder=rank,
               vertex_text_position=0.5, vertex_text=g.vp.name,
               edge_color=[0.19, 0.203,0.110, 0.6], 
               edge_pen_width=0.5, fit_view=0.75,
               fit_view_ink=True, output_size=(700,700),nodesfirst=False);
        
    if race:
        race= g.vertex_properties['race']
        control = g.new_edge_property("vector<double>")
        # color spectrum: white -> asian -> hispanic -> black
        graph_draw(g, pos=pos, vertex_size=rank, 
                   vertex_fill_color=race, vorder=rank,
                    vertex_text_position=0.5, vertex_text=g.vp.name,
                   edge_color=[0.19, 0.203,0.110, 0.6], 
                   edge_pen_width=0.5, fit_view=0.75,
                   fit_view_ink=True, output_size=(700,700),nodesfirst=False);