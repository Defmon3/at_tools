# ADTECH Data Processing Tools

First all you want to create a working directory

```bash
mkdir at_tools
cd at_tools
```

## Prerequisites

Make sure you have `python3` and `pip` installed on your system. You can install them using the following commands:

```bash
sudo apt-get install python3 -y && sudo apt-get install python3-pip -y
``` 

Ensure you have `git` installed on your system. You can install `git` using the following command:

```bash
sudo apt-get install git -y
```

## Getting Started

1. **Clone the repository** to get the scripts:

```bash
git clone https://github.com/Defmon3/at_tools.git
```

2. **Install required packages** for the scripts. Some scripts may need external add-ons or packages to function
   correctly. Install them by running:

```bash
pip install -r requirements.txt
```

This directory includes a collection of scripts tailored for processing ADTECH data from LIGHTHOUSE.

## Scripts Description

### `find_in_files.py`

- **Purpose**: Compares a specific field across different locations within LIGHTHOUSE. Ideal for identifying common
  entities across selected polygons, such as finding devices observed at all selected sites.
- **Usage**: After exporting and unzipping your data, you'll find an "analysis" folder with files for each polygon.
  These files list unique field values, sorted by frequency, to facilitate comparison.
- **Execution**:```python find_in_files.py <file1.txt> file2.txt>```

### `combine_csv.py`

- **Purpose**: Merges multiple CSV files, accommodating variations in field order or completeness. Useful for
  integrating CSVs from extended periods or differing schemas.
- **Usage**: Directly merge CSVs from different sources or times to create a cohesive dataset.
- **Execution**:```python combine_csv.py <file_1.csv> <file_2.csv> ... <file_n.csv>``` or use the following bash script
  to combine all CSVs in a directory:
    ```bash 
    find <csv_dir> -maxdepth 1 -type f| xargs python3 </path/to/combine_csv.py>
    ```

### `csv-to-json.py`

- **Purpose**: Converts CSV files into JSON format, making the data suitable for databases like BigQuery or
  Elasticsearch. Output: ```<inputfile>.json```
- **Execution**:```python csv-to-json.py <file_1.csv>```

### `location_report.py`

- **Purpose**: Generates reports on device sightings at specified locations, using a list of polygons. Adaptable to
  various points of interest. Output: ```location_report.csv```
-
    - **Usage**: You need to edit the wkt_list manually in ```location_report.py```.
- **Execution**:```python location_report.py```

### `csv-trimmer.py`

- **Purpose**: Streamlines CSV files by removing non-essential fields, focusing on key information such
  as `entity_id`, `event_time`, `latitude`, and `longitude`. Output: ```<inputfile>-slim.csv```
- **Execution**:```python csv-trimmer.py <file_1.csv>```

### `cluster_adtech.py`

- **Purpose**: Identifies clusters of activity by analyzing device dwell times, aiding in the discovery of significant
  sites like loading zones or rest areas. Output: ```hexes_over_hour.csv``` and ```detailed_dwell_time.csv```
- **Execution**:```python cluster_adtech.py <combined.csv>```

### `eid_search_str.py`

- **Purpose**: Generates a search string for LIGHTHOUSE to locate all `entity_ids` within CSV files in a directory,
  useful for comprehensive entity_id searches. Output: ```eid-ss.txt```
- **Execution**:```python eid_search_str.py <directory>```
