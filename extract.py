import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np


def yearly_data(year):
    url = f"https://www.cmfri.org.in/{year}"
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.content, "html.parser")
        data = {}
        table = soup.find("table")
        if table:
            for row in table.find_all("tr")[1:]:
                cols = row.find_all("td")
                if len(cols) >= 2:
                    species = cols[1].text.strip().upper()
                    landings = cols[2].text.strip().replace(",", "")
                    try:
                        data[species] = float(landings)
                    except ValueError:
                        continue
        return data
    except Exception as e:
        print(f"Error fetching {year}: {e}")
        return {}


years = list(range(2015, 2025))
all_data = {year: yearly_data(year) for year in years}

df = pd.DataFrame(all_data)

species = df[2024].sort_values(ascending=False).head(15).index
final_df = df.loc[species, years]
print(final_df.shape)
print(final_df)
