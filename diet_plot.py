import streamlit as st
import altair as alt
import pandas as pd


def seaIce_population():
    ice = pd.read_csv("EDA/Annual Sea Ice.csv")
    ice = ice[(ice["Year"] >= 1993) & (ice["Year"] <= 2017)].reset_index(drop=True)
    ice_plot = ice.melt(id_vars=["Year"],
                         var_name="Location",
                         value_name="Area")
    ice_plot = ice_plot[ice_plot["Location"] == "WAP_Area"]
    df = pd.read_csv("EDA/Adelie Penguin Census.csv")
    df["Date"] = pd.to_datetime(df["Date GMT"])
    df["Adults"] = 2 * df["Breeding Pairs"]
    df["Year"] = df["Date"].dt.year
    adult_count_year_data = df.groupby(df["Year"], as_index=False)["Adults"].sum()
    adult_count_year_data = adult_count_year_data[(adult_count_year_data["Year"] >=1993) & (adult_count_year_data["Year"] <=2017)]
    plot_data = ice_plot.merge(adult_count_year_data, how='inner', on="Year")

    base = alt.Chart(plot_data).encode(
        alt.X('Year:O', axis=alt.Axis(title=None, labelAngle=0))
    )

    population = base.mark_line(point=True, interpolate='cardinal', stroke='#5276A7').encode(
        alt.Y("Adults:Q", axis=alt.Axis(title='Adults Count', titleColor='#5276A7', labelColor='#5276A7', grid=True))
    )

    ice_line = base.mark_line(point=True, interpolate='cardinal', stroke='#57A44C').encode(
        alt.Y("Area:Q", axis=alt.Axis(title="Sea Ice Area(km^2)", titleColor='#57A44C', labelColor='#57A44C', grid=True))
    )

    chart = alt.layer(population, ice_line).resolve_scale(
        y = 'independent'
    ).properties(
        width=1000,
        height=450
    )
    st.altair_chart(chart)



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
        y=alt.Y('Area:Q', axis=alt.Axis(title="Sea Ice Area(km^2)")),
        color=alt.Color('Location', scale=alt.Scale(scheme='tableau20')),
        tooltip='Location'
    )

    points = base.mark_circle().encode(
        opacity=alt.value(1)
    ).add_selection(
        highlight
    )

    lines = base.mark_line(interpolate='cardinal').encode(
        size=alt.condition(~highlight, alt.value(1), alt.value(4))
    )

    chart = alt.layer(points+lines)\
    .configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    ).properties(
        width=900,
        height=400
    ).configure_axis(
        titleFontSize=15
    ).interactive()

    st.altair_chart(chart)

# st.subheader("E. superba weight vs. Year")

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
            y=alt.Y('min:Q', title="E superba weight (g)", scale=alt.Scale(domain=[50, 800])),
            y2=alt.Y2('max:Q', title="E superba weight (g)")
        ),
        alt.Chart().mark_bar(width=15).encode(
            y=alt.Y('q1:Q', title="E superba weight (g)", scale=alt.Scale(domain=[50, 800])),
            y2=alt.Y2('q3:Q', title="E superba weight (g)"),
            color=alt.condition(brush, alt.Color('year:Q', scale=alt.Scale(scheme='spectral')), alt.value("lightgray"))
        ),
        alt.Chart().mark_line(color='black').encode(
            y=alt.Y("mean:Q", title="E superba weight (g)", scale=alt.Scale(domain=[50, 800]))
        )
    ).add_selection(
        brush
    ).properties(
        width=700,
        height=300
    )
    box = box.encode(x=alt.X('year:Q', scale=alt.Scale(domain=[1993, 2018])))


    plot_data = plot_data.rename(columns={"E. superba Weight (g)": "E superba weight (g)"})
    scatter = alt.Chart(plot_data).mark_circle().encode(
        x=alt.X("Bird Weight (g):Q", scale=alt.Scale(zero=False)),
        y="E superba weight (g):Q",
    ).transform_filter(
        brush
    ).properties(
        width=700,
        height=300
    )

    regression_line = scatter.transform_regression("Bird Weight (g)", "E superba weight (g)").mark_line()

    chart = alt.vconcat(box, scatter+regression_line
    ).configure_title(
        fontSize=30
    ).configure_axis(
        grid=False
    ).configure_view(
        strokeWidth=0
    )
    st.altair_chart(chart)


def krill_size():
    # transform data
    krill = pd.read_csv("EDA/krill_info.csv")
    krill = krill.drop(["Sample Number", "Total Number", "month", "Date", "index"], axis=1)
    plot_data = krill.melt(id_vars=["year"],
                         var_name="size category",
                         value_name="count")
    plot_data = plot_data[plot_data["size category"] != "61-65mm"]
    selection = alt.selection_multi(fields=['size category'], bind='legend')
    highlight = alt.selection_multi(on='mouseover',
                                    fields=['size category'], nearest=True, bind='legend')

    chart = alt.Chart(plot_data).mark_area().encode(
        alt.X('year:O', axis=alt.Axis(labelAngle=0)),
        alt.Y('sum(count):Q', stack='center'),
        alt.Color('size category:N', scale=alt.Scale(scheme='tableau10')),
        opacity=alt.condition(highlight, alt.value(1), alt.value(0.2))
    ).add_selection(
        highlight
    ).properties(
        width=1000,
        height=450
    ).configure_axis(
        titleFontSize=15
    ).interactive()

    st.altair_chart(chart)

