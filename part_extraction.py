import argparse
from pathlib import Path
from typing import Tuple
from PIL import Image
from utils import normalise


def load_image(img: Path) -> Image:
    """
    Load an image from the path.
    :param img : (Path) Path to the image to load
    :return: PIL.Image
    """
    img = Image.open(img)
    img = img.convert("RGB")
    return img


def crop(img: Image, left_up: Tuple[int, int], right_down: Tuple[int, int]) -> Image:
    """
    Crop the image.
    :param img: PIL.Image to crop.
    :param left_up: Pixel position of the left up corner of the cropped image.
    :param right_down: Pixel position of the right corner of the cropped image.
    :return: PIL.image cropped
    """
    # Check that the cropped dimension are inside the image.
    width, height = img.size
    if left_up[0] > width or left_up[1] > width:
        raise f"The width is bigger than the original width {width}"
    if right_down[0] > height or right_down[1] > height:
        raise f"The height is bigger than the original height {height}"

    # Crop the image
    img = img.crop((*left_up, *right_down))

    return img


def save(img: Image, output_img: Path) -> None:
    """
    Do the last processing and save the image
    :param img: PIL.Image. Image to save
    :param output_img: Path to where to save the image and precise it's name.
    :return: None
    """
    # Convert the image to RGB
    img = img.convert("RGB")
    # Squeeze net need an image size of  224 by 224
    img = img.resize((224, 224))
    # If the destination do not exist, create it.
    output_img.parent.mkdir(parents=True, exist_ok=True)
    img.save(output_img)


def part_extraction(
    img: Path,
    left_up: Tuple[int, int],
    right_down: Tuple[int, int],
    output_img: Path,
    normalise_flag: bool = False,
):
    """
    Load the image, crop it and save it.
    :param img: Path to the image
    :param left_up: X,Y position of the left up corner
    :param right_down: X,Y position of the right down corner
    :param output_img: Path to save the image (with file name + extension)
    :param normalise_flag: Flag to normalise of not the images.
    :return:
    """
    # Load the image specified as input
    img = load_image(img)
    if normalise_flag:
        img = normalise(img)
    # Crop the image
    img = crop(img=img, left_up=left_up, right_down=right_down)
    # Save the cropped image
    save(img, output_img)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Crop ELO image to extract the part ELO image"
    )
    parser.add_argument("-i", "--input_img", type=Path, help="Path to the image to cut")
    parser.add_argument(
        "-o", "--output_img", type=Path, help="Path to save the sub image"
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

    args = parser.parse_args()

    part_extraction(
        img=args.input_img,
        left_up=args.left_up,
        right_down=args.right_down,
        output_img=args.output_img,
        normalise_flag=args.normalise,
    )
