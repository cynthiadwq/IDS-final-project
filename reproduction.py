import streamlit as st
import altair as alt
import pandas as pd

WIDTH = 900
HEIGHT = 400

#### Utils ####
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

    total_counts_per_year = cc_df.groupby(
        cc_df['Year']
    ).agg(
        {'Parents': 'sum', 'Chicks': 'sum', 'Total Population': 'sum'}
    )

    total_counts_per_year = total_counts_per_year.reset_index()
    total_counts_per_year["Chicks to Parents Ratio"] = total_counts_per_year["Chicks"] / total_counts_per_year["Parents"]

    melted = total_counts_per_year.melt(
        id_vars=['Year', "Chicks to Parents Ratio", 'Total Population'], 
        value_vars = ['Parents', 'Chicks'],
        var_name = 'Quantity',
        value_name='Value',
    )
    melted = melted.reset_index()

    return melted

def parent_chick_info():
    melted = load_and_clean_chick_counts()

    base = alt.Chart(melted).encode(
        alt.X('Year:O', axis=alt.Axis(labelAngle=0))
    ).properties(
        width=WIDTH,
        height=HEIGHT
    )

    bar = base.mark_bar().encode(
        y=alt.Y('Value:Q',
                axis=alt.Axis(title="Quantity")
            ),
        color=alt.Color('Quantity:N', scale=alt.Scale(scheme='tableau20')),
        tooltip=['Year:Q',
                 'Quantity:N',
                 'Value:Q',
                 'Total Population:Q',
                 'Chicks to Parents Ratio:Q']
    )

    line =  base.mark_line(color='red').encode(
        y='Chicks to Parents Ratio:Q',
        tooltip=['Year:Q',
                 'Chicks to Parents Ratio:Q']
    )

    points = line.mark_point().encode(
        opacity=alt.value(1)
    )

    combine_graph = alt.layer(bar, line + points).resolve_scale(
        y = 'independent'
    ).configure_axis(
        titleFontSize=20
    )

    st.altair_chart(combine_graph)


@st.cache(persist=True)
def load_and_clean_nest_data():
    chick_brood_df = pd.read_csv(
        'EDA/Adelie Penguin Chick Broods .csv', encoding='unicode_escape',
        skipinitialspace=True)
    chick_brood_df['Year'] = pd.DatetimeIndex(chick_brood_df['Date GMT']).year
    chick_brood_df['Nests with Chicks'] = chick_brood_df['Nests with One Chick'] + \
        chick_brood_df['Nests with Two Chicks']
    # Drop the rows whose 'Nests With Chicks' is greater than 'Nests in Sample' cause it does not make sense
    chick_brood_df = chick_brood_df[chick_brood_df['Nests with Chicks']
                                    <= chick_brood_df['Nests in Sample']]

    # Construct chick brood info per year per island data:
    chick_brood_info_per_year_per_island = chick_brood_df.groupby(
        [chick_brood_df['Year'], chick_brood_df['Island']]
    ).agg({
        'Nests with One Chick': 'sum',
        'Nests with Two Chicks': 'sum',
        'Nests with Eggs': 'sum',
        'Nests with Chicks': 'sum'
    }).reset_index()

    # Construct chick brood info per year:
    chick_brood_info_per_year = chick_brood_df.groupby(
        [chick_brood_df['Year']]
    ).agg({
        'Nests with One Chick': 'sum',
        'Nests with Two Chicks': 'sum',
        'Nests with Eggs': 'sum',
        'Nests with Chicks': 'sum'
    })
    return (chick_brood_info_per_year_per_island, chick_brood_info_per_year)


