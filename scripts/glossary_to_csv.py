import csv

# Input text file (the data you pasted should be saved in a .txt file)
input_file = "glossary_holden_william_prg.txt"
output_file = "output.csv"

with open(input_file, "r", encoding="utf-8") as f_in, open(output_file, "w", newline="", encoding="utf-8-sig") as f_out:
    writer = csv.writer(f_out)
    
    for line in f_in:
        # Split by commas but preserve empty fields
        row = line.strip().split(",")
        writer.writerow(row)

print(f"CSV file has been created: {output_file}")
