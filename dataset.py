from __future__ import annotations

import streamlit as st
from PIL import Image

# SETTING PAGE CONFIG TO WIDE MODE
# st.set_page_config(layout="wide")

########## main program ##########
def _max_width():
  max_width_str = f"max-width: 1200px;"
  st.markdown(
      f"""
  <style>
  .reportview-container .main .block-container{{
      {max_width_str}
  }}
  </style>    
  """,
      unsafe_allow_html=True,
  )
# _max_width()

def four_cs():
  title = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    The Four C's
    </b>
    """
  st.markdown(title, unsafe_allow_html=True)
  d1 = """
      <ol style="font-family:Charter; color:Black; font-size: 18px;">
      <li>
      <b style="font-size: 20px;">Complete</b>:
      The datasets are on Adelie penguins residing in 5 specific islands, 
      with some datasets having more samples collected on some island(s) over the others 
      (eg. Population Arrival dataset is solely about penguins on Humble island). 
      Additionally, we are missing data from 2003 for zooplankton sample data, 
      and we only have zooplankton data until 2004 inclusive. Other than that, 
      the data we have cover the entire breeding season of Adelie penguins consistently every year for more than 20 years, 
      from 1992 to 2018, and the datasets cover many aspects that shed light on this penguin species 
      from environmental factors, diet, to reproductive success, and population change throughout years. 
      </li>
      <li>
      <b style="font-size: 20px;">Correct</b>:
      Generally, the datasets we used are coherent. 
      All datetime information lies within the range of 1991 ~ 2019, 
      which aligns with the ongoing study time. The datasets also make sense relative to themselves 
      as we did not observe absurd extreme values or unexpected patterns during the EDA analysis phase. 
      All the nominal/ordinal data does not contain spelling mistakes 
      and they only serve as special notes or remarks to specific rows that need special attention.
      </li>
      <li>
      <b style="font-size: 20px;">Coherent</b>：
      We can rely on the data source to ensure its correctness. 
      The data are retrieved from Palmer Station, one of the three United States research stations located in Antarctica. 
      The study protocol briefly explains the method they are using to retrieve the data, 
      “data are obtained in accordance with the CEMP Standard Methods (CCAMLR 1992), noting the following exceptions: 
      Censuses to determine breeding population size are done as close to peak egg laying as possible 
      in accordance with the protocol, but only incubating birds are censused... 
      The search effort to detect returning, previously banded penguins is standardized by involving two people 
      that search every colony on Humble Island every two days during the entire length of the field season.”
      </li>
      <li>
      <b style="font-size: 20px;">aCcountable</b>:
      The data source is publicly available on the official site of Palmer station 
      (one of the United States Antarctica programs of the National Science Foundation). 
      In order to provide our audience a transparent view into data, we include the original data, 
      the detailed steps of how we processed the original data (in the format of a Jupyter notebook), 
      and the final polished datasets in our repository. 
      We also publish the code to generate every visualization we present in this website, 
      so that everyone can reproduce them.
      </li>
      </ol>
      <br><br>
    """
  st.markdown(
    d1, unsafe_allow_html=True
  )
# four_cs()

def dataset_description():
  title = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    Data Source Description
    </b>
    """
  st.markdown(title, unsafe_allow_html=True)
  d1 = """
    <body style="font-family:Charter; color:Black; font-size: 15px;">
    <br>
    <b style="font-size: 20px;">Adelie Penguin Census</b>
    <br>
    This dataset records the population of breeding pairs on 5 islands from 1991 to 2017. 
    5 islands are: Torgersen Island, Humble Island, Litchfield Island, Cormorant Island, and Christine Island. 
    Although it also has a colony category for each island, such information is not used in our website 
    to keep consistency with metrics of other data. Explained by the abstract, 
    “the timing of this census is assisted by the REPRO and HUMPOP data, 
    which provide a daily to weekly rate of change in breeding adult population numbers as new nests are initiated.” 
    And the population of breeding pairs is mainly counted during November and December each year.
    <br><br>
    </body>
  """
  st.markdown(
    d1, unsafe_allow_html=True
  )

  d2 = """
    <body style="font-family:Charter; color:Black; font-size: 15px;">
    <b style="font-size: 20px;">Adelie Penguin Population Arrival</b>
    <br>
    This dataset records the breeding population arrival chronology on Humble Island from 1991 to 2017. 
    Explained by the abstract, “the arrival chronology of adult Adélie penguins on Humble Island is documented annually 
    through island-wide censuses performed as ice and weather conditions permit. Recorded data (numbers of adults present) 
    provide a measure of the number of adults arriving daily at the breeding colonies, a metric that is 
    sensitive to environmental conditions such as sea ice extent during late winter and early spring.” 
    Similar to the census data, it also has a colony category which is not used in our website. 
    But the whole population arrival pattern can be obtained from such chronology records.
    <br><br>
    </body>
  """
  st.markdown(
    d2, unsafe_allow_html=True
  )

  d3 = """
    <body style="font-family:Charter; color:Black; font-size: 15px;">
    <b style="font-size: 20px;">Adelie Penguin Chick Broods</b>
    <br>
    This dataset records the nests information in five main islands on which the Adélie penguin colonies have historically occurred, 
    and typically during the first week of January when chicks are in the guard stage. 
    These colonies are censused to determine the ratio of 1-chick to 2-chick nests. 
    This census is restricted to nests that are no more than one meter in from the colony perimeter.
    <br><br>
    </body>
  """
  st.markdown(
    d3, unsafe_allow_html=True
  )

  d4 = """
    <body style="font-family:Charter; color:Black; font-size: 15px;">
    <b style="font-size: 20px;">Adelie Penguin Reproductive Success</b>
    <br>
    This dataset records information about a sample of Adélie penguin nests from colonies on Humble Island. 
    These samples are randomly selected annually and checked daily (or as ice and weather conditions permit) 
    throughout the breeding season from the time adults arrive until the chick crèche phase of the reproductive cycle. 
    Recorded data (the timing of egg laying, hatching and crèching) provide a measure of annual breeding chronology, 
    and the number of chicks crèched, an estimate of reproductive success (chicks crèched/breeding pair).
    <br><br>
    </body>
  """
  st.markdown(
    d4, unsafe_allow_html=True
  )

  
  d5 = """
    <body style="font-family:Charter; color:Black; font-size: 15px;">
    <b style="font-size: 20px;">Adelie Penguin Chick Counts</b>
    <br>
    This dataset records information on the total number of chicks produced on the five main islands 
    on which Adélie penguin colonies have historically occurred. 
    These are censused synoptically once a year to determine the total number of chicks produced in the area. 
    The optimal date for this census may vary by a few days each season, 
    but ultimately tries to capture the week following the time when approximately 2/3 of the chicks have crèched.
    <br><br>
    </body>
  """
  st.markdown(
    d5, unsafe_allow_html=True
  )

  row6_1, row6_2 = st.columns((1, 2))
  with row6_1:
    attack_img = Image.open("images/adelie_attack_emperor.jpg")
    width, height = attack_img.size 
    # cropped_area = (0, 120, width, height - 50)
    # cropped_img = sample_map_img.crop(cropped_area)
    st.image(attack_img, "Penguin Attack!")
  with row6_2:
    d6 = """
      <body style="font-family:Charter; color:Black; font-size: 15px;">
      <b style="font-size: 20px;">Adelie Penguin Diet Composition (multiple datasets)</b>
      <br>
      This series of datasets record the amount (measured in weight and size) of major prey 
      obtained from the diet samples of Adelie Penguin. 
      This includes resuspension of the samples in fresh water to release fish otoliths, 
      squid beaks and other prey hard parts, and then draining to a consistency 
      that facilitates separating the diet samples into subsamples of prey components. 
      Considering the completeness of the data, we mainly focus on analyzing E. superba, 
      which is a primary prey of Adelie Penguin.
      <br><br>
      </body>
    """
    st.markdown(
      d6, unsafe_allow_html=True
    )

    d7 = """
      <body style="font-family:Charter; color:Black; font-size: 15px;">
      <b style="font-size: 20px;">Annual Sea Ice</b>
      <br> 
      This dataset records the area of sea ice in the surrounding locations of Palmer station. 
      The data is measured per year from 1979-2018 in the following locations: WAP, Pori, Pdsr, Pnew. 
      The original data records the area of sea ice extent, sea ice and open water. All measured in km^2. 
      <br><br>
      </body>
    """
    st.markdown(
      d7, unsafe_allow_html=True
    )

  row9_1, row9_2 = st.columns((2, 1))
  with row9_1: 
    d8 = """
      <body style="font-family:Charter; color:Black; font-size: 15px;">
      <b style="font-size: 20px;">Adelie Sites</b>
      <br>
      This dataset contains longitude, latitude, and island name of satellite sightings of Adelie Penguins all around Antarctica, 
      manually marked by collaborating scientists on an open-source data platform. 
      The dataset includes locations of penguin sightings from 1980 to 2019 inclusive.
      <br><br>
      </body>
    """
    st.markdown(
      d8, unsafe_allow_html=True
    )

    d9 = """
      <body style="font-family:Charter; color:Black; font-size: 15px;">    
      <b style="font-size: 20px;">Zooplankton Abundances</b>
      <br>
      This dataset contains calculated abundances for krill, salp and species of zooplankton per 1000 meter cubed, 
      from samples collected between 1993 and 2004 inclusive. Data was collected aboard cruises 
      off the coast of the Western Antarctic Penninsula close to Adelie Penguin habitats (near Torgersen island), 
      along designated spots each year (radiating outwards from coastline, see image on the right). 
      There is an average of 57 samples collected each year except 2003. 
      The dataset contains study’s year, longitude and latitude of the sample collection location, and per species abundance. 
      </body>
    """
    st.markdown(
      d9, unsafe_allow_html=True
    )
  with row9_2:
    sample_map_img = Image.open("images/zooplankton_sample_map.png")
    # width, height = sample_map_img.size 
    # cropped_area = (0, 120, width, height - 50)
    # cropped_img = sample_map_img.crop(cropped_area)
    st.image(sample_map_img, "Annual Zooplankton Sample Collection Sites")


# dataset_description()


