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
        size=alt.condition(~highlight, alt.value(1), alt.value(4))
    )

    chart = alt.layer(points+lines)\
    .configure_axis(
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
- Clicking on legend -> highlight corresponding line; Clicking on "location" -> dis-select all legend
- Zooming in and out on plot area by scrolling mouse. Double click the plot area to reset zooming effect.
""")

st.subheader("E. superba weight vs. Year")

def superba():
    diet_info = pd.read_csv("EDA/diet_info.csv")
    plot_data = diet_info[diet_info["year"] != 0]
    plot_data = plot_data[plot_data["Bird Weight (g)"] != 0]
    plot_data = plot_data[plot_data["E. superba Weight (g)"] != 0]

    brush = alt.selection(type='interval', encodings=['x'])

    box = alt.LayerChart(data=plot_data).transform_aggregate(
        max="max(E. superba Weight (g))",
        min="min(E. superba Weight (g))",
        q1="q1(E. superba Weight (g))",
        q3="q3(E. superba Weight (g))",
        mean="mean(E. superba Weight (g))",
        groupby=["year"]
    ).encode(
        tooltip=['mean:Q']
    ).add_layers(
        alt.Chart().mark_rule().encode(
            y=alt.Y('min:Q', title="E superba weight", scale=alt.Scale(domain=[50, 900])),
            y2=alt.Y2('max:Q', title="E superba weight")
        ),
        alt.Chart().mark_bar(width=15).encode(
            y=alt.Y('q1:Q', title="E superba weight", scale=alt.Scale(domain=[50, 900])),
            y2=alt.Y2('q3:Q', title="E superba weight"),
            color=alt.condition(brush, alt.Color('year:Q', scale=alt.Scale(scheme='spectral')), alt.value("lightgray"))
        ),
        alt.Chart().mark_line(color='black').encode(
            y=alt.Y("mean:Q", title="E superba weight", scale=alt.Scale(domain=[50, 900]))
        )
    ).add_selection(
        brush
    ).properties(
        width=800,
        height=300
    )
    box = box.encode(x=alt.X('year:Q', scale=alt.Scale(domain=[1993, 2018])))


    plot_data = plot_data.rename(columns={"E. superba Weight (g)": "E superba weight"})
    scatter = alt.Chart(plot_data).mark_circle().encode(
        x=alt.X("Bird Weight (g):Q", scale=alt.Scale(zero=False)),
        y="E superba weight:Q",
    ).transform_filter(
        brush
    ).properties(
        width=800,
        height=300
    )

    regression_line = scatter.transform_regression("Bird Weight (g)", "E superba weight").mark_line()

    chart = alt.vconcat(box, scatter+regression_line
    ).configure_title(
        fontSize=30
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )
    chart

superba()
st.markdown("""
Usage:
- Brush over boxplot area to see one or multiple years being selected, and the scatter plot is updated (filtered) accordingly.
- Drag the selected area left and right to see change over year.
- Hover over boxplot to see mean value of each year.
""")
