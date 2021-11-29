import streamlit as st
import altair as alt
from altair import datum
import pandas as pd
import numpy as np

GRADIENT_COLOR_SCHEME = "redpurple"
CATEGORY_COLOR_SCHEME = "category20"

def census_plot():
    st.write("Let's see the total adults count change on all islands (CHR: Christine, TOR: Torgersen, COR: Cormorant, HUM: Humble, LIT: Litchfield) over years. ")

    df = pd.read_csv("EDA/Adelie Penguin Census.csv")
    df["Date"] = pd.to_datetime(df["Date GMT"])
    df["Adults"] = 2 * df["Breeding Pairs"]
    df["Year"] = df["Date"].dt.year
    adult_count_year_data = df.groupby(df["Year"], as_index=False)["Adults"].sum()
    bars = alt.Chart(adult_count_year_data, title="Adelie Penguin Population Change on 5 Islands Over Years").mark_bar().encode(
        x='Year:Q',
        y="Adults:Q",
        color=alt.Color('Adults', scale=alt.Scale(scheme=GRADIENT_COLOR_SCHEME)),
    )
    text = bars.mark_text(
        align='center',
        baseline='middle',
        dy=-5
    ).encode(
        text='Adults:Q'
    )
    chart = alt.layer(bars+text)\
        .properties(
            width=2000,
            height=400
        )
    st.altair_chart(chart, use_container_width=True)

def census_island_plot():
    df = pd.read_csv("EDA/Adelie Penguin Census.csv")
    df["Adults"] = 2 * df["Breeding Pairs"]
    island_count_data = df[["Adults", "Island", "Date GMT"]].groupby(["Island", "Date GMT"], as_index=False)["Adults"].sum()
    chr_df = island_count_data[island_count_data["Island"] == 'CHR']
    tor_df = island_count_data[island_count_data["Island"] == 'TOR']
    cor_df = island_count_data[island_count_data["Island"] == 'COR']
    hum_df = island_count_data[island_count_data["Island"] == 'HUM']
    lit_df = island_count_data[island_count_data["Island"] == 'LIT']

    options, plot = st.columns((3, 7))
    with options: 
        genre = st.radio("Choose an island to see Adelie penguin's population change on this island from 1991 to 2017", ('CHR - Christine', 'TOR - Torgersen', 'COR - Cormorant', 'HUM - Humble', 'LIT - Litchfield'))
        if genre == 'CHR - Christine':
            selected_df = chr_df
        elif genre == 'TOR - Torgersen':
            selected_df = tor_df
        elif genre == 'COR - Cormorant':
            selected_df = cor_df
        elif genre == 'HUM - Humble':
            selected_df = hum_df
        elif genre == 'LIT - Litchfield':
            selected_df = lit_df

        st.info("Note: You can hover on bars to see the precise count number.")

    with plot:
        bars = alt.Chart(selected_df, title="Adelie Penguin Population Change on Selected Island Over Years").mark_bar().encode(
            x='Date GMT',
            y=alt.Y("Adults:Q", scale=alt.Scale(domain=[0,6200])),
            color=alt.Color('Adults', scale=alt.Scale(scheme=GRADIENT_COLOR_SCHEME)),
            tooltip='Adults'
        )
        st.altair_chart(bars, use_container_width=True)

