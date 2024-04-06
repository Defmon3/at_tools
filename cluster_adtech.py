#!/usr/bin/env python3

import multiprocessing as mp
import warnings
from datetime import timedelta

import h3
import pandas as pd
from shapely.geometry import Polygon
from tqdm import tqdm

warnings.filterwarnings("ignore")

# --- Constants ---
CSV_FILE = "combined.csv"
OUTPUT_FILE_1 = "hexes_over_hour.csv"
OUTPUT_FILE_2 = "detailed_dwell_time.csv"
H3_RESOLUTION = 8

# --- Load the data ---
print(f"Loading data from {CSV_FILE}")
df_raw = pd.read_csv(CSV_FILE)

# --- Remove all fields except what we need
print(f"Trimming excess data fields")
df = df_raw[['Entity Id', 'Event Time', 'Latitude', 'Longitude']]

# Ensure datetime format  
print(f"Formatting timestamps")
df['Event Time'] = pd.to_datetime(df['Event Time'])

# Sort by "Event Time" in ascending order
print(f"Sorting by timestamp")
df = df.sort_values(by='Event Time')


# --- Functions ---
def get_h3_index(lat, lng, resolution):
    return h3.geo_to_h3(lat, lng, resolution)


def extract_date(dt):
    return dt.date()


def get_wkt_from_h3_index(h3_index):
    poly = Polygon(h3.h3_to_geo_boundary(h3_index, geo_json=True))
    return h3_index, poly


def calculate_consecutive_dwell_time(df):
    # Pre-calculate frequently used values outside the loop 
    df['Date'] = df['Event Time'].dt.date
    df['h3_index'] = df.apply(lambda row: get_h3_index(row['Latitude'], row['Longitude'], H3_RESOLUTION), axis=1)

    # Find changes in entity, date, or hexagon
    change_flags = (df['Entity Id'].shift() != df['Entity Id']) | \
                   (df['Date'].shift() != df['Date']) | \
                   (df['h3_index'].shift() != df['h3_index'])

    # Find gaps using diff & comparisons
    time_diffs = df['Event Time'].diff()
    gap_flags = time_diffs > timedelta(minutes=120)

    # Combine flags to denote start of new segments
    start_flags = change_flags | gap_flags

    # Use cumulative sum to get segment IDs efficiently
    df['segment_id'] = start_flags.cumsum()

    # Calculate start and end times for each segment
    result = df.groupby(['Entity Id', 'Date', 'h3_index', 'segment_id'])['Event Time'].agg(['min', 'max'])
    result['duration'] = (result['max'] - result['min']).dt.total_seconds()

    return result.reset_index()


# --- Chunked Processing (Modified for multiprocessing) ---
def process_group_chunk(group_key, group_df):
    # Important: Any global objects/variables that  'calculate_consecutive_dwell_time'
    # might need must be either passed down  explicitly as arguments or reloaded 
    # within this function
    return calculate_consecutive_dwell_time(group_df)


# --- Group data - Pre-calculate H3 ---
print(f"Calculating H3 hexagon IDs and dates (once, upfront)")
df['h3_index'] = df.apply(lambda row: get_h3_index(row['Latitude'], row['Longitude'], H3_RESOLUTION), axis=1)
df['Date'] = df['Event Time'].dt.date

print(f"Grouping by object, date, and H3 hexagon")
grouped = df.groupby(['Entity Id', 'Date', 'h3_index'])
num_groups = len(grouped)
print(f"Number of groups: {num_groups}")

print(f"Calculating visit duration results")
chunk_size = 5000
all_results = []
num_groups = len(grouped)  # Calculate total groups 

"""for i, (group_key, group_df) in enumerate(tqdm(grouped, total=num_groups)):
    chunk_result = calculate_consecutive_dwell_time(group_df)
    all_results.append(chunk_result)"""

with mp.Pool() as pool:  # Create a process pool
    results = pool.starmap(process_group_chunk, tqdm(grouped, total=num_groups))
    all_results.extend(results)  # Collect results from pool

print(f"Concatenating Results")
filtered = pd.concat(all_results)

print(f"Calculating stats for debugging")
print(filtered['duration'].describe())

print(f"Filtering for dwell times over 1 hour")
filtered = filtered[filtered['duration'] > 3600]  # Filter for over 1 hour
print(filtered)

print(f"Generating WKT values")
# --- Get h3 indexes and WKT ---
filtered[['h3_index', 'WKT']] = filtered.apply(
    lambda row: get_wkt_from_h3_index(row['h3_index']),
    axis=1,
    result_type='expand'
)

print(f"Saving H3/WKT hexagon list")
# --- Save Results ---
filtered[['h3_index', 'WKT']].to_csv(OUTPUT_FILE_1, index=False)

print(f"Saving detailed output")
filtered.to_csv(OUTPUT_FILE_2, index=False)
