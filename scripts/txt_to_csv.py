# convert_single_column.py
import csv
from pathlib import Path

# Edit these paths if needed
input_folder = Path("temp")
output_folder = Path("output")

output_folder.mkdir(parents=True, exist_ok=True)

for txt_path in sorted(input_folder.glob("*.txt")):
    csv_path = output_folder / (txt_path.stem + ".csv")
    with txt_path.open("r", encoding="utf-8", newline="") as fin, \
         csv_path.open("w", encoding="utf-8", newline="") as fout:
        writer = csv.writer(fout, quoting=csv.QUOTE_MINIMAL)
        for raw_line in fin:
            # preserve the line as-is except remove a single trailing newline
            line = raw_line.rstrip("\r\n")
            # write the line as a single-column CSV row (empty line -> empty cell)
            writer.writerow([line])
    print(f"Converted: {txt_path} -> {csv_path}")
