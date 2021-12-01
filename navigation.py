import streamlit as st


from overview import overview
from dataset import four_cs, dataset_description
from environment_narrative import root


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
  _max_width()
  overview()

elif navigation() == "dataset":
  _max_width(1200)
  four_cs()
  dataset_description()

elif navigation() == "environment/ecosystem":
  _max_width(1200)
  root()

elif navigation() == "results":
  st.title('Results List')
  for item in range(25):
    st.write(f'Results {item}')

elif navigation() == "examples":
  st.title('Examples Menu')
  st.write('Select an example.')

