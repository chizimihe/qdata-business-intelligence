# QData Business Intelligence Dashboard

**Economic Intelligence | Financial Analytics | Global Data**

An interactive economic and financial data dashboard built with Python, Streamlit, Pandas, and Plotly. The project demonstrates practical skills in data collection, data processing, exploratory data analysis, and interactive data visualisation.

## Project Overview

The QData Business Intelligence Dashboard provides an interactive platform for exploring key economic indicators across selected countries.

It retrieves real-world economic data from the World Bank API, processes the information using Pandas, and presents the results through interactive charts, KPI metrics, and analytical summaries.

The project was developed to demonstrate the practical application of Python in building interactive business intelligence dashboards.

## Key Features

- **Economic KPI Metrics:** View key indicators, including GDP growth, inflation, unemployment, GDP per capita, population, and foreign direct investment.
- **Interactive Visualisations:** Explore economic trends using interactive Plotly charts.
- **Country Comparison:** Compare GDP growth across multiple countries.
- **Correlation Analysis:** Examine relationships between available economic indicators.
- **Historical Analysis:** Filter economic data by country and year.
- **Automated Insights:** Generate basic observations from the latest available economic figures.
- **Data Export:** Download processed economic datasets in CSV format.
- **Live Data Integration:** Retrieve data from the World Bank API.

## Technologies Used

| Technology | Application |
|---|---|
| Python | Core programming language |
| Streamlit | Interactive dashboard development |
| Pandas | Data manipulation and processing |
| Plotly | Interactive data visualisation |
| Requests | API integration |
| World Bank API | Economic data source |

## Economic Indicators

The dashboard covers the following indicators:

- GDP Growth (%)
- Inflation (%)
- Unemployment (%)
- GDP per Capita (Current US$)
- Population
- Foreign Direct Investment (% of GDP)

## Countries Covered

- Nigeria
- United States
- United Kingdom
- South Africa
- Ghana

## Data Source

Economic data is retrieved from the [World Bank Open Data API](https://data.worldbank.org/).

The availability of individual indicators may vary by country and reporting year.

## Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/chizimihe/qdata-business-intelligence

### 2. Navigate into the project directory

```bash
cd qdata-business-intelligence
```

### 3. Create a virtual environment

```bash
python -m venv venv
```

### 4. Activate the virtual environment

Windows PowerShell:

```bash
venv\Scripts\Activate
```

### 5. Install dependencies

```bash
pip install streamlit pandas plotly requests
```

### 6. Run the dashboard

```bash
streamlit run app.py
```

The dashboard will open in your web browser.

## Project Objectives

This project demonstrates practical experience in:

1. Connecting Python applications to external APIs.
2. Collecting and processing real-world datasets.
3. Building interactive dashboards with Streamlit.
4. Developing data visualisations with Plotly.
5. Presenting KPIs and analytical findings.
6. Comparing datasets across countries.
7. Exporting processed data for further analysis.

## Author

**Chizimihe Modestus Agugo**

Data Analytics | Economic Research | Financial Analytics

- GitHub: https://github.com/chizimihe
- LinkedIn: https://www.linkedin.com/in/chizimihemodestus-agugo-149b27236

---

*QData Business Intelligence — Turning economic data into meaningful insights.*