@st.cache(persist=True)
def load_and_clean_egg_and_chick_data():
    single_egg_info = pd.read_csv("EDA/single_egg.csv")
    # Note that some eggs' loss date is marked at -1, or only the Lay Date Information is available.
    # which means that the study loses track with the egg. So we ignore thoses rows
    single_egg_info = single_egg_info[single_egg_info['Egg Loss Date'] != -1]
    single_egg_info = single_egg_info[~((single_egg_info['Egg Loss Date'] == 0) & (single_egg_info['Chick Hatch Date'] == 0) & (
        single_egg_info['Chick Loss Date'] == 0) & (single_egg_info['Chick Creche Date'] == 0))]
    single_egg_info = single_egg_info[~((single_egg_info['Egg Loss Date'] != 0) & (
        single_egg_info['Chick Hatch Date'] != 0))]
    # Construct correct information to use
    single_egg_info['Egg is Laid'] = True
    single_egg_info['Egg is Lost'] = (single_egg_info['Egg Loss Date'] != 0)
    single_egg_info['Chick is Hatched'] = (
        single_egg_info['Chick Hatch Date'] != 0)
    single_egg_info['Chick is Lost'] = (
        single_egg_info['Chick Loss Date'] != 0)
    single_egg_info['Chick is Crèched'] = (
        single_egg_info['Chick Creche Date'] != 0)

    single_egg_info_on_humble_by_year = single_egg_info.groupby(['Year']).agg({
        'Egg is Laid': 'sum',
        'Egg is Lost': 'sum',
        'Chick is Hatched': 'sum',
        'Chick is Lost': 'sum',
        'Chick is Crèched': 'sum',
    }).reset_index()
    single_egg_info_on_humble_by_year['Percentage of Egg Loss'] = single_egg_info_on_humble_by_year['Egg is Lost'] / \
        single_egg_info_on_humble_by_year['Egg is Laid']

    single_egg_info_on_humble_by_year['Percentage of Chick Loss'] = single_egg_info_on_humble_by_year['Chick is Lost'] / \
        single_egg_info_on_humble_by_year['Chick is Hatched']
    single_egg_info_on_humble_by_year['Percentage of Chick Creche'] = single_egg_info_on_humble_by_year['Chick is Crèched'] / \
        single_egg_info_on_humble_by_year['Chick is Hatched']

    return single_egg_info_on_humble_by_year

#### Component ####
def nest_info():
    (chick_brood_info_per_year_per_island,
     chick_brood_info_per_year) = load_and_clean_nest_data()

    highlight = alt.selection_multi(
        on='mouseover',
        fields=['Island'],
        nearest=True,
        bind='legend'
    )

    base_chart = alt.Chart(chick_brood_info_per_year_per_island).encode(
        x=alt.X('Year:O',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Nests with Chicks:Q',
                axis=alt.Axis(
                    title="Number of Nests with Chicks")),
        color=alt.Color('Island',
                        scale=alt.Scale(scheme='tableau10')),
        tooltip=['Island:N',
                 'Year:Q',
                 'Nests with Chicks:Q']
    )

    points = base_chart.mark_circle().encode(
        opacity=alt.value(1)
    ).add_selection(
        highlight
    )

    lines = base_chart.mark_line(interpolate='cardinal').encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(4))
    )

    chart = alt.layer(points+lines).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).configure_axis(
        titleFontSize=20
    ).properties(
        width=WIDTH,
        height=HEIGHT
    ).interactive()

    st.altair_chart(chart)


