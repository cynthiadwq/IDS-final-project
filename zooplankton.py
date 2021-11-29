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
  # `Krill`, `E crystallorophias` and `Thysanoessa` are all under the umbrella of krill,
  # `Salp`: salp can be an important diet source for penguins, 
  # this research found diet samples consisting of almost 1/3 of total consumption:https://www.scimex.org/newsfeed/learning-about-penguins-diet-may-save-marine-life,-study-finds2
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


  counts_per_year = z_df.groupby(z_df['Year'].dt.year)[
    'Krill', 'Salp', 'Thy', 'Limacina', 'Ecrystallorophias', 'All Krills', 'All Other', 'Total Food'
  ].sum()
  counts_per_year = counts_per_year.reset_index()
  return (z_df, counts_per_year)


########### main program ###########
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

def indiv_zooplankton():
  (_, counts_per_year) = load_and_clean_zooplankton_data()
  indiv_per_year = counts_per_year[['Year', 'Krill', 'Salp', 'Thy', 'Limacina', 'Ecrystallorophias']]
  indiv_per_year = indiv_per_year.melt(
    id_vars=['Year'], 
    var_name='Category',
    value_name='Amount'
  )
  highlight = alt.selection_multi(
    on='mouseover',
    fields=['Category'], 
    nearest=True, 
    bind='legend'
  )

  base = alt.Chart(indiv_per_year).mark_bar().encode(
    x=alt.X('Category:O', axis=alt.Axis(labelAngle=45)),
    y=alt.Y('sum(Amount):Q', axis=alt.Axis(title="Zooplankton Abundance (num/1000m³)")), 
  )  
  bars = base.encode(
    column='Year:O',
    opacity=alt.condition(highlight, alt.value(1), alt.value(0.4)),
    # color=alt.Color('Category',scale=alt.Scale(scheme='tableau10')),
    color=alt.condition(highlight, 'Category', alt.value('lightgrey'), scale=alt.Scale(scheme='blues')),
    tooltip=alt.Column('Category')
  ).add_selection(
    highlight
  ).properties(
    width=50,
    height=350
  ).interactive()
  st.altair_chart(bars)

indiv_zooplankton()

def total_zooplankton():
  (_, counts_per_year) = load_and_clean_zooplankton_data()
  total_zooplankton = counts_per_year[['Year', 'Total Food']]
  base = alt.Chart(total_zooplankton).mark_bar().encode(
    x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Total Food:Q', axis=alt.Axis(title="Total Zooplankton Abundance (num/1000m³)")), 
  )
  bar = base.encode(
    color=alt.Color('Total Food:Q',scale=alt.Scale(scheme='blues')),
    tooltip=[
      alt.Tooltip('Total Food'),
    ]
  )
  points = base.mark_circle().encode(
    opacity=alt.value(1),
  )
  lines = base.mark_line().encode(
    color=alt.value('lightblue')
  )
  regression = base.transform_regression(
    'Year', 'Total Food', method="linear"
  ).mark_line(
  ).transform_fold(
     ["reg-line"], 
     as_=["Regression", "y"]
  ).encode(
    alt.Color("Regression:N", scale=alt.Scale(scheme='reds'))
  )
  chart = alt.layer(bar + lines + points + regression).properties(
    width=650,
    height=350
  ).resolve_scale(color='independent')
  st.altair_chart(chart)
total_zooplankton()
