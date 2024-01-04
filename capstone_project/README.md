# Capstone Project

## Identifying the Data Source

I have selected data provided by the Australian Bureau of Statistics about the
following areas:

- [Overseas Migration](https://www.abs.gov.au/statistics/people/population/overseas-migration/2022-23-financial-year)
- [Labour Force](https://www.abs.gov.au/statistics/labour/employment-and-unemployment/labour-force-australia/nov-2023)
- [Housing Occupancy and Costs](https://www.abs.gov.au/statistics/people/housing/housing-occupancy-and-costs/2019-20)
- [Total Value of Dwellings](https://www.abs.gov.au/statistics/economy/price-indexes-and-inflation/total-value-dwellings/latest-release#:~:text=The%20number%20of%20residential%20dwellings%20in%20Australia%20rose%20by%2052%2C300,%2419%2C200%20to%20%24925%2C400%20this%20quarter.)

Most of the data is available in MS Excel format, which makes it somewhat
straightforward to work with.

Recent news and forum discussions regarding the influence of international
migration on Australia's job and housing markets have piqued my curiosity. I am
keen on analysing data to uncover potential correlations that may connect
international migration with trends in these markets.

As an international migrant, I am personally invested in understanding how
Australia's migration policies and the influx of immigrants impact the country's
economy.

I intend to perform the following analysis with this data:

- **Database Integration:** Import the data into a database for efficient
  querying and analysis.
- **Visualization:** Generate maps, charts, and graphs to represent migration
  and economic data.
- **Economic Impact Analysis:** Understand the economic impact of migration on
  housing and job markets.
- **Correlation Analysis:** Identify potential correlations between migration,
  labour force, and housing data.
- **Predictive Modelling:** Predict housing demand and occupancy, as well as job
  offerings, based on migration patterns.

## Analysing a Data Source

Upon further investigation, I discovered that the data is available through an
API provided by the Australian Bureau of Statistics. This makes it easier to
integrate the data into a database and perform analysis. The API provides an XML
response.

After trying to build an API request on my own, I discovered that the Australian
Bureau of Statistics provides a tool to explore data,
[Stat Data Explorer](https://explore.data.abs.gov.au/). What's cool about this
tool is that it allows a visual inspection of the data and generates the
corresponding API request for the selected data.

I decided to not use the data I initially identified in MS Excel files and use
this tool to select the most interesting data sets for my intended analysis:

- Net Overseas Migration (per state)

  - Dataset: Net overseas migration, Arrivals, departures and net,
    State/territory, Age and sex - Calendar years, 2004 onwards
  - Measure: Net Overseas Migration
  - Age: All ages
  - Sex: Persons (no sex disaggregation)
  - Region: Australia and Australian states
  - Frequency: Annual
  - Unit of measure: Number
  - Data visualisation:
    ```
    https://explore.data.abs.gov.au/vis?tm=Migration&pg=0&df[ds]=ABS_ABS_TOPICS&df[id]=NOM_CY&df[ag]=ABS&df[vs]=1.0.0&pd=2004%2C&dq=3.TOT.3..A&ly[cl]=TIME_PERIOD
    ```
  - API request:
    ```
    https://api.data.abs.gov.au/data/ABS,NOM_CY,1.0.0/3.TOT.3..A?startPeriod=2004
    ```

- Employment to population ratio (per state)

  - Dataset: Labour Force
  - Measure: Employment to population ratio
  - Sex: Persons (no sex disaggregation)
  - Age: Total (age)
  - Adjustment Type: Seasonally Adjusted
  - Region: Australia and Australian states
  - Frequency: Monthly
  - Unit of measure: Percent
  - Data visualisation:
    ```
    https://explore.data.abs.gov.au/vis?tm=employment%20to%20population%20ratio&pg=0&df[ds]=LABOUR_TOPICS&df[id]=LF&df[ag]=ABS&df[vs]=1.0.0&pd=2004-01%2C2023-11&dq=M16.3.1599.20..M&ly[cl]=TIME_PERIOD&hc[Measure]=Employment%20to%20population%20ratio&fs[0]=Labour%2C0%7CEmployment%20and%20unemployment%23EMPLOYMENT_UNEMPLOYMENT%23&fc=Labour
    ```
  - API request:
    ```
    https://api.data.abs.gov.au/data/ABS,LF,1.0.0/M16.3.1599.20..M?startPeriod=2004-01&endPeriod=2023-11
    ```
  - [Information about the Employment to Population Ratio](https://www.investopedia.com/terms/e/employment_to_population_ratio.asp)

- Number of residential dwellings and Mean price of residential dwellings (per
  state)
  - Dataset: Residential Dwellings: Values, Mean Price and Number by State and
    Territories
  - Region: Australia and Australian states
  - Frequency: Quarterly
  - Measure: Number of residential dwellings
    - Unit of measure: Number, Thousands
  - Measure: Mean price of residential dwellings
    - Unit of measure: Australian Dollars, Thousands
  - Data visualisation:
    ```
    https://explore.data.abs.gov.au/vis?tm=Dwellings&pg=0&df[ds]=ECONOMY_TOPICS&df[id]=RES_DWELL_ST&df[ag]=ABS&df[vs]=1.0.0&pd=2011-Q3%2C2023-Q3&dq=5%2B4..Q&ly[rw]=TIME_PERIOD&ly[rs]=MEASURE
    ```
    - API request:
    ```
    https://api.data.abs.gov.au/data/ABS,RES_DWELL_ST,1.0.0/5+4..Q?startPeriod=2011-Q3&endPeriod=2023-Q3
    ```

As the data contains different measures and frequencies, some cleanup and
normalisation will be required to analyse it correctly.

### Building a data fetching script

I started by building the Python script (`data_getter.py`) to get the data from
the Australian Bureau of Statistics API endpoints. As the data is available in
XML format, I used the `xml.etree.ElementTree` module to parse the XML response.

I decided to consider the period from 2011 to 2022 for the analysis. This is
because the data for the number of residential dwellings is only available from
2011 onwards, and the is no migration data for 2023 yet.

Once the XML data is parsed, I insert it into a SQLite database
(`capstone.sqlite`). I decided to use SQLite because it is lightweight and easy
to use (and the database that we have been using throughout the course).

### Building a data normalisation script

After fetching the data, I noticed that the data is not normalised. For example,
the number of residential dwellings is available in quarters, while the
employment ratio is available in months. I decided to normalise the data to
years, as is the case with migrations data.

I built another Python script (`data_normaliser.py`) to normalise the data. This
script also performs a data insertion into a "clean" database
(`capstone_normalised.sqlite`). This database will be used for the analysis and
visualisation of the data.

## Data Analysis and Visualization

Once the data is normalised, I can start performing some analysis and
visualization.

I started by getting basic statistics about the data. I built a Python script
(`data_stats.py`) to get the following statistics:

- Migration
  - Year with highest migration
  - Year with lowest migration
  - Average Migration per year
  - Average Migration per state
- Employment ratio
  - Year with highest employment ratio
  - Year with lowest employment ratio
  - Average employment ratio per year
  - Average employment ratio per state
- Dwellings (quantity)
  - Year with highest dwellings number
  - Year with lowest dwellings number
  - Average dwellings number per year
- Dwellings (price)
  - Year with highest dwelling price
  - Year with lowest dwelling price
  - Average dwelling price per year
