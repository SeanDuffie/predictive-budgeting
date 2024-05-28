import pandas as pd
import numpy as np

nas = pd.read_csv(filepath_or_buffer="nasdaq_screener_1716918676853.csv")
print(nas)

print("\nUnique Sectors")
for i, sector in enumerate(nas.Sector.unique()):
    sector_vals = np.array([])

    ind = nas[nas["Sector"] == sector]
    for j, industry in enumerate(ind.Industry.unique()):
        industry_vals = np.array([])

        com = nas[nas["Industry"] == industry]
        for company in com.Symbol.unique():
            try:
                current = float(nas.loc[nas["Symbol"] == company].reset_index()["% Change"][0].replace("%", ""))
                industry_vals = np.append(industry_vals, current)
                sector_vals = np.append(sector_vals, current)
            except KeyError:
                pass

        if len(industry_vals) == 0:
            industry_avg = 0
        else:
            industry_avg = np.average(industry_vals)
        print(f"\t{j}) {industry} | {industry_avg}")
        # print(f"\t\t{industry_vals}")

    if len(sector_vals) == 0:
        sector_avg = 0
    else:
        sector_avg = np.average(sector_vals)
    print(f"{i}) {sector} | {sector_avg}\n")
    # print(f"\t{sector_vals}")
