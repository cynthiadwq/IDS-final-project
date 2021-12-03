import streamlit as st
import altair as alt
from altair import datum
import pandas as pd
import numpy as np
from PIL import Image

GRADIENT_COLOR_SCHEME = "redpurple"
CATEGORY_COLOR_SCHEME = "category20"

def study_island_intro():
    palmer_icon = Image.open("images/palmer_icon.png")
    tor_image = Image.open("images/tor_image.jpeg")
    lit_image = Image.open("images/lit_image.jpeg")

    tor_location = Image.open("images/tor_location.png")
    hum_location = Image.open("images/hum_location.png")
    chr_location = Image.open("images/chr_location.png")
    lit_location = Image.open("images/lit_location.png")
    cor_location = Image.open("images/cor_location.png")

    title = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
    <br>
    Our approach: a look at Palmer Station, dataset and our Focus.
    </b>
    <br><br>
    """
    st.markdown(title, unsafe_allow_html=True)

    intro, icon = st.columns((8, 2))
    with intro:
        introduction = """
        <body style="font-family:Charter; color:Black; font-size: 18px;">
            <p>
                To look deeper into Adelie Penguin populations and other characteristics, we will \
                visualize and extract interesting information from \
                the data provided by the Palmer Station. The Palmer Long-Term Ecological Research (LTER) study area is \
                located to the west of the Antarctic Peninsula extending South and North of the Palmer Basin from onshore \
                to several hundred kilometers off shore. Palmer Station is one of the three United States research stations \
                located in Antarctica. Their datasets cover census, diet, chick status, etc., of Adelie Penguins (More \
                details see Data page), and also many other fields, such as bacterial properties of Antarctic, seabird, etc.
            </p>
            <p>
                If you are interested in the station or datasets, see links below:
                <ul>
                    <li><a href="https://pal.lternet.edu/">Palmer Station Website </a></li>
                    <li><a href="https://oceaninformatics.ucsd.edu/datazoo/catalogs/pallter/datasets"> Palmer Station Dataset </a></li>
                </ul>
            </p>
        </body>
        """
        st.markdown(
            introduction, unsafe_allow_html=True
        )
    with icon:
        st.image(palmer_icon, "Palmer Station LTER")

    instruction = """
    <body style="font-family:Charter; color:Black; font-size: 18px; padding-top: 20px;">
        <p>
            Although Adelie penguins live across Antarctica continent and neighboring islands, we’ll use the datasets \
            from the Palmer Station which focus on 5 islands instead. Below is a short introduction to these islands.
        </p>
    </body>
    """
    st.markdown(
        instruction, unsafe_allow_html=True
    )

    st.subheader("Christine Island (CODE: CHR)")
    l_chr, m_chr = st.columns((2, 8))
    with l_chr:
        st.image(chr_location, "Christine Island Location")
    with m_chr:
        st.metric(label="Coordinates", value="64°48′S 64°02′W")
        st.write("Christine Island is an island 0.9 km (0.5 nmi) long which lies 1.9 km (1 nmi) off the south coast of Anvers Island and 2.8 km (1.5 nmi) southeast of Bonaparte Point.")

    st.subheader("Torgersen Island (CODE: TOR)")
    l_tor, m_tor, r_tor = st.columns((2, 6, 2))
    with l_tor:
        st.image(tor_location, "Torgersen Island Location")
    with m_tor:
        st.metric(label="Coordinates", value="64°46′S 64°5′W")
        st.write("Torgersen Island is a small rocky island lying just east of Litchfield Island in the entrance to Arthur Harbour, off the south-west coast of Anvers Island in the Palmer Archipelago of Antarctica.")
    with r_tor:
        st.image(tor_image, "Adelie penguins on Torgersen Island")

    st.subheader("Cormorant Island (CODE: COR)")
    l_cor, m_cor = st.columns((2, 8))
    with l_cor:
        st.image(cor_location, "Cormorant Island Location")
    with m_cor:
        st.metric(label="Coordinates", value="64°48′S 63°58′W")
        st.write("Cormorant Island is a 10 ha island lying in Bismarck Strait 1 km south of Anvers Island, 4 km (2.5 mi) east-south-east of Bonaparte Point, in the Palmer Archipelago of Antarctica. It lies some 5 km to the south-east of the United States' Palmer Station in Arthur Harbour on Anvers Island.")

    st.subheader("Humble Island (CODE: HUM)")
    l_hum, m_hum = st.columns((2, 8))
    with l_hum:
        st.image(hum_location, "Humble Island Location")
    with m_hum:
        st.metric(label="Coordinates", value="64°46′S 64°06′W")
        st.write("Humble Island is a small rocky island lying 0.74 km (0.4 nmi) south-east of Norsel Point on Amsler Island, off the south-west coast of Anvers Island in the Palmer Archipelago of Antarctica.")

    st.subheader("Litchfield Island (CODE: LIT)")
    l_lit, m_lit, r_lit = st.columns((2, 6, 2))
    with l_lit:
        st.image(lit_location, "Litchfield Island Location")
    with m_lit:
        st.metric(label="Coordinates", value="64°46′S 64°06′W")
        st.write("Litchfield Island is a rocky island 0.9 kilometres (0.5 nmi) long and rising to 50 m (164 ft), lying in Arthur Harbour, 0.9 kilometres (0.5 nmi) south of Norsel Point, off the south-west coast of Anvers Island in the Palmer Archipelago of Antarctica.")
        st.write("The island, together with its littoral zone, possesses an unusually high collection of marine and terrestrial life and is unique amongst the neighboring islands as a breeding place for six species of native birds. It provides an outstanding example of the natural ecological system of the Antarctic Peninsula area. In addition, Litchfield Island possesses rich growths of vegetation and has the most varied topography and the greatest diversity of terrestrial habitats of the islands in Arthur Harbour.")
    with r_lit:
        st.image(lit_image, "Litchfield island picture")

    
    instruction = """
    <body style="font-family:Charter; color:Black; font-size: 20px; padding-top: 50px">
        <p>
            As we can see, these 5 islands are either adjacent to each other, or near to others. Therefore, we will view
            them as a whole in some of our data visualizations on following pages.
        </p>
    </body>
    """
    st.markdown(
        instruction, unsafe_allow_html=True
    )
    # st.write("As we can see, these 5 islands are either adjacent to each other, or near to others. Therefore, in some of our data visualizations, we will view them as a whole.")

def census_plot():
    instruction = """
        <body style="font-family:Charter; color:Black; font-size: 18px;">
        <p>
            Let's see the total adults count change on all islands (CHR: Christine, TOR: Torgersen, COR: Cormorant, HUM: Humble, LIT: Litchfield) over years.
        </p>
        </body>
        """
    st.markdown(
        instruction, unsafe_allow_html=True
    )

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
    instruction = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
        <p>
            We have seen the drastic change on the population of Adelie penguins over years. How about a \
            more detailed look into the annual population arrival pattern of them? Due to data limitation, let's \
            focus on Humble Island this time. But the study data will be sufficient for us to see an annual pattern \
            for each year.
        </p>
        <p>
            Because of the activity pattern of Adelie penguins, study data is retrieved annually from October \
            to next Feburary. As a result, we'll view the cycle of annual pattern as from October to next Feburary.
        </p>
    </body>
    """
    st.markdown(
        instruction, unsafe_allow_html=True
    )

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
    instruction = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
        <p>
            If we draw population arrival patterns for each year, and compare the annual patterns in a single \
            graph, the variation will be more obvious.
        </p>
    </body>
    """
    st.markdown(
        instruction, unsafe_allow_html=True
    )

    st.info("""
    Usage:
    - Change the year ranges to focus on certain annual patterns
    - Hover on a point on the lines to see its detailed information
    - Click the Start Year legend on the right to focus on a single year pattern
    - Click on the graph to cancel single highlighting

    Hint: Try choose a range of years and then click on the start year legends on the right from the first year to the last year!
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
def census():
    header1 = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
        How did the Adelie penguin's population change?
    </b>
    """
    st.markdown(
        header1, unsafe_allow_html=True
    )
    census_plot()
    census_island_plot()

    st.markdown('---')
    header2 = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
        How about their population arrival pattern change over years?
    </b>
    """
    st.markdown(
        header2, unsafe_allow_html=True
    )
    population_arrival_plot()
    annual_population_arrival_plot()

    # conclusion
    conclusion = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
        <p>
        In conclusion, we observed a drastic drop on Adélie penguin's population. In addition, the arrival rate of Adélie penguin
        to Humble island drops as well over years. We are curious about the reason for such decrease. Thus, we'll explore 
        multiple possible explanations in Reproduction and Environment/Ecosystem sections.
        </p>
    </body>
    """

    st.markdown(
        conclusion, unsafe_allow_html=True
    )
