import pandas as pd

nas = pd.read_csv(filepath_or_buffer="nasdaq_screener_1716918676853.csv")
print(nas)

print("\nUnique Sectors")
for i, sector in enumerate(nas.Sector.unique()):
    print(f"\n{i}) {sector}")

    ind = nas[nas["Sector"] == sector]
    for j, industry in enumerate(ind.Industry.unique()):
        print(f"\t{j}) {industry}")
