from __future__ import annotations
from os import truncate

from numpy.lib.npyio import load

import streamlit as st
import altair as alt
from vega_datasets import data

import math
import datetime
import pandas as pd
import numpy as np
import geopandas as gpd
import pydeck as pdk
from pydeck.types import String

########### Utils ###########
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

@st.cache(persist=True)
def load_and_clean_zooplankton_data():
  raw_z_df = pd.read_csv("EDA/Zooplankton Abundances.csv", engine="python")
  # Processing column
  z_df = raw_z_df.copy()

  z_df['Year'] = pd.to_datetime(z_df['col_2631'], format='%Y')
  z_df['Latitude'] = z_df['col_2635']
  z_df['latitude'] = z_df['Latitude']
  z_df['Longitude'] = z_df['col_2636']
  z_df['longitude'] = z_df['Longitude']
  z_df['Krill'] = z_df['col_2637']
  z_df['Salp'] = z_df['col_2638']
  z_df['Thy'] = z_df['col_2639']
  z_df['Limacina'] = z_df['col_2640']
  z_df['Ecrystallorophias'] = z_df['col_2641']

  z_df['Krill'] = z_df['Krill'].clip(lower=0)
  z_df['Salp'] = z_df['Salp'].clip(lower=0)
  z_df['Thy'] = z_df['Thy'].clip(lower=0)
  z_df['Limacina'] = z_df['Limacina'].clip(lower=0)
  z_df['Ecrystallorophias'] = z_df['Ecrystallorophias'].clip(lower=0)
  z_df['Total Food'] = z_df['Krill'] + z_df['Salp'] + z_df['Thy'] + z_df['Limacina'] + z_df['Ecrystallorophias']

  # Limacina: sea snail babies, on penguin diet: https://en.wikipedia.org/wiki/Sea_butterfly
  # E crystallorophias: antarctic costal krill: https://en.wikipedia.org/wiki/Euphausia_crystallorophias
  # Thysanoessa, a genre of krill: https://en.wikipedia.org/wiki/Thysanoessa
  # Since `Krill`, `E crystallorophias` and `Thysanoessa` are all under the umbrella of krill,
  # we can just group krill together. And create a Krill and other separation
  z_df['All Krills'] = z_df['Krill'] + z_df['Thy'] +  z_df['Ecrystallorophias']
  z_df['All Other'] = z_df['Salp'] + z_df['Limacina']

  del z_df['col_2630']
  del z_df['col_2631']
  del z_df['col_2632']
  del z_df['col_2633']
  del z_df['col_2634']
  del z_df['col_2635']
  del z_df['col_2636']
  del z_df['col_2637']
  del z_df['col_2638']
  del z_df['col_2639']
  del z_df['col_2640']
  del z_df['col_2641']
  del z_df['col_2642']

  return z_df

########### main program ###########
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

##### First Row #####
row1_1, row1_2= st.columns((4, 1))
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
      width=800,
      height=600
  )
  st.altair_chart(base + points, use_container_width=True)

load_sites_map()

# zooming in
map_source = alt.topo_feature(
  'https://raw.githubusercontent.com/jazlyn5/hosting_data/master/ata_map.topojson',
  'collection'
)
sites_df = load_and_clean_sites_data()
base = alt.Chart(map_source).mark_geoshape(
    fill='lightgray',
    stroke='white'
  ).project(
    type='transverseMercator',
    center=[-23, -80],
    scale=3500,
    # clipExtent= [[0, 0], [400, 300]],
  )

points = alt.Chart(sites_df).mark_circle(
).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    size=alt.value(80),
    tooltip=[
      alt.Tooltip('site name'),
      alt.Tooltip('Focus')
    ],
    color="Focus:N"
    # color=alt.condition(brush, 'Count:N', alt.value('lightgray'))
).project(
    type="transverseMercator",
    center=[-23, -80],
    scale=3500,
    # clipExtent= [[0, 0], [400, 300]],
).properties(
    width=800,
    height=600
)
st.altair_chart(base + points)


########## try zooplankton
z_df = load_and_clean_zooplankton_data()
z_1993 = z_df[z_df['Year'].dt.year == 1996]
z_1993.reset_index()

##### try altair zooplankton
z_base = alt.Chart(map_source).mark_geoshape(
    fill='lightgray',
    stroke='white'
  ).project(
    type='transverseMercator',
    center=[-25, -80],
    scale=1300,
    clipExtent= [[0, 0], [400, 300]],
  )

z_points = alt.Chart(
  z_1993[['Longitude', 'Latitude', 'All Krills']]
).mark_circle(
).encode(
    longitude='Longitude:Q',
    latitude='Latitude:Q',
    size=alt.Size('All Krills:Q', title='Krill Abundance', scale=alt.Scale(domain=[0, 1000])),
    tooltip='All Krills',
    # color=alt.condition(brush, 'Count:N', alt.value('lightgray'))
).project(
    type="transverseMercator",
    center=[-25, -80],
    scale=1300,
    clipExtent= [[0, 0], [400, 300]],
).properties(
    width=500,
    height=400
)

st.altair_chart(z_base + z_points)

##### try pydeck zooplankton
z_1993['new_krills_radius'] = z_1993['All Krills'].apply(lambda x: x * 5.0 if x < 100 else x)
layers = [
    pdk.Layer(
        "ScatterplotLayer",
        z_1993,
        pickable=True,
        opacity=0.5,
        stroked=True,
        filled=True,
        radius_scale=3,
        radius_min_pixels=3,
        radius_max_pixels=3,
        line_width_min_pixels=1,
        get_position=["longitude", "latitude"],
        get_radius="new_krills_radius",
        get_fill_color=[204, 0, 0],  # [99, 140, 201],
        get_line_color=[255, 255, 255],
    ),
]
view_state = pdk.ViewState(
    latitude=-64,
    longitude=-64,
    zoom=3,
    max_zoom=16,
    pitch=0,
    bearing=0
)

st.pydeck_chart(
  pdk.Deck(
    map_style="mapbox://styles/mapbox/light-v9",
    layers=layers,
    initial_view_state=view_state,
    tooltip={"text": "Krill Abundance: {All Krills}"},
    height=800,
    width=800,
  ),
  use_container_width=True
)

##### try pydeck 
# with row1_1:
#   COUNTRIES = "https://d2ad6b4ur7yvpq.cloudfront.net/naturalearth-3.3.0/ne_50m_admin_0_scale_rank.geojson"
#   view_state = pdk.ViewState(
#     latitude=51.47, 
#     longitude=0.45, 
#     zoom=0, 
#     min_zoom=0
#   )

#   # Set height and width variables
#   view = pdk.View(type="_GlobeView", controller=True, width=1000, height=700)


#   layers = [
#       pdk.Layer(
#           "GeoJsonLayer",
#           id="base-map",
#           data=COUNTRIES,
#           stroked=False,
#           filled=True,
#           get_fill_color=[200, 200, 200],
#       ),
#   ]

#   st.pydeck_chart(
#     pdk.Deck(
#       views=[view],
#       initial_view_state=view_state,
#       layers=layers,
#       # Note that this must be set for the globe to be opaque
#       parameters={"cull": True},
#     )
#   )
