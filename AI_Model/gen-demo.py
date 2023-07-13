import csv
import random

# Path to the original CSV file
original_file = "demo.csv"

# Path to the new CSV file
new_file = "selected_rows.csv"

# Number of rows to select
num_rows = 500

# Read the original CSV file
with open(original_file, "r") as file:
    reader = csv.reader(file)
    header = next(reader)  # Assuming the first row is a header
    rows = list(reader)

# Shuffle the rows
random.shuffle(rows)

# Select the first 100 rows
selected_rows = rows[:num_rows]

# Write the selected rows to a new CSV file
with open(new_file, "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(header)
    writer.writerows(selected_rows)

print("Selected rows have been written to", new_file)