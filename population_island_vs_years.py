from __future__ import annotations
from os import truncate

from numpy.lib.npyio import load

import streamlit as st
import streamlit.components.v1 as components
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
def load_and_clean_chick_counts():
  raw_cc_df = pd.read_csv(
      "EDA/Adelie Penguin Chick Counts.csv", 
      engine='python'
    )
  cc_df = raw_cc_df.copy()
  # Processing column
  cc_df['Parents'] = cc_df['Adults'] * 2 # data contains adult breeding pairs
  cc_df['Total Population'] = cc_df['Parents'] + cc_df['Chicks']
  cc_df['Date'] = pd.to_datetime(cc_df['Date GMT'])
  cc_df['Year'] = cc_df['Date'].dt.year
  cc_df['Island'] = cc_df['Island'].str.rstrip()
  cc_df['Island'] = cc_df['Island'].str.lstrip()

  total_counts_per_year_per_island = cc_df.groupby(
  [cc_df['Year'], cc_df['Island']]
  ).agg({'Colony':'count', 'Parents': 'sum', 'Chicks': 'sum', 'Total Population': 'sum'})
  total_counts_per_year_per_island = total_counts_per_year_per_island.reset_index()

  # Compute percentage
  total_counts_per_year = total_counts_per_year_per_island.groupby('Year')['Total Population'].sum()
  total_counts_per_year = total_counts_per_year.reset_index()
  temp = total_counts_per_year.copy()
  year_to_total = temp.set_index('Year').to_dict()['Total Population']

  def compute_percentage(row):
    base = year_to_total[row['Year']]
    denom = row['Total Population']
    return denom / base * 100

  total_counts_per_year_per_island['Total Population Percentage'] = total_counts_per_year_per_island.apply(
      compute_percentage,
      axis=1
  ).round(2)
  return total_counts_per_year_per_island

########### main program ###########
# SETTING PAGE CONFIG TO WIDE MODE
st.set_page_config(layout="wide")

########## percentage per island throughout years 
def percentage():
  # reference: https://altair-viz.github.io/gallery/multiline_tooltip.html
  source = load_and_clean_chick_counts().copy()[['Year', 'Island', 'Total Population Percentage']]

  # Create a selection that chooses the nearest point & selects based on x-value
  nearest = alt.selection(
    type='single', 
    nearest=True, 
    on='mouseover',
    fields=['Year'], 
    empty='none'
  )

  # The basic line
  # cardinal interpolation: a Cardinal spline, with control point duplication on the ends.
  line = alt.Chart(source).mark_line(interpolate='cardinal').encode(
    x='Year:Q',
    y='Total Population Percentage:Q',
    color=alt.Color('Island:N', scale=alt.Scale(scheme='tableau10'))
  )

  # Transparent selectors across the chart. This is what tells us
  # the x-value of the cursor
  selectors = alt.Chart(source).mark_point().encode(
    x='Year:Q',
    opacity=alt.value(0),
  ).add_selection(
    nearest
  )

  # Draw points on the line, and highlight based on selection
  points = line.mark_point().encode(
    opacity=alt.condition(nearest, alt.value(1), alt.value(0))
  )

  # Draw text labels near the points, and highlight based on selection
  text = line.mark_text(align='left', dx=5, dy=-5).encode(
    text=alt.condition(nearest, 'Total Population Percentage:Q', alt.value(' '))
  )

  # Draw a rule at the location of the selection
  rules = alt.Chart(source).mark_rule(color='gray').encode(
    x='Year:Q',
  ).transform_filter(
    nearest
  )

  # Put the five layers into a chart and bind the data
  chart = alt.layer(
    line, selectors, points, rules, text
  ).properties(
    width=600, height=300
  )
  st.altair_chart(chart)

percentage()

########## alternative highlight percentage 
def percentage_2():
  
  source = load_and_clean_chick_counts().copy()[['Year', 'Island', 'Total Population Percentage']]

  # Reference: https://altair-viz.github.io/gallery/multiline_highlight.html
  highlight = alt.selection_multi(
    on='mouseover',
    fields=['Island'], 
    nearest=True, 
    bind='legend'
  )

  base = alt.Chart(source).encode(
    x=alt.X('Year:O', axis=alt.Axis(labelAngle=90)),
    y=alt.Y('Total Population Percentage:Q', axis=alt.Axis(title="Total Population Percentage")),
    color=alt.Color('Island', scale=alt.Scale(scheme='tableau20')),
    tooltip='Island'
  )

  points = base.mark_circle().encode(
    opacity=alt.value(1)
  ).add_selection(
    highlight
  )

  # cardinal interpolation: a Cardinal spline, with control point duplication on the ends.
  lines = base.mark_line(interpolate='cardinal').encode(
    size=alt.condition(~highlight, alt.value(1), alt.value(4))
  )

  chart = alt.layer(points+lines)\
  .configure_axis(
    grid=False
  ).configure_view(
    strokeWidth=0
  ).properties(
    width=600,
    height=300
  ).configure_axis(
    titleFontSize=15
  ).interactive()

  st.altair_chart(chart)

