import streamlit as st


from overview import overview
from dataset import four_cs, dataset_description
from environment_narrative import root
from reproduction import run_reproduction
from census import census, study_island_intro

def _max_width(amount=2000):
  max_width_str = f"max-width: {amount}px;"
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


def navigation():
  try:
    path = st.experimental_get_query_params()['p'][0]
  except Exception as e:
    # print(e)
    st.error('Please use the main app.')
    return None
  return path


if navigation() == "home":
  _max_width(1200)
  overview()
  study_island_intro()

elif navigation() == "census":
  _max_width(1200)
  census()
  
elif navigation() == "environment/ecosystem":
  _max_width(1200)
  root()

elif navigation() == "reproduction":
  _max_width(1200)
  run_reproduction()

elif navigation() == "dataset":
  _max_width(1200)
  four_cs()
  dataset_description()

else:
  _max_width()
  st.write("Not a valid page. Please go to main page.")

# footer
def footer():
  st.markdown("---")
  footer="""
    <p style="font-family:Charter; color:gray; font-size: 12px;">
    Developed with ❤ by Crystal Jin (chenj), Wenqin Dong (wenqind), Jazlyn Li (zhixianl), Vanessa Yin (yuey4)
    </p>
    """
  st.markdown(footer, unsafe_allow_html=True)


footer()