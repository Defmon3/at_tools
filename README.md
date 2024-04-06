Make sure you have git installed ("sudo apt-get install git -y") a open terminal and run the following command:
git clone https://github.com/Defmon3/at_tools.git

Some of these scripts requires external addons. To install them, run the following command in the terminal:
pip install -r requirements.txt


This directory contains scripts used to process ADTECH data from LIGHTHOUSE.

# Scripts:

**`find_in_files.py`** 
This tool is used when you run an export and compare a field between different locations. To use this, select multiple polygons in LIGHTHOUSE that you want to find common fields between. For example, to find which device has been seen in all the polygons. When you export data from your search, you’ll be able to run a compare operation on one field (e.g. entity_id). When you unzip the results, there will be a folder called “analysis” containing a list of the unique items from the field, each in one file per polygon. This tool will quickly show you all the field values that were seen in more than one file, sorted by frequency. An example of how to use this is to select all known ammunition depots or supply points, run a search, and then compare to see which devices have been traveling to multiple points of interest. 

**`combine_csv.py`**
This script merges two or more CSVs that might not perfectly overlap. This is useful when you have two or more CSVs whose fields might be in different orders, or don’t have the same number of fields. For example, if you search a long period of time and the scheme has changed, some fields could be different. It also works fine to quickly merge a directory of CSVs, which is common in the output of longer LIGHTHOUSE exports.

**`csv-to-json.py`**
Exactly what it says. Useful for loading CSV data into BigQuery, Elastic, etc.

**`location_report.py`**
Uses a list of polygons to represent known ammunition depots, this script quickly summarized when devices were seen at known locations. Feel free to swap out the list of polygons for ones that you’re interested in.

**`csv-trimmer.py`**
This removes excess fields and keeps only the entity_id, event_time, lat, and lon fields. This greatly reduces the size of the CSV file and allows you to handle much longer files than if you use the raw LIGHTHOUSE output.

**`cluster_adtech.py`**
Used to help find clusters of activity where devices in your data have stayed for more than one hour (dwell time). This may help identify bed-down, loading/unloading, or similar locations.

**`eid_search_str.py`**
Takes all CSV files in a directory and generates a search string for lighthouse to find all the entity_ids in the files. 
This is useful when you have a large number of CSVs and want to search for all the entity_ids in them.