def load_and_clean_zooplankton_data():
  raw_z_df = pd.read_csv("EDA/Zooplankton Abundances.csv", engine="python")
  # Processing column
  z_df = raw_z_df.copy()

  z_df['Year'] = pd.to_datetime(z_df['col_2631'], format='%Y')
  z_df['Latitude'] = z_df['col_2635']
  z_df['latitude'] = z_df['Latitude']
  z_df['Longitude'] = z_df['col_2636']
  z_df['longitude'] = z_df['Longitude']
  z_df['Krill'] = z_df['col_2637']
  z_df['Salp'] = z_df['col_2638']
  z_df['Thy'] = z_df['col_2639']
  z_df['Limacina'] = z_df['col_2640']
  z_df['Ecrystallorophias'] = z_df['col_2641']

  z_df['Krill'] = z_df['Krill'].clip(lower=0)
  z_df['Salp'] = z_df['Salp'].clip(lower=0)
  z_df['Thy'] = z_df['Thy'].clip(lower=0)
  z_df['Limacina'] = z_df['Limacina'].clip(lower=0)
  z_df['Ecrystallorophias'] = z_df['Ecrystallorophias'].clip(lower=0)
  z_df['Total Food'] = z_df['Krill'] + z_df['Salp'] + z_df['Thy'] + z_df['Limacina'] + z_df['Ecrystallorophias']

  # Limacina: sea snail babies, on penguin diet: https://en.wikipedia.org/wiki/Sea_butterfly
  # E crystallorophias: antarctic costal krill: https://en.wikipedia.org/wiki/Euphausia_crystallorophias
  # Thysanoessa, a genre of krill: https://en.wikipedia.org/wiki/Thysanoessa
  # `Krill`, `E crystallorophias` and `Thysanoessa` are all under the umbrella of krill,
  # `Salp`: salp can be an important diet source for penguins,
  # this research found diet samples consisting of almost 1/3 of total consumption:https://www.scimex.org/newsfeed/learning-about-penguins-diet-may-save-marine-life,-study-finds2
  z_df['All Krills'] = z_df['Krill'] + z_df['Thy'] +  z_df['Ecrystallorophias']
  z_df['All Other'] = z_df['Salp'] + z_df['Limacina']

  del z_df['col_2630']
  del z_df['col_2631']
  del z_df['col_2632']
  del z_df['col_2633']
  del z_df['col_2634']
  del z_df['col_2635']
  del z_df['col_2636']
  del z_df['col_2637']
  del z_df['col_2638']
  del z_df['col_2639']
  del z_df['col_2640']
  del z_df['col_2641']
  del z_df['col_2642']


  counts_per_year = z_df.groupby(z_df['Year'].dt.year)[
    'Krill', 'Salp', 'Thy', 'Limacina', 'Ecrystallorophias', 'All Krills', 'All Other', 'Total Food'
  ].sum()
  counts_per_year = counts_per_year.reset_index()
  return (z_df, counts_per_year)



def total_zooplankton():
  (_, counts_per_year) = load_and_clean_zooplankton_data()
  total_zooplankton = counts_per_year[['Year', 'Total Food']]

  df = pd.read_csv("EDA/Adelie Penguin Census.csv")
  df["Date"] = pd.to_datetime(df["Date GMT"])
  df["Adults"] = 2 * df["Breeding Pairs"]
  df["Year"] = df["Date"].dt.year
  adult_count_year_data = df.groupby(df["Year"], as_index=False)["Adults"].sum()
  adult_count_year_data = adult_count_year_data[
      (adult_count_year_data["Year"] >= 1993) & (adult_count_year_data["Year"] <= 2004)]
  plot_data = total_zooplankton.merge(adult_count_year_data, how='inner', on="Year")

  base = alt.Chart(plot_data).mark_bar().encode(
    x=alt.X('Year:O', axis=alt.Axis(labelAngle=0)),
    y=alt.Y('Total Food:Q', axis=alt.Axis(title="Total Zooplankton Abundance (num/1000m³)", titleColor="#ADD8E6", labelColor="#ADD8E6")),
  )
  bar = base.encode(
    color=alt.Color('Total Food:Q',scale=alt.Scale(scheme='blues')),
    tooltip=[
      alt.Tooltip('Total Food'),
    ]
  )
  points = base.mark_circle().encode(
    opacity=alt.value(1),
  )
  lines = base.mark_line().encode(
    color=alt.value('lightblue')
  )
  # regression = base.transform_regression(
  #   'Year', 'Total Food', method="linear"
  # ).mark_line(
  # ).transform_fold(
  #    ["reg-line"],
  #    as_=["Regression", "y"]
  # ).encode(
  #   alt.Color("Regression:N", scale=alt.Scale(scheme='reds'))
  # )
  population = base.mark_line(point=True, stroke='#FF5733 ').encode(
      alt.Y("Adults:Q", axis=alt.Axis(title='Adults Count', titleColor='#FF5733', labelColor='#FF5733'))
  )

  chart = alt.layer(bar + lines + points, population).properties(
    width=700,
    height=400
  ).resolve_scale(color='independent', y='independent')
  st.altair_chart(chart)