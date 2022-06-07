import os

# Preprocessing

# Part extraction
os.system(
    "python part_extraction.py -i imgs/demo_full_powder_bed.png -o outs/out.jpg -l 292 713 -r 590 1012"
)

# Prediction
os.system("python predicte.py -i outs/out.jpg -o results.csv")
