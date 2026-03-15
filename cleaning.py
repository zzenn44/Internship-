import pandas as pd 
import numpy as np

df = pd.read_csv("flight_reroutes.csv")

print(df.head())
print(df.columns.tolist())
print(df.shape)
print(df["origin"].unique())
print(df["destination"].unique())
print(df["original_route"].unique())
print(df["new_route"].unique())

# Generalization for dates
df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period("M").astype(str)

# Redaction of flight number
df["flight_number"] = df["flight_number"].astype(str).str.replace(r"\d", "*", regex=True)

#  Generalization of locations
region_map = {
    "Istanbul": "Middle East",
    "Amman": "Middle East",
    "Doha": "Middle East",
    "Dubai": "Middle East",
    "Tehran": "Middle East",
    "Riyadh": "Middle East",
    "Cairo": "Middle East",
    "Beirut": "Middle East",
    "Abu Dhabi": "Middle East",
    "Kuwait City": "Middle East",
    "Bahrain": "Middle East",
    "Muscat": "Middle East",
    "Karachi": "South Asia",
    "Lahore": "South Asia",
    "Islamabad": "South Asia",
    "Delhi": "South Asia",
    "Mumbai": "South Asia",
    "London": "Europe",
    "Frankfurt": "Europe",
    "Paris": "Europe",
    "Moscow": "Europe",
    "New York": "North America",
    "Los Angeles": "North America",
    "Washington": "North America",
    "Beijing": "East Asia",
    "Singapore": "East Asia",
    "Sydney": "Australia"
}

df["origin"] = df["origin"].map(region_map).fillna("Other")
df["destination"] = df["destination"].map(region_map).fillna("Other")
# Generalization of routes
route_map_original = {
    "Via Strait of Hormuz": "Gulf Route",
    "Via Persian Gulf": "Gulf Route",
    "Direct Gulf route": "Gulf Route",
    "Via Iran/Iraq corridor": "Iran-Iraq Corridor",
    "Via Baghdad FIR": "Iran-Iraq Corridor",

    "Direct Tehran overfly": "Direct Overfly",
    "Direct Middle East overfly": "Direct Overfly"
}

route_map_new = {
    "Via Red Sea–Suez route": "Southern Route",
    "Via Indian Ocean southern route": "Southern Route",
    "Via Egypt–East Africa southern route": "Southern Route",
    "Via Turkey–Kazakhstan northern route": "Northern Route",
    "Via Ankara–Baku corridor": "Northern Route",
    "Via Ashgabat–Almaty route": "Central Asia Route",
    "Via Central Asian detour": "Central Asia Route",
    "Via Jordan–Egypt alternate": "Alternate Route"
}

df["new_route"] = df["new_route"].map(route_map_new).fillna("Other Route")

# Descretization of distance
distance_cols = [
    "original_distance_km",
    "new_distance_km",
    "additional_distance_km"
]

for col in distance_cols:
    df[col] = pd.to_numeric(df[col], errors="coerce")

bins = [0, 1000, 3000, 6000, np.inf]
labels = ["0-1000", "1001-3000", "3001-6000", "6000+"]

for col in distance_cols:
    df[col] = pd.cut(df[col], bins=bins, labels=labels, include_lowest=True)

# Generalization Extra fuel
df["extra_fuel_cost_usd"] = pd.to_numeric(df["extra_fuel_cost_usd"], errors="coerce")

cost_bins = [0, 500, 2000, 5000, np.inf]
cost_labels = ["Low", "Moderate", "High", "Very High"]

df["extra_fuel_cost_usd"] = pd.cut(
    df["extra_fuel_cost_usd"],
    bins=cost_bins,
    labels=cost_labels,
    include_lowest=True
)
# generalizedelay hours

df["delay_hours"] = pd.to_numeric(df["delay_hours"], errors="coerce")

delay_bins = [0, 1, 3, 6, np.inf]
delay_labels = ["0-1 hr", "1-3 hrs", "3-6 hrs", "6+ hrs"]

df["delay_hours"] = pd.cut(
    df["delay_hours"],
    bins=delay_bins,
    labels=delay_labels,
    include_lowest=True
)

# missing values
print(df.isna().sum())
df = df.fillna("Unknown")
df.to_csv("flights_cleaned.csv", index=False)