percentage_2()

########## open html altair chart
HtmlFile = open("cc_population_chart.html", 'r', encoding='utf-8')
source_code = HtmlFile.read() 
components.html(source_code, height= 1600, width=1600)

# ########## above html is rendered via below code in jupyter notebook, as streamlit altair didn't work :/
# # --- cell 1
# raw_cc_df = pd.read_csv(
#     "Adelie Penguin Chick Counts.csv", 
#     engine='python'
#   )
# cc_df = raw_cc_df.copy()
# # Processing column
# cc_df['Parents'] = cc_df['Adults'] * 2 # data contains adult breeding pairs
# cc_df['Total Population'] = cc_df['Parents'] + cc_df['Chicks']
# cc_df['Date'] = pd.to_datetime(cc_df['Date GMT'])
# cc_df['Year'] = cc_df['Date'].dt.year
# cc_df['Island'] = cc_df['Island'].str.rstrip()
# cc_df['Island'] = cc_df['Island'].str.lstrip()

# total_counts_per_year_per_island = cc_df.groupby(
# [cc_df['Year'], cc_df['Island']]
# ).agg({'Colony':'count', 'Parents': 'sum', 'Chicks': 'sum', 'Total Population': 'sum'})
# total_counts_per_year_per_island = total_counts_per_year_per_island.reset_index()

# melted = total_counts_per_year_per_island[['Year', 'Island', 'Parents', 'Chicks']].melt(
#     id_vars=['Year', 'Island'], 
#     value_vars = ['Parents', 'Chicks'],
#     var_name = 'Role',
#     value_name='Count',
#   )
# melted = melted.reset_index()

# pink_blue = alt.Scale(
#     domain=('Parents', 'Chicks'),
#     range=["steelblue", "salmon"]
# )
# slider = alt.binding_range(min=1992, max=2018, step=1)
# select_year = alt.selection_single(
# name="Year", 
# fields=['Year'],
# bind=slider, init={'Year': 1992}
# )
# # ---- cell 2
# chart = alt.Chart(melted).mark_bar().encode(
#     x=alt.X('Role:N', title=None),
#     y=alt.Y('Count:Q'), # scale=alt.Scale(domain=(0, 4500))),
#     color=alt.Color('Role:N'), # scale=pink_blue),
#     column='Island:O'
# ).properties(
#   width=20
# ).add_selection(
#   select_year
# ).transform_filter(
#   select_year
# ).configure_facet(
#   spacing=8
# )
# chart
# # --- cell 3
# chart.save('chart.html')

########## try native steamlit altair chart
# (_, total_counts_per_year_per_island) = load_and_clean_chick_counts()
# melted = total_counts_per_year_per_island[['Year', 'Island', 'Parents', 'Chicks']].melt(
#   id_vars=['Year', 'Island'], 
#   # value_vars = ['Parents', 'Chicks'],
#   var_name = 'Role',
#   value_name = 'Count',
# )
# melted = melted.reset_index()

# pink_blue = alt.Scale(
#   domain=('Parents', 'Chicks'),
#   range=["steelblue", "salmon"]
# )
# slider = alt.binding_range(min=1992, max=2018, step=1)
# select_year = alt.selection_single(
#   name="Year", 
#   fields=['Year'],
#   bind=slider, init={'Year': 1992}
# )

# base = alt.Chart(melted).mark_bar().encode(
#     x=alt.X('Role:N', title=None),
#     y=alt.Y('Count:Q'), #, scale=alt.Scale(domain=(0, 5000))),
#     color=alt.Color('Role:N'), # scale=pink_blue),
#     column='Island:O'
# ).properties(
#   width=20
# ).add_selection(
#   select_year
# )

# bars = base.transform_filter(
#   select_year
# ) # .configure_facet(
# #   spacing=8
# # ).interactive()


# st.altair_chart(base)
# st.dataframe(melted)