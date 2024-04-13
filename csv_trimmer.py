#!/usr/bin/env python3

import argparse
import csv


def process_csv(input_filename: str) -> str:
    output_filename = input_filename.replace(".csv", "-slim.csv")

    desired_fields = {
        'Event Time',
        'Advertiser Id',
        'Latitude',
        'Speed',
        'Accuracy Score',
        'Confidence',
        'Longitude',
        'Entity Id'
    }

    with open(input_filename, newline='') as infile, \
            open(output_filename, 'w', newline='') as outfile:
        reader = csv.DictReader(infile)
        writer = csv.DictWriter(outfile, fieldnames=desired_fields)

        writer.writeheader()  # Write the header row
        rows = list(reader)
        for row in rows:
            slim_row = {field: row.get(field, "") for field in desired_fields}
            writer.writerow(slim_row)
        print(f"Processed {len(rows)} rows and wrote to {output_filename}")
        return output_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process CSV data")
    parser.add_argument("filename", help="Path to the CSV file to process")
    args = parser.parse_args()

    process_csv(args.filename)
    print(f"Processed data saved to {args.filename.replace('.csv', '-slim.csv')}")
