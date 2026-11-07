
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.data_loader import get_world_bank_data


# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="QData | Economic Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =====================================================
# 2. COUNTRY AND INDICATOR CONFIGURATION
# =====================================================

COUNTRIES = {
    "Nigeria": "NGA",
    "United States": "USA",
    "United Kingdom": "GBR",
    "South Africa": "ZAF",
    "Ghana": "GHA"
}

INDICATORS = {
    "gdp_growth": {
        "name": "GDP Growth",
        "code": "NY.GDP.MKTP.KD.ZG",
        "unit": "%",
        "format": "percent"
    },
    "inflation": {
        "name": "Inflation",
        "code": "FP.CPI.TOTL.ZG",
        "unit": "%",
        "format": "percent"
    },
    "unemployment": {
        "name": "Unemployment",
        "code": "SL.UEM.TOTL.ZS",
        "unit": "%",
        "format": "percent"
    },
    "gdp_per_capita": {
        "name": "GDP Per Capita",
        "code": "NY.GDP.PCAP.CD",
        "unit": "USD",
        "format": "currency"
    },
    "population": {
        "name": "Population",
        "code": "SP.POP.TOTL",
        "unit": "People",
        "format": "number"
    },
    "fdi": {
        "name": "Foreign Direct Investment",
        "code": "BX.KLT.DINV.WD.GD.ZS",
        "unit": "%",
        "format": "percent"
    }
}


# =====================================================
# 3. CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>

.stApp {
    background-color: #0e1117;
}

[data-testid="stMetric"] {
    background-color: #192331;
    border: 1px solid #30394d;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stMetricValue"] {
    color: #00d4aa;
}

[data-testid="stMetricLabel"] {
    color: #a0aec0;
}

h1, h2, h3 {
    color: #ffffff;
}

.subtitle {
    color: #94a3b8;
    font-size: 14px;
}