def egg_and_chick_info():
    single_egg_info_on_humble_by_year = load_and_clean_egg_and_chick_data()

    # Refer to https://altair-viz.github.io/gallery/multiline_tooltip.html
    source1 = single_egg_info_on_humble_by_year.melt('Year',
                                                     value_vars=[
                                                         'Egg is Laid',
                                                         'Egg is Lost',
                                                         'Chick is Hatched',
                                                         'Chick is Lost',
                                                         'Chick is Crèched'
                                                     ])

    # Create a selection that chooses the nearest point & selects based on x-value
    nearest = alt.selection(
        type='single',
        nearest=True,
        on='mouseover',
        fields=['Year'],
        empty='none'
    )
    base = alt.Chart(source1).properties(
        width=WIDTH,
        height=HEIGHT
    )

    # Transparent selectors across the chart. This is what tells us
    # the x-value of the cursor
    selectors = base.mark_point().encode(
        x='Year:Q',
        opacity=alt.value(0),
    ).add_selection(
        nearest
    )

    # The basic line
    line = base.mark_line(interpolate='cardinal').encode(
        x=alt.X('Year:Q',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('value:Q',
                axis=alt.Axis(
                    title="Quantity")),
        color=alt.Color('variable:N', scale=alt.Scale(
            scheme='tableau20'), title="Variable",)
    )

    # Draw points on the line
    points = line.mark_point().encode(
        opacity=alt.value(1)
    )

    # Draw text labels near the points, and highlight based on selection
    text = line.mark_text(align='left', dx=5, dy=-5).encode(
        text=alt.condition(nearest, 'value:Q', alt.value(' '))
    )

    # Draw a rule at the location of the selection
    rules = base.mark_rule(color='gray').encode(
        x='Year:Q',
    ).transform_filter(
        nearest
    )

    # Put the five layers into a chart and bind the data
    line_chart = alt.layer(
        line, selectors, points, rules, text
    )

    bar_chart = base.mark_bar().encode(
        x=alt.X('variable:N',
                axis=alt.Axis(title="Variable", labelAngle=0)),
        y=alt.Y('value:Q',
                axis=alt.Axis(title="Quantity")
                ),
        color=alt.Color('variable:N', scale=alt.Scale(scheme='tableau20'))
    ).transform_filter(
        nearest
    ).properties(
        width=WIDTH,
        height=HEIGHT*2 / 3
    )

    text = bar_chart.mark_text(
        align='center',
        baseline='middle',
        dx=0,
        dy=-5,
    ).encode(
        text='value:Q'
    )

    combined_chart = alt.vconcat(
        line_chart, bar_chart+text
    ).configure_axis(
        titleFontSize=20
    )

    st.altair_chart(combined_chart)

def run_reproduction():
    # transition:
    header = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
    Reproduction Factor
    </b>
    <body><p></p></body>
    """
    st.markdown(header, unsafe_allow_html=True)

    d1 = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    In the Census section, we have seen that total population of Adélie penguin is decreasing across all 5 islands. 
    <br>
    In this section, we want to further inspect the population change reflected in chicks counts and explore how reproduction factor may contribute to the decline in Adélie penguin population.
    </p> 
    </body>
    """
    st.markdown(
        d1, unsafe_allow_html=True
    )

    st.markdown('---')





    # parent_chick_info info section header
    parent_chick_info_section_header = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    Chicks, Parents, and Chicks-to-Parents Ratio
    </b>
    <body><p></p></body>
    """
    st.markdown(parent_chick_info_section_header, unsafe_allow_html=True)
    # parent_chick_info info graph and usage
    st.info("""
        Usage:
        - A bar has two parts where each part indicate the quantities of Parents penguins and chick penguins respectively. One bar as a whole represents the total popluation of Adélie penguins at a specific year. The corresponding axis for understanding bar values is on th left hand side of the graph.
        - The red line plots out the chicks-to-parents ratio information over time. 
        - If you are interested in the exact values recorded at a given year, a tooltip will be rendered showing full values for all quantities for a specific year.
    """)
    parent_chick_info()
    # parent_chick_info info explanation
    parent_chick_info_explanation = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    The above graph shows the changes in the parent and chick populations on all 5 islands over the past 30 years.
    </p>
    <p>
    We can observe that the overall population for both parents and chicks are decreasing, leading to the decline of overall poplution for Adélie penguin. 
    </p>
    <p>
    More specifically, we can see that more fluctuations occur before 2000, whereas the chicks-to-parent ratio appears more stable in the past decade.
    </p>
    </body>
    """
    st.markdown(parent_chick_info_explanation, unsafe_allow_html=True)
    st.markdown('---')







    # nest info section header
    nest_section_header = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    How does the number of nests with chicks change over time?
    </b>
    <body><p></p></body>
    """
    st.markdown(nest_section_header, unsafe_allow_html=True)
    # nest info intro paragraph
    transition_to_nest_info = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    At a first glace, let's first explore the change in number of nests with chicks.
    </p>
    </body>
    """
    st.markdown(transition_to_nest_info, unsafe_allow_html=True)
    # nest info graph and usage
    info, plot = st.columns((3, 7))
    with plot:
        nest_info()
    with info:
        st.info("""
            Usage:
            - Hovered-over lines are highlighted and the corresponding nest count information for the target island in the specific year is shown in tooltip.
            - Clicking on legend (Island) to see the corresponding line highlighted. 
            - Zooming in and out on plot area by scrolling mouse to. Double click the plot area to reset zooming effect.
        """)
    # nest info explanation
    nest_explanation = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    The above graph shows the change in the number of nests with chicks on all 5 islands over the past 30 years. 
    </p>
    <p>
    We can observe that there is a sharp increase in the number of nests with chicks in 1994 and a sudden drop in 2002. The sharp increase in 1994 aligns with the increase in zooplankton abundance during the same time as various zooplanktons are the main source of food for Adélie penguins (More information can be found in the Environmental/Ecosystem Factors section). However, we did not find an solid explanation for the sudden drop seen in 2002.
    </p>
    <p>
    After 2002, we see a general decline in the number of nests with chicks on all 5 islands, with Humble Island having the most number of nests with chicks among the 5 islands since 2010.
    </p>
    <p>
    Ovevrall, the changes and decline trend seen in the number of nests with chicks align with the general trend we observe in the decrease in the chicks' population.
    </p>
    </body>
    """
    st.markdown(nest_explanation, unsafe_allow_html=True)

    st.markdown('---')




    # egg and chick info section header
    egg_and_chick_section_header = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    What about actual egg and chick counts?
    </b>
    <body><p></p></body>
    """
    st.markdown(egg_and_chick_section_header, unsafe_allow_html=True)
    # intro paragraph
    transition_to_egg_and_chick_info = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    To further inspect the direct change in the number of chicks over time, we explore the Adélie Penguin Reproductive Success dataset which provides a measure of annual breeding chronology, and the number of chicks crèched (an estimate of reproductive success) by collecting daily data from randomly selected parent penguins throughout the breeding season from the time adults arrive until the chick crèche phase of the reproductive cycle. 
    <br>
    Note that crèche (from French) in zoology refers to care of offspring in a group or colony.
    </p>
    </body>
    """
    st.markdown(transition_to_egg_and_chick_info, unsafe_allow_html=True)

    # egg and chick info graph and usage
    st.info("""
        Usage:
        - Hover the mouse over a specific year you are interested into. A gray ruler helps identify all values recorded for that specific year with actual value labels displaying near the corresponding points.
        - The bar chart is linked with the plot by the grey rule: all quantities recorded for the target year are presented as a seperate bar to help visualize the difference among all values..  
    """)
    egg_and_chick_info()

    # egg and chick info explanation
    egg_and_chick_explanation = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    From the above component, it is not hard to see that the trends of number of eggs laid, chicks hatched, and chick creched are almost the same, while we don't see a specific pattern in the number of chicks lost and eggs lost over time.
    </p>
    <p>
    We tried to related information collected in this dataset (which is based on some randomly sampling) with other data recorded about chicks/breeding information on Humble island, but failed to draw a conclusion explaining the sudden increase and small drop in 1997 and 2002 respectively. Therefore, we focus on using the general declining trend in chicks population to explain the change in overal population Adélie penguin.
    </p>
    <p>
    Overall, we reached the following conclusion regarding how reproduction affect the change in Adélie penguin's population: 
    <br>
    Chick penguins in earlier years will grow up and turn into adult penguins in later years. Therefore, as there is a decreasing number of chicks, one can image that the overall popluation base for Adélie penguin is decreasing, resulting in the overal decline in total population.
    </p>
    </body>
    """
    st.markdown(egg_and_chick_explanation, unsafe_allow_html=True)

###### main program ######
