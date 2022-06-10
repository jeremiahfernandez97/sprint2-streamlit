
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import folium
from streamlit_folium import folium_static
from PIL import Image
import geopandas as gpd
import warnings
warnings.filterwarnings('ignore')

st.sidebar.title("STOP VAW NOW!")

st.sidebar.write('')
st.sidebar.write('')

st.sidebar.title("The Team")
st.sidebar.write('Gelo')
st.sidebar.write('Jac')
st.sidebar.write('Rocelle')

st.sidebar.write('')
st.sidebar.write('')

df = pd.read_csv("data/PH-HRIR-merged.csv")
df_1 = pd.read_csv("data/experienced_DV.csv")
province_df = pd.read_csv('data/province_df.csv')
my_page = st.sidebar.radio('Violence Against Women (VAW) in the Philippines', ['Dataset', 'Prevailence of VAW', 'VAW Interactive Regional Map', 'Clusters', 'Insights', 'Recommendations'])





if my_page == 'Dataset':
    st.title("Reference Data")
    st.header("2017 Philippines Standard DHS Dataset")
    st.caption("Processing:")
    st.caption("- No Processing Required")
    if st.checkbox('Show Reference Data', value = False):
        data_load_state = st.text('Loading data...')
        st.write(df.head(300))
        data_load_state.markdown('Loading data...**done!**')
        
    st.title("Processed Data")
    st.header("Women who Answered Violence-Related Questionnaire")
    st.caption("Processing:")
    st.caption(" - Removed respondents who did not answer if they experienced emotional, physical, and sexual violence")
    st.caption(" - Replaced values 'Yes' to 1 and 'No' to 0 to these columns related to violence" )
    st.caption(" - Added one column for the sum of these columns related to violence")
    if st.checkbox('Show Processed Data', value = False):
        data_load_state = st.text('Loading data...')
        st.write(df_1.head(300))
        data_load_state.markdown('Loading data...**done!**')
 


        
elif my_page == 'Prevailence of VAW':
    st.title("Prevailence of Violence Against Women in the Philippines")
    st.caption("Highest Prevailence: 57.66% in Camarines Norte (Darkest Orange)")
    st.caption("Lowest Prevailence: 00.41% in Lanao Del Sur (Lightest Orange)")
    
    if st.checkbox('Show Data', value = False):
        data_load_state = st.text('Loading data...')
        st.write(province_df.head(300))
        data_load_state.markdown('Loading data...**done!**')
    
    merged_data2 = gpd.read_file("data/geo/sprint1-map-cleaned2.shp")
   
    variable = 'pct_exp_re'
    vmin, vmax = merged_data2[variable].min(), merged_data2[variable].max()
    fig, ax = plt.subplots(1, figsize=(15, 10))
    merged_data2.plot(column=variable, cmap='Oranges', linewidth=0.8, ax=ax, edgecolor='0.8', vmin=vmin, vmax=vmax)
    plt.xlim(115,130)
    plt.ylim(0,25)
    plt.title('Prevailence of Violence against Women Per Province', fontsize = 18)
    sm = plt.cm.ScalarMappable(cmap='Oranges', norm=plt.Normalize(vmin=vmin, vmax=vmax))
    cbar = fig.colorbar(sm)
    st.pyplot(fig)
    
    
    
    
    
elif my_page == 'VAW Interactive Regional Map':
    st.title("Interactive Regional Map")
    st.header("Number of Women Experiencing Violence Based on DHS Data 2017")
    st.header("")
    st.caption("Instructions:")
    st.caption("1. Select Region from Left Pane")
    st.caption("2. Zoom in to desired location")
    st.header("")
    shapefile = gpd.read_file('data/geo/cluster_centers.shp')
    shapefile["x"] = shapefile.geometry.centroid.x
    shapefile["y"] = shapefile.geometry.centroid.y
    map_center = [8.508, 128.476]

    # Styling the map
    mymap = folium.Map(location=map_center, height=700, width=1000, tiles="OpenStreetMap", zoom_start=5.4)
    from folium.plugins import MarkerCluster
    marker_cluster = MarkerCluster().add_to(mymap)
    
    option_reg = st.sidebar.selectbox(
        'Select Region',
        shapefile["DHSREGNA"].unique())
    
    'You selected: ', option_reg
    
    reg = option_reg
    df_reg = shapefile[shapefile["DHSREGNA"]==reg]

    for i in np.arange(len(df_reg)):
        lat = df_reg["y"].values[i]
        lon = df_reg["x"].values[i]
        name = df_reg["emo_phy_se"].values[i]
        folium.Marker([lat, lon], popup=name).add_to(marker_cluster)
    folium_static(mymap)
      
    
    
    
    
    
