# ELO images classification

## Goal:
This repository's goal is to implement the ELO images classification script that can be used on a production computer or with the Manuela dashboard.

## Use case:
Monitoring ELO images can be saved into an **input folder** during the printing process. 
As those ELO images will contain multiple parts, the inside of the part must be extracted, so the **top-left** coordinate and
the **right-down** coordinate of the part must be provided to crop the part. 
The part image is saved in an **output folder**. Then a CNN model from our previous study ([GitHub](https://github.com/lerouxl/Automatised-quality-assessment-in-additive-layer-manufacturing-using-layer-by-layer-surface-measurem), [DOI](https://doi.org/10.1016/j.procir.2021.03.050)) is applied to classify the image.
The classification can be **saved in a CSV file**. Image can be normalised using the **--normalise** or -n flag, this is useful for images with low contrast.

Input images are expected to be in the **.jpg** format. 
The CSV output is made of 3 columns, image_path, good, porous and bulging. 
Image_path is the path to the input images, and the 3 other scores are the classification probability with 1 equal to 100% and 0 to 0%.

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/csv.JPG?raw=true" alt="CSV output example">
 <br>
 <i>CSV output example</i>
</p>

## Examples of use:

### Crop:
To manualy select where to crop:
```bash
# Open a GUI to crop
python display_crop -i imgs/demo_full_powder_bed.png -o outs/out.jpg
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```
To crop to a know location with normalisation:
```bash
# crop
python part_extraction.py -i imgs/demo_full_powder_bed.png --normalise -o outs/out.jpg -l 292 713 -r 590 1012
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```

### Normalisation (recommended)

If the image has no contrast, as in raw monitoring images, preprocessing steps are required. Here is an example of what can be seen with a non-normalised image for the crop GUI:
<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/GUI_no_normalise.JPG?raw=true" alt="Raw monitoring image">
 <br>
 <i>Raw monitoring image</i>
</p>


 If we extract a specific area to know if there is porosity or bulging, this area will lack contrast. 
 For example, the area ((934, 540), (986, 596)) was extracted from imgs/img_to_normalise/14-25-41.jpg and classified.

```bash
# crop
python part_extraction.py -i imgs/img_to_normalise/14-25-41.jpg -o outs/out.jpg -l 934 540 -r 986 596
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```
The cropped image is:

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/out_no_normalise.jpg?raw=true" alt="Crop raw image">
 <br>
 <i>Crop raw image</i>
</p>

And is classification results show that the neural network thinks the area is good, but by looking at it, we can guess porosity, which is hard to find due to the contrast.

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/classification_no_normalise.JPG?raw=true" alt="Result with a raw image">
 <br>
 <i>Result with a raw image</i>
</p>

If we redo the same previous step but by normalising the image, the classification is now good:
```bash
# crop
python part_extraction.py -i imgs/img_to_normalise/14-25-41.jpg --normalise -o outs/out.jpg -l 934 540 -r 986 596
# Classify the image
python predicte.py -i outs/out.jpg -o results.csv
```
The normalised image is now:
<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/GUI_with_normalise.JPG?raw=true" alt="Normalised monitoring image">
 <br>
 <i>Normalised monitoring image</i>
</p>


And the cropped image is now:

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/out_with_normalise.jpg?raw=true" alt="Crop raw image">
 <br>
 <i>Crop raw image</i>
</p>

In this image, we can now see the porosity that was hard to see in the non-normalised image. 
And the classification results show now that the neural network is sure that there is a porosity. 

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/classification_with_normalise.JPG?raw=true" alt="Results raw image">
 <br>
 <i>Results raw image</i>
</p>

### Batch processing
It may be useful to process and classify all the images from a folder, the batch script was made for this use:

```batch
python batch.py --input_folder imgs/img_to_normalise --output_csv results.csv --crop --processing_folder out --left_up 934 540 --right_down 986 596 --normalise
```

This example will list all images in the input_folder, crop them, normalise them and save them in the processing_folder. 
The cropped images are then classified and the results are saved in the results.csv.
If we already have preprocessed images, it's possible to directly classify them with:
```batch
python batch.py --input_folder out --output_csv results.csv 
```

### HTML reports
When processing batch of images, it can be hard to compare the neural network classification with the real images, as the csv file is only providing the image path and its classification score.
To simplify this comparison task, a html report can be generated, with the `--html` argument, displaying the images and there classification score.
the html report will be generated in the same folder of the csv file with the same name.
```batch
python batch.py --input_folder out --output_csv results.csv --html
```
<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/html_repport_example.JPG?raw=true" alt="HTML report example">
 <br>
 <i>HTML report example</i>
</p>

### Image smoothing
Monitoring images can have noise due to the image capture parameters, reducing the accuracy of the neural network classification.
To reduce the effect of the ELO images artefact (those artefacts can be seen on the image ID 1 of the HTML report 
example), the ELO images classification script have a smoothening option. 
The smoothening filter must be applied multiple time to remove the noise features, a by our experience, 10 times seem to be a good number.
```batch
python batch.py --input_folder out --output_csv results.csv --html --smooth 10
```

Here is an example of a normal html report and another one with images with a 10 steps smoothing:

<p align="center">
 <img src="https://github.com/lerouxl/ELO-images-classification/blob/main/imgs/readme/comparison_of_html_report_without_and_with_10_smooth?raw=true" alt="comparison of html report without and with_10 smoothening steps">
 <br>
 <i>Comparison of html report without and with_10 smoothening steps</i>
</p>

On the left, it appears that the neural network believe that all the images 63, 64 and 65 are porous.
But the images only show artefacts. By smoothing those artefacts, right show that
the neural networks can now correctly identity them as good layers.