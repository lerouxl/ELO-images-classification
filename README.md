# ELO images classification

## Goal:
This repository is goal is to implement the ELO images classification script and how to implement it on a server side.

## Use case:
During the printing process, monitoring ELO images can be saved into an **input folder**.
As those ELO images will contain multiple parts, the inside of the part must be extracted, for that the **top left**
coordinate and the **right down** coordinate of the part must be provided to crop the part.
The part image is saved in an **output folder**.
Then a CNN model from our previous study 
([GitHub](https://github.com/lerouxl/Automatised-quality-assessment-in-additive-layer-manufacturing-using-layer-by-layer-surface-measurem), [DOI](https://doi.org/10.1016/j.procir.2021.03.050)) is applied to classify the image.
The classification can be **saved in a csv** file.

## Examples of use:
To manualy select where to crop
```bash
# Open a GUI to crop
python display_crop -i imgs/demo_full_powder_bed.png -o outs/out.jpg
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```
To crop to a know location:
```bash
# crop
python part_extraction.py -i imgs/demo_full_powder_bed.png -o outs/out.jpg -l 292 713 -r 590 1012
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```


