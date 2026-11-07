
import requests
import pandas as pd

WORLD_BANK_API = "https://api.worldbank.org/v2"


def get_world_bank_data(country, indicator, start_year=2000, end_year=2025):
    """
    Retrieve economic indicator data from the World Bank API.
    Returns a Pandas DataFrame.
    """

    url = (
        f"{WORLD_BANK_API}/country/{country}/indicator/{indicator}"
        f"?date={start_year}:{end_year}&format=json&per_page=1000"
    )

    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()

        result = response.json()

        if len(result) < 2 or result[1] is None:
            return pd.DataFrame()

        records = []

        for item in result[1]:
            if item["value"] is not None:
                records.append({
                    "year": int(item["date"]),
                    "value": item["value"],
                    "country": item["country"]["value"]
                })

        if not records:
            return pd.DataFrame()

        return (
            pd.DataFrame(records)
            .sort_values("year")
            .reset_index(drop=True)
        )

    except requests.exceptions.RequestException as e:
        print(f"World Bank API connection error: {e}")
        return pd.DataFrame()

    except (ValueError, KeyError, TypeError) as e:
        print(f"Data processing error: {e}")
        return pd.DataFrame()


# Test the data loader independently
if __name__ == "__main__":

    data = get_world_bank_data(
        country="NGA",
        indicator="NY.GDP.MKTP.KD.ZG",
        start_year=2015,
        end_year=2025
    )

    if data.empty:
        print("No data retrieved. Check your internet connection.")
    else:
        print("\nNigeria GDP Growth Data")
        print(data.to_string(index=False))
