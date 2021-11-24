import streamlit as st
import altair as alt
import pandas as pd

st.header("Diet & Sea Ice")
st.subheader("Sea Ice Area vs. Year")
def sea_ice():
    ice = pd.read_csv("EDA/Annual Sea Ice.csv")
    ice = ice[(ice["Year"] >= 1993) & (ice["Year"] <= 2018)].reset_index(drop=True)
    plot_data = ice.melt(id_vars=["Year"],
                         var_name="Location",
                         value_name="Area")

    highlight = alt.selection_multi(on='mouseover',
                              fields=['Location'], nearest=True, bind='legend')

    base =  alt.Chart(plot_data).encode(
        x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Area:Q', axis=alt.Axis(title="Sea Ice Area")),
        color=alt.Color('Location', scale=alt.Scale(scheme='tableau20')),
        tooltip='Location'
    )

    points = base.mark_circle().encode(
        opacity=alt.value(1)
    ).add_selection(
        highlight
    )

    lines = base.mark_line().encode(
        size=alt.condition(highlight, alt.value(4), alt.value(1))
    )

    chart = alt.layer(points+lines
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=1000,
        height=450
    ).configure_axis(
        titleFontSize=15
    ).interactive()

    st.altair_chart(chart)

sea_ice()
st.markdown("""
Usage:
- Hover over line -> highlight line and tooltip to show the corresponding location -> highlight corresponding legend
- Clicking on legend -> highlight corresponding line; Clicking on "location" -> select all legend
- Zooming in and out on plot area by scrolling mouse. Double click the plot area to reset zooming effect.
""")

