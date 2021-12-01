import streamlit as st
from diet_plot import sea_ice, seaIce_population, superba, total_zooplankton, krill_size

def root():
    # transition:
    header = """
    <b style="font-family:Charter; color:Black; font-size: 40px;">
    Environmental/Ecosystem Factors
    </b>
    """
    st.markdown(header, unsafe_allow_html=True)

    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    We have observed that there is a major population growth rate change of Adélie penguin. 
    Research area has proposed two hypothesis which might explain this change. 

    - One of them suggests that population change can be explained by the changes in regional 
    krill biomass (which, as explained in the introduction section, is the major prey of Adélie penguin).
    - The other suggests that long-term changes in sea ice affect population of Adélie penguin. 
    This proposal comes from the assumption that change of sea ice might tip the balance in favor of those 
    species who have looser requirements for affinities to sea ice.
    </p> 
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )
    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    In this section, we explore multiple datasets to assess two possible hypothesis explained above.
    </p>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )
    # sea ice plot
    sea_ice_header = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    Sea Ice
    </b>
    """
    st.markdown(sea_ice_header, unsafe_allow_html=True)
    plot, info = st.columns((8, 2))
    with info:
        st.info("""
            Usage:
            - Hovered-over lines are highlighted and the correpsonding location is shown in tooltip.
            - Clicking on legend(location) to see the corresponding line highlighted. 
            - Zooming in and out on plot area by scrolling mouse to. Double click the plot area to reset zooming effect.
        """)
    with plot:
        sea_ice()
    # sea ice explanation
    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    This plot measures the annual sea ice area (measured in km^2) in the local areas of Palmer Station.
    We can observe that even though different local areas have different level of sea ice extent, their 
    changes over year behave pretty much the same as each other. This behavior makes sense because the 
    data is based on the close surrounding area of Palmer Station. With this discover, we'll pick one 
    representing line (WAP area) to compare with population change. 
    </p>
    <br>
    <br>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )
    # sea ice vs. population and reproduction
    _, plot, _ = st.columns((0.5, 8, 1.5))
    with plot:
        seaIce_population()
    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    We can clearly observe that there is no clear correlation between population change and sea ice area
    change. Overall, sea ice level stays stable in a certain boundary while the population continues to 
    decrease over the years. 
    </p>
    <p>
    Looking at these two lines more closely, we can observe that in the range of 1994-2001, the change of 
    Adélie penguin is somewhat in accordance with the change of sea ice level. More specifically, though 
    Adélie penguin's population decreases in general, increase in sea ice level can lead to a slight increase
    on population (1994-1995) or can lower the population decrease rate (1998-2000). 
    </p>
    <p>
    Now, let's switch gear to the ecosystem factors, in particular, the major prey of Adélie penguin. The next 
    section will explore the change of prey amount (measured in weight and size) over the year. 
    </p>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )
    # zooplankton + diet plot
    diet_header = """
    <b style="font-family:Charter; color:Black; font-size: 30px;">
    Diet
    </b>
    """
    st.markdown(diet_header, unsafe_allow_html=True)
    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    Zooplankton are a morphologically and taxonomically diverse group of animals living in Antarctica area, and is the 
    major prey of Adélie penguin. It includes species like Salp, Krill, Limacina, etc. The abundance of zooplankton per 
    1000 meter^3 can provide us an overview of how ecosystem changes over years in the studied area. 
    </p>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )

    info, plot, info2 = st.columns((2, 6.5, 1.5))
    with info:
        st.info("""
        Introduction:
        - Blue bars and blue line indicates the total zooplankton abundance according to year.
        - Red line indicates the population change over year. 
        - Notice that the original zooplankton dataset only includes data from 1993-2004, so we 
        only do the comparison in this range.
        """
        )
    with plot:
        total_zooplankton()
    with info2:
        st.info("""
        Usage:
        - Hover over bar area to see that detailed value of zooplankton abundance in that year.
        """)

    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    In the visualization, we can observe that blue line (abundance of zooplankton) and red line (population)
    fits each other pretty well with only a few exceptions. This indicates that Adélie penguin's population 
    is quite correlated with the amount of their prey. Since the original zooplankton dataset only provides data
    from 1993-2004, while our population data spans more years. Because lack of data on general zooplankton behavior, 
    we decide to focused on exploring more about E. superba, the krill (a species belong to zooplankton) that lives in Antarctica.
    Palmer station provides more detailed data about E. superba. The researchers retrieved samples from an organism's (bird in this study)
    digestive system and drained the samples to measure weights of E. superba obtained. 
    </p>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )

    info, plot = st.columns((3, 7))
    with info:
        st.info("""
        Note: these two visualizations are associated with each other.
        """)
        st.info("""
        Introduction:
        - The first visualization displays the weight of E. superba each year. Since weight is measured per sample, so
        we present it with box-plot to show percentiles. The black line connects all the averages.
        - The second visualization displays the weight of E. superba with its corresponding Penguin's weight (from whom the
        sample was obtained). This plot is filtered based on the selected year in the first plot.
        """)
        st.info("""        
        Usage:
        - Brush over boxplot area to see one or multiple years being selected, and the scatter plot is updated (filtered) accordingly.
        - Drag the selected area left and right to see change over year.
        - Hover over boxplot to see mean value of each year.
        """)
    with plot:
        superba()

    d = """
    <body style="font-family:Charter; color:Black; font-size: 18px;">
    <p>
    We can still observe a general trend that weight of E. superba decreases over the years, which is consistent with
    the trend of population and abundance of zooplankton. Interestingly, we noticed that there is a large variance on E. superba weight
    for each year (box-plot with long tails). Since those samples were retrieved from different birds' digestive system, 
    the weight of E. superba can depend on that individual bird. For example, one hypothesis we had was that larger birds
    (birds with higher weights) tend to consume more E. superba. Thus, we plotted the second visualization to investigate 
    this hypothesis. 
    </p>
    <p>
    Overall, there is no clear positive correlation between birds weights and consumed E. superba weights. Moreover, as 
    we select one or two years, and drag the window left and right to see the filter effect on the second plot, sometimes 
    (e.g 2013-2014) we can even observe negative correlation between birds weights and consumed E. superba weights. This 
    performance might be caused by the small amount of data we get or there are other prey birds consumed which were not included
    in the dataset. 
    </p>
    </body>
    """
    st.markdown(
        d, unsafe_allow_html=True
    )
