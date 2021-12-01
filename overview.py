from __future__ import annotations

import streamlit as st
import altair as alt
from PIL import Image
import pandas as pd
import numpy as np

# SETTING PAGE CONFIG TO WIDE MODE
# st.set_page_config(layout="wide")

########## map related methods #########
@st.cache(persist=True)
def load_and_clean_sites_data():
  raw_sites_df = pd.read_csv(
      "EDA/Adelie Sites.csv",
      engine='python'
  )
  sites_df = raw_sites_df.copy()
  sites_df = sites_df[~sites_df['site name'].isnull()]
  sites_df = sites_df[~sites_df['longitude EPSG:4326'].isnull()]
  sites_df = sites_df[~sites_df['latitude EPSG:4326'].isnull()]
  sites_df['Longitude'] = raw_sites_df['longitude EPSG:4326']
  sites_df['Latitude'] = raw_sites_df['latitude EPSG:4326']
  sites_df['Count'] = raw_sites_df.groupby('site name')["site name"].count().reset_index(name="Count")['Count']

  # For coloring the 5 target islands 
  focus_sites = ['Chirstine Island', 'Humble Island', 'Torgersen Island', 'Litchfield Island', 'Cormorant Island']
  def f(row):
    if row['site name'] in focus_sites:
      val = 1
    else:
      val = 0
    return val
  sites_df['Focus'] = sites_df.apply(f, axis=1)
  
  return sites_df

def load_sites_map():
  sites_df = load_and_clean_sites_data()

  map_source = alt.topo_feature(
    'https://raw.githubusercontent.com/jazlyn5/hosting_data/master/ata_map.topojson',
    'collection'
  )

  base = alt.Chart(map_source).mark_geoshape(
      fill='lightgray',
      stroke='white'
    )# .project(type='transverseMercator')

  points = alt.Chart(sites_df).mark_circle(
  ).encode(
      longitude='Longitude:Q',
      latitude='Latitude:Q',
      size=alt.value(80),
      tooltip='site name',
      # color=alt.condition(brush, 'Count:N', alt.value('lightgray'))
  ).project(
      type="transverseMercator",
  ).properties(
      width=400,
      height=300
  )
  st.altair_chart(base + points, use_container_width=True)

########## main program ##########
def overview():
  ice_float_image = Image.open("images/adelie_penguins_ice_float.jpg")
  width, height = ice_float_image.size 
  cropped_area = (0, 200, width, height - 250)
  cropped_img = ice_float_image.crop(cropped_area)
  st.image(cropped_img, "Adelie penguins congregating on an ice floe")

  row1_1, row1_2 = st.columns((2, 1))
  with row1_1:
    intro = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
    Introduction
    </b>
    <br><br>
    """
    st.markdown(intro, unsafe_allow_html=True)
    description = """
      <body style="font-family:Charter; color:Black; font-size: 18px;">
      Adélie penguin is a species of penguins characterized by black and white 
      plumage, with feathers covering the head, throat, back and tail; and one 
      distinguishing feature of Adélie penguin is a small ring of white feathers surrouding each eye.
      On the other hand, the feathers of Adélie penguin chicks range from light gray to dark black.
      </body>
    """
    st.markdown(
      description, unsafe_allow_html=True
    )
    
    phys_description = """
      <p style="font-family:Charter; color:Black; font-size: 18px;">
      <br>
      <b>Physical Features</b>
      <br>
      The Adélie is the littlest species of penguin in the Antarctic.
      Adult Adélie penguins stand 70–73 cm (about 28–29 inches) tall and weigh 4–6 kg (about 9–13 pounds), 
      the males being slightly taller and heavier than the females. Adelie fledgings weigh about 2.8-3.2kg.  
      </p>
    """
    st.markdown(
      phys_description, unsafe_allow_html=True
    )
    # fledging weight source is our EDA and https://www.researchgate.net/publication/227193539_Factors_affecting_fledging_weight_of_Adelie_penguin_Pygoscelis_adeliae_chicks_a_modeling_study
    # other facts: https://www.britannica.com/animal/Adelie-penguin

  with row1_2:
    adult_and_chick = Image.open("images/adult_and_chick.jpg")
    width, height = adult_and_chick.size 
    cropped_area = (90, 0, width - 90, height)
    cropped_img = adult_and_chick.crop(cropped_area)
    st.image(cropped_img) 

  # Fun fact about its name
  # The Adélie penguin got its name from the French Antarctic explorer, Jules Dumont d'Urville. 
  # On discovering these sea birds in 1840 he decided to name them after his beloved wife – Adéle. 
  # The scientific name for the Adélie penguin is Pygoscelis adeliae. Pygoscelis means ‘rump-legged’, 
  # but the genus is better known as 'brush-tailed penguins'.
  
  row2_1, row2_2 = st.columns((2, 3))
  with row2_1:
    load_sites_map()

  with row2_2:
    habitat_description = """
      <p style="font-family:Charter; color:Black; font-size: 18px;">
      <b>Habitat</b>
      <br>
      There are a total of 18 different species of penguin in the world. 
      However, only two species truly make the Antarctic their home by living and breeding 
      there – the Emperor penguin and – yes you guessed it – the Adélie penguin.
      They are common along the entire coast of Antarctica, and during the warmer months 
      Adélie penguins are found primarily in several breeding colonies along rocky, ice-free coasts.
      <br>
      Studies have shown that colonies have declined on the Antarctic Peninsula since the early 1980s, 
      however East Antarctica have seen increases in population in the recent years.
      </p>
    """
    st.markdown(
      habitat_description, unsafe_allow_html=True
    )
    # declining text source: https://en.wikipedia.org/wiki/Adélie_penguin#Distribution_and_habitat
  
  row3_1, row3_2, row3_3, row3_4 = st.columns((3, 1, 1, 1))
  with row3_1:
    diet_description = """
    <p style="font-family:Charter; color:Black; font-size: 18px;">
    <b>Diet</b>
    <br>
    The Adélie penguin is known to feed mainly on: Antarctic krill, ice krill, Antarctic silverfish, 
    sea krill and glacial squid (diet varies depending on geographic location) during the chick-rearing season. 
    There have been studies that show that salp can also take up to 1/3 of an Adélie penguin's diet at times.
    </p>
    """
    # salp reference: https://www.scimex.org/newsfeed/learning-about-penguins-diet-may-save-marine-life,-study-finds2
    st.markdown(
      diet_description, unsafe_allow_html=True
    )
  with row3_2:
    krill = Image.open("images/krill.jpg")
    st.image(krill, "Antarctic Krill")

  with row3_3:
    silver_fish = Image.open("images/silver_fish.jpg")
    st.image(silver_fish, "Antarctic Silverfish School (photo by Simonepietro Canese)")

  with row3_4:
    salp = Image.open("images/salp.png")
    width, height = salp.size
    print(width, height)
    cropped_area = (0, 30, width, height-30)
    cropped_img = salp.crop(cropped_area)
    st.image(cropped_img, "Salp")

# overview()