.insight {
    background-color: #192331;
    border-left: 4px solid #00d4aa;
    padding: 14px;
    border-radius: 6px;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# 4. DATA RETRIEVAL AND CACHING
# =====================================================

@st.cache_data(ttl=600, show_spinner=False)
def load_indicator(country_code, indicator_code, start_year, end_year):

    return get_world_bank_data(
        country=country_code,
        indicator=indicator_code,
        start_year=start_year,
        end_year=end_year
    )


@st.cache_data(ttl=600, show_spinner=False)
def load_country_data(country_code, start_year, end_year):

    frames = []

    for key, indicator in INDICATORS.items():

        data = load_indicator(
            country_code,
            indicator["code"],
            start_year,
            end_year
        )

        if not data.empty:

            data = data[["year", "value"]].copy()

            data = data.rename(
                columns={"value": key}
            )

            frames.append(data)

    if not frames:
        return pd.DataFrame()

    combined = frames[0]

    for frame in frames[1:]:

        combined = combined.merge(
            frame,
            on="year",
            how="outer"
        )

    return combined.sort_values("year").reset_index(drop=True)


# =====================================================
# 5. HELPER FUNCTIONS
# =====================================================

def latest_observation(data, column):

    if data.empty or column not in data.columns:
        return None

    valid = data.dropna(subset=[column]).sort_values("year")

    if valid.empty:
        return None

    return valid.iloc[-1]


def format_value(value, format_type):

    if format_type == "percent":
        return f"{value:.2f}%"

    if format_type == "currency":
        return f"${value:,.0f}"

    if format_type == "number":
        return f"{value:,.0f}"

    return str(value)


def create_chart(data, key, title, unit):

    chart_data = data[["year", key]].dropna()

    if chart_data.empty:
        st.info(f"No available data for {title}.")
        return

    fig = px.line(
        chart_data,
        x="year",
        y=key,
        markers=True,
        title=title,
        labels={
            "year": "Year",
            key: unit
        }
    )

    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#0e1117",
        plot_bgcolor="#0e1117",
        font_color="white",
        hovermode="x unified",
        margin=dict(l=20, r=20, t=55, b=20)
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# =====================================================
# 6. DASHBOARD HEADER
# =====================================================

st.title("QData Economic Intelligence")

st.markdown(
    '<div class="subtitle">'
    'Global Economic Monitoring | Financial Analytics | '
    'Macroeconomic Research'
    '</div>',
    unsafe_allow_html=True
)

st.divider()


# =====================================================
# 7. SIDEBAR CONTROLS
# =====================================================

st.sidebar.title("Dashboard Controls")

country = st.sidebar.selectbox(
    "Primary Country",
    list(COUNTRIES.keys())
)

year_range = st.sidebar.slider(
    "Historical Period",
    min_value=2000,
    max_value=2025,
    value=(2015, 2025)
)

start_year, end_year = year_range

st.sidebar.divider()

comparison_countries = st.sidebar.multiselect(
    "Countries for Comparison",
    list(COUNTRIES.keys()),
    default=list(COUNTRIES.keys())
)

st.sidebar.divider()

st.sidebar.caption(
    "Source: World Bank Open Data"
)

if st.sidebar.button("Clear Cached Data"):

    st.cache_data.clear()
    st.rerun()


# =====================================================
# 8. LOAD PRIMARY COUNTRY DATA
# =====================================================

country_code = COUNTRIES[country]

with st.spinner(
    f"Loading economic indicators for {country}..."
):

    economic_data = load_country_data(
        country_code,
        start_year,
        end_year
    )


# =====================================================
# 9. MAIN DASHBOARD
# =====================================================

if economic_data.empty:

    st.error(
        "Economic data could not be retrieved."
    )

    st.info(
        "Check your internet connection or try again. "
        "The World Bank API may be temporarily unavailable."
    )

    if st.button("Retry"):

        st.cache_data.clear()
        st.rerun()

else:

    # -------------------------------------------------
    # ECONOMIC PERFORMANCE OVERVIEW
    # -------------------------------------------------

    st.subheader(
        f"Economic Performance Overview: {country}"
    )

    # Six KPI cards, arranged in two rows

    indicator_keys = list(INDICATORS.keys())

    for row_start in range(0, len(indicator_keys), 3):

        columns = st.columns(3)

        for column, key in zip(
            columns,
            indicator_keys[row_start:row_start + 3]
        ):

            indicator = INDICATORS[key]

            latest = latest_observation(
                economic_data,
                key
            )

            with column:

                if latest is not None:

                    value = latest[key]

                    st.metric(
                        indicator["name"],
                        format_value(
                            value,
                            indicator["format"]
                        )
                    )

                    st.caption(
                        f"Reporting year: {int(latest['year'])}"
                    )

                else:

                    st.metric(
                        indicator["name"],
                        "Unavailable"
                    )

    st.divider()


    # -------------------------------------------------
    # HISTORICAL ECONOMIC INDICATORS
    # -------------------------------------------------

    st.subheader("Historical Economic Indicators")

    chart_keys = [
        "gdp_growth",
        "inflation",
        "unemployment",
        "gdp_per_capita",
        "population",
        "fdi"
    ]

    for row_start in range(0, len(chart_keys), 2):

        columns = st.columns(2)

        for column, key in zip(
            columns,
            chart_keys[row_start:row_start + 2]
        ):

            indicator = INDICATORS[key]

            with column:

                create_chart(
                    economic_data,
                    key,
                    indicator["name"],
                    indicator["unit"]
                )

    st.divider()


    # =================================================
    # 10. INTERNATIONAL COUNTRY COMPARISON
    # =================================================

    st.subheader("International Economic Comparison")

    st.caption(
        "Compare annual GDP growth across selected countries."
    )

    comparison_data = []

    with st.spinner("Preparing country comparisons..."):

        for selected_country in comparison_countries:

            selected_code = COUNTRIES[selected_country]

            data = load_indicator(
                selected_code,
                INDICATORS["gdp_growth"]["code"],
                start_year,
                end_year
            )

            if not data.empty:

                data = data[["year", "value"]].copy()

                data["country"] = selected_country

                comparison_data.append(data)

    if comparison_data:

        comparison_df = pd.concat(
            comparison_data,
            ignore_index=True
        )

        comparison_fig = px.line(
            comparison_df,
            x="year",
            y="value",
            color="country",
            markers=True,
            title="GDP Growth Comparison",
            labels={
                "year": "Year",
                "value": "GDP Growth (%)",
                "country": "Country"
            }
        )

        comparison_fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0e1117",
            plot_bgcolor="#0e1117",
            hovermode="x unified"
        )

        st.plotly_chart(
            comparison_fig,
            use_container_width=True
        )

        st.dataframe(
            comparison_df.pivot(
                index="year",
                columns="country",
                values="value"
            ).round(2),
            use_container_width=True
        )

    else:

        st.info(
            "No comparison data available for the selected countries."
        )

    st.divider()


    # =================================================
    # 11. CORRELATION ANALYSIS
    # =================================================

    st.subheader("Economic Indicator Correlation Analysis")

    st.caption(
        "Explore statistical relationships between "
        "the selected country's economic indicators."
    )

    correlation_columns = [
        key for key in INDICATORS
        if key in economic_data.columns
        and economic_data[key].notna().sum() >= 3
    ]

    if len(correlation_columns) >= 2:

        correlation_matrix = economic_data[
            correlation_columns
        ].corr(min_periods=3)

        correlation_matrix = (
            correlation_matrix
            .dropna(axis=0, how="all")
            .dropna(axis=1, how="all")
        )

        if not correlation_matrix.empty:

            correlation_matrix = correlation_matrix.rename(
                columns={
                    key: INDICATORS[key]["name"]
                    for key in correlation_matrix.columns
                },
                index={
                    key: INDICATORS[key]["name"]
                    for key in correlation_matrix.index
                }
            )

            correlation_fig = px.imshow(
                correlation_matrix,
                text_auto=".2f",
                color_continuous_scale="RdBu",
                zmin=-1,
                zmax=1,
                aspect="auto",
                title=f"{country} Economic Correlation Matrix"
            )

            correlation_fig.update_layout(
                template="plotly_dark",
                paper_bgcolor="#0e1117",
                font_color="white"
            )

            st.plotly_chart(
                correlation_fig,
                use_container_width=True
            )

            st.caption(
                "Correlation ranges from -1 to +1. "
                "Positive values indicate positive association; "
                "negative values indicate negative association. "
                "Correlation does not establish causation."
            )

        else:

            st.info(
                "Insufficient overlapping observations "
                "for correlation analysis."
            )

    else:

        st.info(
            "At least two indicators with sufficient observations "
            "are needed for correlation analysis."
        )

    st.divider()


    # =================================================
    # 12. AUTOMATED ECONOMIC INSIGHTS
    # =================================================

    st.subheader("Automated Economic Insights")

    gdp_latest = latest_observation(
        economic_data,
        "gdp_growth"
    )

    inflation_latest = latest_observation(
        economic_data,
        "inflation"
    )

    unemployment_latest = latest_observation(
        economic_data,
        "unemployment"
    )

    if gdp_latest is not None:

        value = gdp_latest["gdp_growth"]
        year = int(gdp_latest["year"])

        if value > 0:

            message = (
                f"{country} recorded economic growth of "
                f"{value:.2f}% in {year}."
            )

        elif value < 0:

            message = (
                f"{country} recorded an economic contraction of "
                f"{abs(value):.2f}% in {year}."
            )

        else:

            message = (
                f"{country} recorded zero GDP growth in {year}."
            )

        st.markdown(
            f'<div class="insight">{message}</div>',
            unsafe_allow_html=True
        )

    if inflation_latest is not None:

        value = inflation_latest["inflation"]
        year = int(inflation_latest["year"])

        if value >= 10:

            interpretation = "elevated inflation"

        elif value >= 5:

            interpretation = "moderate inflation"

        else:

            interpretation = "relatively low inflation"

        message = (
            f"Inflation was {value:.2f}% in {year}, "
            f"indicating {interpretation} under this dashboard's "
            f"simple classification."
        )

        st.markdown(
            f'<div class="insight">{message}</div>',
            unsafe_allow_html=True
        )

    if unemployment_latest is not None:

        value = unemployment_latest["unemployment"]
        year = int(unemployment_latest["year"])

        message = (
            f"The reported unemployment rate was "
            f"{value:.2f}% in {year}."
        )

        st.markdown(
            f'<div class="insight">{message}</div>',
            unsafe_allow_html=True
        )


    st.divider()


    # =================================================
    # 13. HISTORICAL DATA AND EXPORT
    # =================================================

    st.subheader("Economic Data Explorer")

    display_data = economic_data.copy()

    display_data = display_data.rename(
        columns={
            key: INDICATORS[key]["name"]
            for key in INDICATORS
            if key in display_data.columns
        }
    )

    st.dataframe(
        display_data,
        use_container_width=True,
        hide_index=True
    )

    csv_data = economic_data.to_csv(
        index=False
    ).encode("utf-8")

    st.download_button(
        label="Download Economic Dataset (CSV)",
        data=csv_data,
        file_name=(
            f"{country.lower().replace(' ', '_')}_"
            "economic_data.csv"
        ),
        mime="text/csv"
    )


# =====================================================
# 14. FOOTER
# =====================================================

st.divider()

st.caption(
    "QData Economic Intelligence | "
    "Built with Python, Streamlit, Pandas and Plotly | "
    "Data Source: World Bank Open Data"
)
