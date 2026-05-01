import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine


# PAGE CONFIG (must be first streamlit command)
st.set_page_config(
    page_title="Global Literacy Vs Global Economic Condition Analysis",
    layout="wide"
)

st.title("📊 Global Literacy & Education Trends Analysis")

st.subheader("Data-driven insights into global literacy patterns, education access, and economic development.")

st.write("Data Preview")


# DATABASE CONNECTION
engine = create_engine(
    "mysql+pymysql://DB_USERNAME:DB_TOKEN@gateway01.ap-southeast-1.prod.aws.tidbcloud.com:4000/literacy_gdp_analysis",
    connect_args={"ssl": {"ssl": True}}
)


# SIDEBAR NAVIGATION
page = st.sidebar.radio(
    "Navigation",
    ["SQL Query Dashboard", "EDA Visualizations", "Country Profile Page"]
)


# SQL DASHBOARD
if page == "SQL Query Dashboard":

    st.header("SQL Query Dashboard")

    query = st.selectbox(
        "Choose a Query",

        ("Get top 5 countries with highest adult literacy in 2020.",
         "Find countries where female youth literacy < 80%",
         "Average adult literacy per continent (owid region).",
         "Countries with illiteracy % > 20 percent in 2000.",
         "Trend of illiteracy percent for India (2000 to 2020).",
         "Top 10 countries with largest illiterate population in the last year.",
         "Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.",
         "Rank countries by GDP per schooling for the year 2020.",
         "Find global average schooling years per year.",
         "List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling (less than 6).",
         "Show countries where the illiterate population is high despite having more than 10 average years of schooling.",
         "Compare literacy rates and GDP per capita growth for Uruguay over the last 20 years.",
         "Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.")
    )


    if st.button("Run Query"):

        if query == "Get top 5 countries with highest adult literacy in 2020.":
            sql = """
                SELECT country, adult_literacy_rate, year
                FROM adult_youth_df
                WHERE year = 2020
                ORDER BY adult_literacy_rate DESC
                LIMIT 5
                """

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
            df,
            x="country",
            y="adult_literacy_rate",
            color="country",
            title="Top 5 Countries with Highest Adult Literacy (2020)"
             )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Find countries where female youth literacy < 80%":

            sql = """
                select country, year, youth_literacy_rate_female 
                from adult_youth_df
                where youth_literacy_rate_female < 80"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
            df,
            x="country",
            y="youth_literacy_rate_female",
            hover_name="year",
            color="year",
            title="Female Youth Literacy below 80%"
        )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Average adult literacy per continent (owid region).":

            sql = """select owid_region, avg(adult_literacy_rate) as adult_avg_literacy from adult_youth_df group by owid_region"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
                df,
                x="owid_region",
                y="adult_avg_literacy",
                color="adult_avg_literacy",
                title="Average Adult Literacy by Continent"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Countries with illiteracy % > 20 percent in 2000.":

            sql = """select country, year, illiteracy_rate as illiteracy_percentage from illiterate_pop_data where year = 2000 AND illiteracy_rate > 20"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
                df,
                x="country",
                y="illiteracy_percentage",
                hover_data="year",
                title="Countries with Illiteracy >20% in 2000"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Trend of illiteracy percent for India (2000 to 2020).":

            sql = """select country, year, illiteracy_rate from illiterate_pop_data where country = 'India' and year between 2000 and 2020"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.line(
                df,
                x="year",
                y="illiteracy_rate",
                markers=True,
                title="Illiteracy Trend for India"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Top 10 countries with largest illiterate population in the last year.":

            sql = """ select country, year, illiteracy_rate 
            from illiterate_pop_data 
            where year = (select max(year) from illiterate_pop_data) 
            order by illiteracy_rate desc limit 10 """

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
                df,
                x="country",
                y="illiteracy_rate",
                color="country",
                title="Top 10 Countries with Highest Illiteracy Rate"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Find countries with avg_years_schooling > 7 and gdp_per_capita < 5000.":

            sql = """select country, avg_year_edu, gdp_per_capita 
            from gdp_schooling_df where avg_year_edu > 7 and gdp_per_capita < 5000"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.scatter(
                df,
                x="avg_year_edu",
                y="gdp_per_capita",
                hover_name="country",
                color="country",
                title="GDP vs Average Years of Education"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Rank countries by GDP per schooling for the year 2020.":

            sql = """select country, year, gdp_per_capita/avg_year_edu as gdp_per_schooling from gdp_schooling_df where year = 2020 order by gdp_per_schooling desc"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.bar(
                df,
                x="country",
                y="gdp_per_schooling",
                title="GDP per Schooling Ratio"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Find global average schooling years per year.":

            sql = """select year, avg(avg_year_edu) as global_avg_schooling from gdp_schooling_df group by year order by year"""

            df = pd.read_sql(sql, engine)

            st.dataframe(df)

            fig = px.line(
                df,
                x="year",
                y="global_avg_schooling",
                markers=True,   
                title="Global Average Schooling Years Trend"
            )
            st.plotly_chart(fig, use_container_width=True)


        elif query == "List top 10 countries in 2020 with highest GDP per capita but lowest average years of schooling (less than 6).":

            sql = "select country, year, gdp_per_capita, avg_year_edu from gdp_schooling_df where year = 2020 and avg_year_edu < 6 order by gdp_per_capita desc limit 10"
            df = pd.read_sql(sql, engine)
            st.dataframe(df)
            fig = px.scatter(
                df,
                x="avg_year_edu",
                y="gdp_per_capita",
                color="country",
                title="High GDP but Low Schooling Countriesin 2020")
            st.plotly_chart(fig, use_container_width=True)

        elif query == "Show countries where the illiterate population is high despite having more than 10 average years of schooling.":
            sql = "select i.country , i.year, g.avg_year_edu, i.illiteracy_rate  from illiterate_pop_data i join gdp_schooling_df g on g.country = i.country and g.year = i.year where g.avg_year_edu > 10 order by i.illiteracy_rate desc"
            df = pd.read_sql(sql, engine)
            st.dataframe(df)

            fig = px.scatter(df,
                x="avg_year_edu",
                y="illiteracy_rate",
                hover_name="year",
                color="country",
                title="Countries with high illiteracy population despite having 10 Avg years of schooling")
            st.plotly_chart(fig, use_container_width=True)


        elif query == "Compare literacy rates and GDP per capita growth for Uruguay over the last 20 years.":
            sql = """
                SELECT i.country, i.year, i.literacy_rate, g.gdp_per_capita
                FROM illiterate_pop_data i
                JOIN gdp_schooling_df g
                ON g.year = i.year AND g.country = i.country
                WHERE i.country = 'Uruguay'
                AND i.year >= (SELECT MAX(year) - 20 FROM illiterate_pop_data)
                ORDER BY i.year
                """
            df = pd.read_sql(sql, engine)
            st.dataframe(df)

            fig = px.bar(df,
                        x="literacy_rate",
                        y="gdp_per_capita",
                        hover_name="year",
                        title="Uruguay's last 20 years GDP and Literacy Comparison")
            st.plotly_chart(fig, use_container_width=True)          

        
        elif query == "Show the difference between youth literacy male and female rates for countries with GDP per capita above $30,000 in 2020.":
            sql = "select y.country, g.gdp_per_capita, y.youth_literacy_rate_male, y.youth_literacy_rate_female, y.youth_literacy_rate_male - y.youth_literacy_rate_female as literacy_gap from adult_youth_df y join gdp_schooling_df g on g.country=y.country and g.year = y.year where gdp_per_capita > 30000 and y.year = 2020"
            df = pd.read_sql(sql, engine)
            st.dataframe(df)

            fig = px.scatter(df,
                        x="literacy_gap",
                        y="gdp_per_capita",
                        hover_data=["youth_literacy_rate_male", "youth_literacy_rate_female"],
                        color="country",
                        title="Literacy Gap between Male and female")
            st.plotly_chart(fig, use_container_width=True)         


