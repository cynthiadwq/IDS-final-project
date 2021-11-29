import streamlit as st
import altair as alt
import pandas as pd

WIDTH = 1000
HEIGHT = 400

#### Utils ####


@st.cache(persist=True)
def load_and_clean_chick_count_data():
    cc_df = pd.read_csv("EDA/Adelie Penguin Chick Counts.csv",
                        engine='python')
    cc_df['Adult Pairs'] = cc_df['Adults']
    cc_df['Adults'] = cc_df['Adult Pairs'] * 2
    cc_df['Total Population'] = cc_df['Adults'] + cc_df['Chicks']
    cc_df['Date'] = pd.to_datetime(cc_df['Date GMT'])
    cc_df['Island'] = cc_df['Island'].str.rstrip()
    cc_df['Island'] = cc_df['Island'].str.lstrip()
    total_counts_per_year_per_island = cc_df.groupby(
        [cc_df['Date'].dt.year, cc_df['Island']]
    ).agg({
        'Adults': 'sum',
        'Chicks': 'sum',
        'Total Population': 'sum'})
    total_counts_per_year_per_island = total_counts_per_year_per_island.reset_index()
    total_counts_per_year = cc_df.groupby(
        cc_df['Date'].dt.year
    ).agg({
        'Adults': 'sum',
        'Chicks': 'sum',
        'Total Population': 'sum'}
    )
    return (total_counts_per_year_per_island, total_counts_per_year)


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
    single_egg_info['Chick is Creche'] = (
        single_egg_info['Chick Creche Date'] != 0)

    single_egg_info_on_humble_by_year = single_egg_info.groupby(['Year']).agg({
        'Egg is Laid': 'sum',
        'Egg is Lost': 'sum',
        'Chick is Hatched': 'sum',
        'Chick is Lost': 'sum',
        'Chick is Creche': 'sum',
    }).reset_index()
    single_egg_info_on_humble_by_year['Percentage of Egg Loss'] = single_egg_info_on_humble_by_year['Egg is Lost'] / \
        single_egg_info_on_humble_by_year['Egg is Laid']

    single_egg_info_on_humble_by_year['Percentage of Chick Loss'] = single_egg_info_on_humble_by_year['Chick is Lost'] / \
        single_egg_info_on_humble_by_year['Chick is Hatched']
    single_egg_info_on_humble_by_year['Percentage of Chick Creche'] = single_egg_info_on_humble_by_year['Chick is Creche'] / \
        single_egg_info_on_humble_by_year['Chick is Hatched']

    return single_egg_info_on_humble_by_year

#### Component ####


def adult_and_chicks(total_counts_per_year_per_island):
    select_year = alt.selection_single(
        name='select',
        fields=['Date'],
        init={'Date': 1992},
        bind=alt.binding_range(min=1992, max=2018, step=1)
    )
    plot_data1 = total_counts_per_year_per_island.copy()
    plot_data1['Category'] = 'Adults'
    plot_data1['Count'] = plot_data1['Adults']
    plot_data1 = plot_data1.drop(
        columns=['Adults', 'Chicks', 'Total Population']
    )
    plot_data2 = total_counts_per_year_per_island.copy()
    plot_data2['Category'] = 'Chicks'
    plot_data2['Count'] = plot_data2['Chicks']
    plot_data2 = plot_data2.drop(
        columns=['Adults', 'Chicks', 'Total Population']
    )
    plot_data = plot_data1.append(plot_data2)
    print(plot_data)
    # pie_chart_data = total_counts_per_year_per_island.melt()
    # chart = alt.Chart(pie_chart_data).encode(
    #   alt.Theta(field="Total Population", type="quantitative"),
    #   color=alt.Color(field="Island", type="nominal"),
    # ).add_selection(select_year).transform_filter(select_year)
    # chart
    chart = alt.Chart(plot_data).mark_bar().encode(
        x='Count:Q',
        y='Category:O',
        color='Category:N',
        row='Island:N'
    )
    # .add_selection(select_year).transform_filter(select_year).interactive()
    st.altair_chart(chart)


def nest_info(chick_brood_info_per_year_per_island):
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
        titleFontSize=15
    ).properties(
        width=WIDTH,
        height=HEIGHT,
        title="Nests with Chicks on Each Island over Time",
    ).interactive()

    st.altair_chart(chart)


def egg_and_chick_info(single_egg_info_on_humble_by_year):
    # Refer to https://altair-viz.github.io/gallery/multiline_tooltip.html
    source1 = single_egg_info_on_humble_by_year.melt('Year',
                                                     value_vars=[
                                                         'Egg is Laid',
                                                         'Egg is Lost',
                                                         'Chick is Hatched',
                                                         'Chick is Lost',
                                                         'Chick is Creche'
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
        color=alt.Color('variable:N', scale=alt.Scale(scheme='tableau20'))
    )

    # Draw points on the line, and highlight based on selection
    points = line.mark_point().encode(
        # opacity=alt.condition(nearest, alt.value(1), alt.value(0))
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

    hist = base.mark_bar().encode(
        x=alt.X('variable:N',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('value:Q',
                axis=alt.Axis(title="Quantity")
                ),
        color=alt.Color('variable:N', scale=alt.Scale(scheme='tableau20'))
    ).transform_filter(
        nearest
    ).properties(
        width=WIDTH,
        height=HEIGHT/2
    )

    text = hist.mark_text(
        align='center',
        baseline='middle',
        dx=0,
        dy=-5,
    ).encode(
        text='value:Q'
    )

    combined_chart = alt.vconcat(
        line_chart, hist+text
    )
    st.altair_chart(combined_chart)


###### main program ######
st.header("Reproduction Info")
(total_counts_per_year_per_island,
 total_counts_per_year) = load_and_clean_chick_count_data()
# adult_and_chicks(total_counts_per_year_per_island)

st.subheader("Nests with Chicks on Each Island over Time")
(chick_brood_info_per_year_per_island,
 chick_brood_info_per_year) = load_and_clean_nest_data()
nest_info(chick_brood_info_per_year_per_island)

st.subheader("Egg and Chick Info on Humble Island")
single_egg_info_on_humble_by_year = load_and_clean_egg_and_chick_data()
egg_and_chick_info(single_egg_info_on_humble_by_year)
