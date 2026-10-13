import os
import random
import xml.etree.ElementTree as ET

# -------------------------------
# CONFIGURATION
# -------------------------------
# Medical corpora (must keep everything, no trimming)
medical_tmx_files = [
    "en-ko.tmx",
    "en-ko(1).tmx",
    "en-ko(2).tmx",
    "en-ko(3).tmx"  # if missing, script skips
]

# General corpora (used to bulk up, trimmed if necessary)
general_tmx_files = [
    "en-ko(4).tmx",
    "paracrawl-release10v5.en-ko.filter-1.05.tmx"
]

# Output file
output_file = "combined_medical_TM.tmx"

# Desired TU range
MIN_TUS = 100000
MAX_TUS = 500000


# -------------------------------
# FUNCTIONS
# -------------------------------
def read_tmx(filepath):
    """Read TMX and return list of (en, ko) pairs"""
    pairs = []
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for tu in root.findall(".//tu"):
            segs = tu.findall(".//tuv")
            if len(segs) >= 2:
                en, ko = None, None
                for tuv in segs:
                    lang = tuv.attrib.get("{http://www.w3.org/XML/1998/namespace}lang")
                    seg = tuv.find("seg").text if tuv.find("seg") is not None else ""
                    if not seg:
                        continue
                    if lang == "en":
                        en = seg
                    elif lang.startswith("ko"):
                        ko = seg
                if en and ko:
                    pairs.append((en.strip(), ko.strip()))
    except Exception as e:
        print(f"⚠ Error reading {filepath}: {e}")
    return pairs


def write_tmx(pairs, output_file):
    """Write pairs to TMX"""
    header = '''<?xml version="1.0" encoding="UTF-8"?>
<tmx version="1.4">
 <header
   creationtool="OPUS-Combiner"
   creationtoolversion="1.0"
   segtype="sentence"
   adminlang="en"
   srclang="en"
   datatype="PlainText"/>
 <body>
'''
    footer = "</body>\n</tmx>"

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(header)
        for en, ko in pairs:
            f.write(f'  <tu>\n')
            f.write(f'    <tuv xml:lang="en"><seg>{en}</seg></tuv>\n')
            f.write(f'    <tuv xml:lang="ko"><seg>{ko}</seg></tuv>\n')
            f.write(f'  </tu>\n')
        f.write(footer)


# -------------------------------
# MAIN
# -------------------------------
if __name__ == "__main__":
    med_pairs = []
    gen_pairs = []

    # Load medical TMX files (keep all, no trimming except deduplication)
    for tmx in medical_tmx_files:
        if os.path.exists(tmx):
            print(f"Reading MEDICAL file {tmx} ...")
            pairs = read_tmx(tmx)
            print(f"  → {len(pairs)} pairs loaded")
            med_pairs.extend(pairs)
        else:
            print(f"⚠ Skipping missing medical file: {tmx}")

    # Load general TMX files (subject to trimming later)
    for tmx in general_tmx_files:
        if os.path.exists(tmx):
            print(f"Reading GENERAL file {tmx} ...")
            pairs = read_tmx(tmx)
            print(f"  → {len(pairs)} pairs loaded")
            gen_pairs.extend(pairs)
        else:
            print(f"⚠ Skipping missing general file: {tmx}")

    print(f"\nTotal medical before deduplication: {len(med_pairs)}")
    print(f"Total general before deduplication: {len(gen_pairs)}")

    # Deduplicate separately, then combine
    med_pairs = list(set(med_pairs))
    gen_pairs = list(set(gen_pairs))

    print(f"Medical after deduplication: {len(med_pairs)}")
    print(f"General after deduplication: {len(gen_pairs)}")

    # Always keep all medical
    all_pairs = med_pairs[:]

    # Add general only as much as needed
    available_space = MAX_TUS - len(all_pairs)
    if len(gen_pairs) > available_space:
        print(f"Trimming general pairs down to {available_space} to respect max limit")
        gen_pairs = random.sample(gen_pairs, available_space)

    all_pairs.extend(gen_pairs)

    # Final deduplication just in case
    all_pairs = list(set(all_pairs))

    if len(all_pairs) < MIN_TUS:
        print(f"⚠ Warning: Only {len(all_pairs)} TUs in final TM (< {MIN_TUS})")

    # Write output
    write_tmx(all_pairs, output_file)
    print(f"\n✅ Combined TMX saved as '{output_file}' with {len(all_pairs)} translation units.")
    print(f"   → {len(med_pairs)} medical pairs (all kept)")
    print(f"   → {len(gen_pairs)} general pairs (trimmed if needed)")