def population_arrival_plot():
    df = pd.read_csv("EDA/Adelie Penguin Population Arrival.csv")
    df["Date"] = pd.to_datetime(df["Date GMT"])
    count_date_data = df[["Adults", "Date GMT", "Date"]].groupby(["Date GMT", "Date"], as_index=False)["Adults"].sum()

    info, plot = st.columns((2,8))
    with info:
        st.info("""
        These two graphs are associtaed with each other.

        Usage:
        - Use mouse to drag an area on the upper graph, a more detailed look on this section will be displayed on the lower graph.
        - Hover on the bars of lower graph to see detailed information
        """)

    with plot:
        x_init = pd.to_datetime(['2000-07-01', '2001-05-01']).view(int) / 1E6
        brush = alt.selection(type='interval', encodings=['x'], zoom=True, init={'x':list(x_init)})
        bars_base = alt.Chart(count_date_data, title="Adelie Penguin Population Arrival").mark_bar().encode(
            x = "Date GMT:T", 
            y = "Adults:Q",
            color=alt.Color('Adults', scale=alt.Scale(scheme=GRADIENT_COLOR_SCHEME)),
        ).properties(
            width=800,
            height=250
        )
        
        bars_whole = bars_base.add_selection(
            brush
        )
        bars_detail = bars_base.encode(
            alt.X('Date GMT:T', 
            scale=alt.Scale(domain=brush)),
            tooltip=[
            alt.Tooltip('Date', title='Date in GMT'),
            alt.Tooltip('Adults', title='Adults arrived')
            ]
        )

        st.altair_chart(
            alt.vconcat(
                bars_whole,
                bars_detail,
                center=True
            ).resolve_scale(color='independent'),
            use_container_width=True
        )

def annual_population_arrival_plot():
    st.write("If we draw population arrival patterns for each year, and compare the annual patterns in a single \
        graph, the variation will be more obvious.")
    st.info("""
    Usage:
    - Change the year ranges to focus on certain annual patterns
    - Hover on a point on the lines to see its detailed information
    - Click the Start Year legend on the right to focus on a single year pattern
    - Click on the graph to cancel single highlighting
    """)
    values = st.slider('Select a range of years to display annual population arrival patterns for these years', 
        1991, 2017, (2001, 2007))
    
    df = pd.read_csv("EDA/Adelie Penguin Population Arrival.csv")
    df["Date"] = pd.to_datetime(df["Date GMT"])
    df = df.sort_values('Date')
    count_date_data = df[["Adults", "Date GMT", "Date"]].groupby(["Date GMT", "Date"], as_index=False)["Adults"].sum()
    count_date_data["Start Year"] = np.where(
        count_date_data["Date"].dt.month < 6, 
        count_date_data["Date"].dt.year - 1, 
        count_date_data["Date"].dt.year
    )
    count_date_data["Month Date"] = count_date_data["Date"].dt.strftime('%m-%d')
    count_date_data["Month"] = count_date_data["Date"].dt.month
    # count_date_data

    highlight = alt.selection_single(on='mouseover', fields=['Start Year'], nearest=True, bind='legend')

    lines = alt.Chart(count_date_data, title="Annual Population Arrival Pattern").transform_filter(
        'datum["Month"] > 8 || datum["Month"] < 3',
    ).mark_line(point=True, interpolate='cardinal').encode(
        y=alt.Y("Adults:Q"),
        x=alt.X("Month Date:N", 
            sort=list(pd.date_range('2019-10-01', '2020-03-01', freq='D').strftime("%m-%d")),
            title="Measured Date",
            axis=alt.Axis(labelAngle=60)
            ),
        color = alt.Color('Start Year:O', scale=alt.Scale(scheme=CATEGORY_COLOR_SCHEME)),
        order = alt.Order('min(Date)'),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.1)),
        tooltip=[
          alt.Tooltip('Date', title='Date in GMT'),
          alt.Tooltip('Adults', title='Adults arrived')
        ]
    ).transform_filter(
        alt.FieldRangePredicate(field='Start Year', range=[values[0], values[1]])
    ).add_selection(
        highlight
    ).properties(
        width=1000,
        height=500
    ).configure_axis(
        labelFontSize=8
    )

    st.altair_chart(lines, use_container_width=True)

# main program starts here
st.set_page_config(layout="wide")
st.write("TODO: add transition story")
st.header("How did the population change?")
census_plot()
census_island_plot()

st.markdown('---')
st.header("How about the population arrival pattern change over years?")
st.write("We have seen the drastic change on the population of Adelie penguins over years. How about a \
    more detailed look into the annual population arrival pattern of them? Due to data limitation, let's \
    focus on Humble Island this time. But the study data will be sufficient for us to see an annual pattern \
    for each year.")
st.write("Because of the activity pattern of Adelie penguins, study data is retrieved annually from October \
    to next Feburary. As a result, we'll view the cycle of annual pattern as from October to next Feburary.")
population_arrival_plot()
annual_population_arrival_plot()