elif my_page == 'Clusters':
    st.title("Clusters for Violence Against Women")
    st.caption("Factors for Clustering:")
    st.caption("1. Domestic Violence")
    st.caption("2. Justification of Domestic Violence")
    st.caption("3. Wealth Index")
    st.caption("4. Educational Attainment")
    img = Image.open("clusters.png")
    st.image(img)
    
    st.title("Cluster Description")
    st.header("Vulnerable")
    st.caption(" 1. 79.6% of the cluster come from the poorer to the poorest of wealth indices and  49.1% only finished secondary education at most. ")
    st.caption(" 2. Group with the most instances of severe physical violence and sexual violence.")
    st.caption(" 3. 35.4% of respondents come from the highest cases of GBV (Caraga, Bicol, Eastern Visayas)")
    img = Image.open("vulnerable.png")
    st.image(img)
    
    st.caption("")

    st.header("Unaware")
    st.caption(" 1. Those who justify GBV don’t necessarily have to be victims themselves. ")
    st.caption(" 2. 12% have experienced some form of domestic violence in their life.")
    st.caption(" 3. Like the vulnerable cluster, majority come from poverty(74%) and unfinished education (50.5%)")
    st.caption(" 4. Interestingly, 28% of respondents are from ARMM")
    img = Image.open("vulnerable.png")
    st.image(img)
    
    st.caption("")

    st.header("Protected")
    st.caption(" 1. Wealth is still a big shield against forms of GBV. 69.2% are from the richer to richest of wealth indices. ")
    st.caption(" 2. Only 5.3% have experienced some form of domestic violence in their life.")
    st.caption(" 3. Most of the experiences stem from emotional violence and less than 1% for physical and sexual")
    img = Image.open("protected.png")
    st.image(img)
    
    st.caption("")

    st.header("Informed")
    st.caption(" 1. All in this cluster come from poorest to middle wealth indices. ")
    st.caption(" 2. Not necessarily finished education. Only 33.5% finished higher education.")
    st.caption(" 3. Interestingly, a large percentage, 31.4, come from NCR and Central Luzon ")
    st.caption(" 4. Most common form is emotional violence ")
    img = Image.open("informed.png")
    st.image(img)
    
    
    
elif my_page == 'Insights':
    st.title("Insights found in the Analysis of Violence in the Pihlippines")
    
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    
    st.header("Insights: Around 68.8% Women are aware with the available protection programs in our country.")
    img = Image.open("insight1.png")
    st.image(img)

    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    
    st.header("Where are they located?")
    st.header("Insights: Most of the women who are aware with the protection programs are located at Western Visayas, CARAGA, Davao, Eastern Visayas.")
    img = Image.open("insight2.png")
    st.image(img)
    
    st.caption("")
    st.caption("")
    st.caption("")
    st.caption("")
    
    st.header("What are the common programs?")
    st.header("Insights: Most of the women who are aware with the protection programs are located at Western Visayas, CARAGA, Davao, Eastern Visayas.")
    img = Image.open("insight3.png")
    st.image(img)
    
    
elif my_page == 'Recommendations':
    st.title("Recommendations")
    st.header("1. Target areas (i.e., provincial, regional) with high cases of gender based violence")
    st.header("2. Build on programs that involve both men and women")
    st.header("3. Increase awareness of protection programs and communities for cure and prevention")
    
    

    
    