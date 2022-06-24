import argparse
from pathlib import Path
from part_extraction import part_extraction
from predicte import create_pretrain_model, batch_classify
from tqdm import tqdm
from utils import generate_html_report


def main(
    input_folder: Path,
    output_csv: Path,
    crop: bool,
    processing_folder: Path,
    left_up,
    right_down,
    normalise: bool,
    html: bool
) -> None:
    """
    Process a batch of inputs
    :param input_folder:
    :param output_csv:
    :param crop:
    :param processing_folder:
    :param left_up:
    :param right_down:
    :param normalise:
    :param html
    :return:
    """
    output_csv = Path(output_csv)
    if output_csv.exists():
        output_csv.unlink()
    # List all image in a folder
    all_images = list(Path(input_folder).glob("*.jpg"))

    # If we where asked to crop them, we crop them and create a list of images to classify,
    # Otherwise, all_images is used to define the list of images to classify.
    if crop:
        image_to_classify = []
        # We must crop all images
        print("Crop images")
        for img in tqdm(all_images):
            output_img = Path(processing_folder) / Path(img.name).with_suffix(".jpg")

            part_extraction(
                img=img,
                left_up=left_up,
                right_down=right_down,
                output_img=output_img,
                normalise_flag=normalise,
            )
            image_to_classify.append(output_img)
    else:
        image_to_classify = all_images

    # Classify all the images

    print("Images classification")
    batch_classify(image_to_classify, output_csv)

    # Generate html report
    if html:
        generate_html_report(output_csv, output_csv.with_suffix(".html"))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Will classify a batch of images.")
    parser.add_argument(
        "-i",
        "--input_folder",
        type=Path,
        help="Path of the folder where the images are stored",
    )
    parser.add_argument(
        "-o",
        "--output_csv",
        type=str,
        help="If not none, the prediction will be added to the targeted csv",
    )
    parser.add_argument(
        "-c",
        "--crop",
        action="store_true",
        help="Flag if the images need to be croped",
    )

    parser.add_argument(
        "-f", "--processing_folder", type=Path, help="Where to save the croped images"
    )
    parser.add_argument(
        "-l",
        "--left_up",
        type=int,
        nargs="+",
        help="Left up coordinate of the image to extract (X,Y)",
    )
    parser.add_argument(
        "-r",
        "--right_down",
        type=int,
        nargs="+",
        help="Right down coordinate of the image to extract (X,Y)",
    )
    parser.add_argument(
        "-n",
        "--normalise",
        action="store_true",
        help="Flag if the images need to be normalised",
    )
    parser.add_argument(
        "--html",
        action="store_true",
        help="Flag if a html document should be generated (same name than the css)",
    )

    args = parser.parse_args()

    main(**vars(args))
