# from collections import namedtuple
# import altair as alt
# import math
# import pandas as pd
# import streamlit as st

# """
# # Welcome to Streamlit!

# Edit `/streamlit_app.py` to customize this app to your heart's desire :heart:

# If you have any questions, checkout our [documentation](https://docs.streamlit.io) and [community
# forums](https://discuss.streamlit.io).

# In the meantime, below is an example of what you can do with just a few lines of code:
# """


# with st.echo(code_location='below'):
#     total_points = st.slider("Number of points in spiral", 1, 5000, 2000)
#     num_turns = st.slider("Number of turns in spiral", 1, 100, 9)

#     Point = namedtuple('Point', 'x y')
#     data = []

#     points_per_turn = total_points / num_turns

#     for curr_point_num in range(total_points):
#         curr_turn, i = divmod(curr_point_num, points_per_turn)
#         angle = (curr_turn + 1) * 2 * math.pi * i / points_per_turn
#         radius = curr_point_num / total_points
#         x = radius * math.cos(angle)
#         y = radius * math.sin(angle)
#         data.append(Point(x, y))

#     st.altair_chart(alt.Chart(pd.DataFrame(data), height=500, width=500)
#         .mark_circle(color='#0068c9', opacity=0.5)
#         .encode(x='x:Q', y='y:Q'))


import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import networkx as nx
from pyvis.network import Network

# Read dataset (CSV)
df_interact = pd.read_csv('data/processed_drug_interactions.csv')

# Set header title
st.title('Network Graph Visualization of Drug-Drug Interactions')

# Define list of selection options and sort alphabetically
drug_list = ['Metformin', 'Glipizide', 'Lisinopril', 'Simvastatin',
            'Warfarin', 'Aspirin', 'Losartan', 'Ibuprofen']
drug_list.sort()

# Implement multiselect dropdown menu for option selection (returns a list)
selected_drugs = st.multiselect('Select drug(s) to visualize', drug_list)

# Set info message on initial site load
if len(selected_drugs) == 0:
    st.text('Choose at least 1 drug to get started')

# Create network graph when user selects >= 1 item
else:
    df_select = df_interact.loc[df_interact['drug_1_name'].isin(selected_drugs) | \
                                df_interact['drug_2_name'].isin(selected_drugs)]
    df_select = df_select.reset_index(drop=True)

    # Create networkx graph object from pandas dataframe
    G = nx.from_pandas_edgelist(df_select, 'drug_1_name', 'drug_2_name', 'weight')

    # Initiate PyVis network object
    drug_net = Network(height='465px', bgcolor='#222222', font_color='white')

    # Take Networkx graph and translate it to a PyVis graph format
    drug_net.from_nx(G)

    # Generate network with specific layout settings
    drug_net.repulsion(node_distance=420, central_gravity=0.33,
                       spring_length=110, spring_strength=0.10,
                       damping=0.95)

    # Save and read graph as HTML file (on Streamlit Sharing)
    try:
        path = '/tmp'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Save and read graph as HTML file (locally)
    except:
        path = '/html_files'
        drug_net.save_graph(f'{path}/pyvis_graph.html')
        HtmlFile = open(f'{path}/pyvis_graph.html', 'r', encoding='utf-8')

    # Load HTML file in HTML component for display on Streamlit page
    components.html(HtmlFile.read(), height=435)

    