elif page == "EDA Visualizations":
    st.header("EDA Visualizations")
    query = st.selectbox(
        "Choose a Query", 
        ("Distribution of Global Adult Literacy Rates",
         "Distribution of Male Youth Literacy Rates",
         "Female Youth Literacy Rate Spread",
         "Distribution of GDP per Capita",
         "Literacy Growth Over Time",
         "GDP vs Literacy Relationship",
         "Average Years of Education vs Historical Population Across Countries",
         "Average Years of Education vs Literacy",
         "Male vs Female Youth Literacy",
         "Correlation Heatmap")
         )   
    
    

    if st.button("Display Chats"):
        if query == "Distribution of Global Adult Literacy Rates":
            adult_df = pd.read_sql("SELECT * FROM adult_df", engine)
            fig, ax = plt.subplots()
            sns.histplot(adult_df["adult_literacy_rate"], kde=True, ax=ax)
            ax.set_title("Distribution of Global Adult Literacy Rates")
            st.pyplot(fig)
            st.subheader("Insights:")
            st.write("""This distribution chart visualizes how adult literacy rates are spread across different countries.
                        The distribution appears left-skewed, meaning many countries cluster around 80–100% literacy indicating global increment in adult education.
                        The distributions suggest that though the adult literacy improved over the years certain regions still face literacy challenges.""")
            

        elif query == "Distribution of Male Youth Literacy Rates":
            youth_df = pd.read_sql("SELECT * FROM youth_df", engine)
            fig, ax = plt.subplots()
            sns.distplot(youth_df["youth_literacy_rate_male"])
            st.pyplot(fig)
            st.subheader("Insights:")
            st.write("""This chart displays the distribution of literacy rates among young males.
                     Most values falls around 80 - 100 % indicating global increment in youth literacy among males
                     this also suggest widespread access to education for young males.
                     Youth Male literacy is higher compared to adult literacy suggesting that education ratio have improved among the recent generation""")
            

        elif query == "Female Youth Literacy Rate Spread":
            youth_df = pd.read_sql("SELECT * FROM youth_df", engine)
            fig, ax = plt.subplots()
            sns.boxplot(youth_df["youth_literacy_rate_female"])
            st.pyplot(fig)
            st.subheader("Insights:")
            st.write("""This box plot summarizes the spread and variability of female youth literacy rates. 
                     The median literacy rate is high, indicating that most young women have access to education.
                     Gender gaps in education still exist in certain regions, but overall female youth literacy is improving globally.""")
            

        elif query == "Distribution of GDP per Capita":
            gdp_schooling_df = pd.read_sql("SELECT * FROM gdp_schooling_df",engine)
            fig, ax = plt.subplots()
            sns.histplot(gdp_schooling_df["gdp_per_capita"])
            st.pyplot(fig)
            st.subheader("Insights:")
            st.write("""This histogram illustrates the economic distribution of countries based on GDP per capita.
                    The data is skewed toward the right stating most countries fall into lower or middle income levels, while a few countries have extremely high GDP per capita.
                    This indicated the global economic inequality with only a fewer number of country being weathy and falls on the right side of the distribution""")
            

        elif query == "Literacy Growth Over Time":
            literacy_growth = pd.read_sql("SELECT * FROM literacy_growth", engine)
            fig = px.bar(literacy_growth, x="year",
            y="overall_literacy", hover_data = "country",
            title="Literacy Growth Over Time")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""This visualization tracks how literacy rates have changed over time across countries.
                     The plot shows steady upward trend in literacy rates over time.
                     Some countries may show rapid improvements, indicating successful education reforms.
                     This distribution also suggests that global literacy levels have improved over time""")

        
        elif query == "GDP vs Literacy Relationship":
            gdp_schooling_df = pd.read_sql("SELECT * FROM gdp_schooling_df",engine)
            fig = px.scatter(
                gdp_schooling_df,
                x="gdp_per_capita",
                y="literacy_rate", color="country", size="gdp_per_capita",
                title="GDP vs Literacy Relationship")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""This scatter plot explores the relationship between economic development and literacy rates.
                     A positive relation as been observed between GDP and literacy.
                     Countries with higher GDP per capita tend to have higher literacy rates.
                     The chat shows that economic development plays a significant role in improving literacy rates""")


        elif query == "Average Years of Education vs Historical Population Across Countries":
            gdp_schooling_df = pd.read_sql("SELECT * FROM gdp_schooling_df",engine)
            fig = px.scatter(gdp_schooling_df,
                x="population_historical",
                y="avg_year_edu", hover_data="year",color="country",
                title="Average Years of Education vs Historical Population Across Countries")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""The chart shows how population levels relate to the average years of education in different countries.
                        Many countries display increasing education levels as time progresses, reflecting improvements in schooling systems.
                        The visualization suggests that improvements in education tend to occur alongside broader social and demographic development.""")
            

        elif query == "Average Years of Education vs Literacy":
            gdp_schooling_df = pd.read_sql("SELECT * FROM gdp_schooling_df",engine)
            fig = px.scatter(
                    gdp_schooling_df,
                    x="avg_year_edu",
                    y="literacy_rate",color="year",
                    title="Average Years of Education vs Literacy")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""A positive relationship trend is typically observed between average years of schooling and literacy rate.
                        Countries with more years of schooling generally show higher literacy levels.
                        The visualization supports the idea that longer educational exposure contributes to higher literacy rates.""")


        elif query == "Male vs Female Youth Literacy":
            youth_df = pd.read_sql("SELECT * FROM youth_df", engine)
            fig = px.scatter(
                youth_df,
                x="youth_literacy_rate_male",
                y="youth_literacy_rate_female",
                title="Male vs Female Youth Literacy")
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""A strong positive relationship is typically observed between male and female literacy rates.
                        Most countries lie close to the diagonal line, meaning male and female literacy rates are similar.
                        The chart indicates that although many countries have achieved gender parity in youth literacy, gender gaps still exist in some regions.""")


        elif query == "Correlation Heatmap":
            correlation_matrix = pd.read_sql("select * from correlation_matrix", engine)
            fig = px.imshow(
                correlation_matrix,
                text_auto=True,
                color_continuous_scale=[(0, "red"),
                    (0.25, "lightcoral"),
                    (0.5, "orange"),
                    (0.75, "lightgreen"),
                    (1, "green")])
            st.plotly_chart(fig, use_container_width=True)
            st.subheader("Insights:")
            st.write("""The heatmap highlights relationships between different variables such as literacy rate, GDP, and education.
                        Education variables are highly interconnected and play a key role in literacy improvement.
                        Literacy rate and average years of education has a very positive corelation""")

elif page == "Country Profile Page":
    st.title("Country Profile")


    country = st.selectbox(
        "Select Country",
        ('Afghanistan', 'Armenia', 'Bangladesh', 'Belize', 'Bolivia',
       'Brazil', 'Cambodia', 'Cameroon', 'Chile', 'China', 'Colombia',
       'Costa Rica', "Cote d'Ivoire", 'Dominican Republic', 'Ecuador',
       'Egypt', 'El Salvador', 'Eswatini', 'Gambia', 'Ghana', 'Guatemala',
       'Guyana', 'Honduras', 'Indonesia', 'Iran', 'Iraq', 'Jordan',
       'Kenya', 'Kuwait', 'Laos', 'Lesotho', 'Malawi', 'Malaysia', 'Mali',
       'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia',
       'Mozambique', 'Myanmar', 'Nicaragua', 'Niger', 'Pakistan',
       'Panama', 'Paraguay', 'Peru', 'Philippines', 'Russia', 'Rwanda',
       'Saudi Arabia', 'Senegal', 'Singapore', 'South Africa', 'Spain',
       'Sri Lanka', 'Sudan', 'Tanzania', 'Thailand', 'Togo',
       'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Uruguay',
       'Zambia')
    )

    if st.button("Display Country"):
        ['Afghanistan', 'Armenia', 'Bangladesh', 'Belize', 'Bolivia',
       'Brazil', 'Cambodia', 'Cameroon', 'Chile', 'China', 'Colombia',
       'Costa Rica', "Cote d'Ivoire", 'Dominican Republic', 'Ecuador',
       'Egypt', 'El Salvador', 'Eswatini', 'Gambia', 'Ghana', 'Guatemala',
       'Guyana', 'Honduras', 'Indonesia', 'Iran', 'Iraq', 'Jordan',
       'Kenya', 'Kuwait', 'Laos', 'Lesotho', 'Malawi', 'Malaysia', 'Mali',
       'Malta', 'Mauritania', 'Mauritius', 'Mexico', 'Mongolia',
       'Mozambique', 'Myanmar', 'Nicaragua', 'Niger', 'Pakistan',
       'Panama', 'Paraguay', 'Peru', 'Philippines', 'Russia', 'Rwanda',
       'Saudi Arabia', 'Senegal', 'Singapore', 'South Africa', 'Spain',
       'Sri Lanka', 'Sudan', 'Tanzania', 'Thailand', 'Togo',
       'Trinidad and Tobago', 'Tunisia', 'Turkey', 'Uganda', 'Uruguay',
       'Zambia']
        
        query_result = dataset[dataset["country"].isin(selected_country)]
        query_result

