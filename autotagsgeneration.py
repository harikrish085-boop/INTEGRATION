import csv
import random

# Output file path
output_file = r"C:\Users\HariKrishna\Desktop\Generated_Sensors.csv"

# Number of entries
num_entries = 5000

# Define CSV headers (same as your original file)
headers = [
    "Tag Name","Address","Data Type","Respect Data Type","Client Access",
    "Scan Rate","Scaling","Raw Low","Raw High","Scaled Low","Scaled High",
    "Scaled Data Type","Clamp Low","Clamp High","Eng Units","Description","Negate Value"
]

# Generate data
rows = []
for i in range(1, num_entries + 1):
    tag_name = f"sensor{i}"
    
    # Random values for Address
    rand1 = random.randint(10, 1000)   # first number
    rand2 = random.randint(-50, 0)     # second number (negative range)
    rand3 = random.randint(50, 1000)   # third number
    
    address = f"RANDOM ({rand1}, {rand2}, {rand3})"
    
    # Fill other columns with defaults similar to your file
    row = [
        tag_name, address, "Long", 1, "RO", 100,
        "", "", "", "", "", "", "", "", "", "", ""
    ]
    rows.append(row)

# Write to CSV
with open(output_file, mode="w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(headers)
    writer.writerows(rows)

print(f"CSV file with {num_entries} entries created at: {output_file}")
