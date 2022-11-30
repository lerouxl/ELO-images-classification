from pathlib import Path
import torch
from torch import nn
from PIL import Image
from torchvision import transforms
import argparse
from csv import writer
from tqdm import tqdm
from flash.image import ImageClassifier


def create_pretrain_model():
    """
    Load a saved pytorch lightning model from a path.
    The model is put in eval mode and gradient is deactivated.
    :param path: path where is saved the model
    :return: ImageClassifier model with loaded weitgh.
    """
    model = ImageClassifier.load_from_checkpoint(r"image_classification_model.pt")

    for p in model.parameters():
        p.requires_grad = False
    model.eval()

    return model


def batch_classify(model, images_path, output_path):
    """
    Classify a list of images, dataloader are not use to avoid memory issues with big list of files.
    :param model: the pretrained model
    :param images_path: list of path of images
    :param output_path If not none, the prediction will be added to the targeted csv
    :return:
    """
    # Classify the image
    classification_list = []
    for image_path in tqdm(images_path):
        classification_list.append(classify_an_image(model, image_path, output_path))

    return classification_list


def classify_an_image(model, image_path, output_path):
    """
    Load ONE image an classify it.
    :param model: the pretrained model
    :param image_path: path to one image
    :param output_path If not none, the prediction will be added to the targeted csv
    :return: dictionary with the image name and the classification probability.
    """
    image_path = Path(image_path)

    # Load image
    input_size = (196, 196)
    input_image = Image.open(image_path)
    preprocess = transforms.Compose(
        [
            transforms.Resize(input_size),
            transforms.ToTensor(),
            transforms.ConvertImageDtype(torch.float),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
        ]
    )
    input_tensor = preprocess(input_image)
    input_batch = input_tensor.unsqueeze(
        0
    )  # create a mini-batch as expected by the model

    # Make a prediction
    with torch.no_grad():
        output = model(input_batch)
    # Tensor of shape 1000, with confidence scores over Imagenet's 1000 classes
    print(output[0])
    # The output has unnormalized scores. To get probabilities, you can run a softmax on it.
    probabilities = torch.nn.functional.softmax(output[0], dim=0)
    print(probabilities)

    probabilities = probabilities.numpy()
    proba_to_text = {
        "image_path": str(image_path),
        "bulging": round(probabilities[0], 4),
        "edges": round(probabilities[1], 4),
        "good": round(probabilities[2], 4),
        "porous": round(probabilities[3], 4),
        "powder": round(probabilities[4], 4),

    }
    print(proba_to_text)

    # If an ouput path is specified:
    if not output_path is None:
        output_path = Path(output_path)
        # if the file output is not existing, create an empty one with the header
        if not output_path.is_file():
            with open(output_path, "w", newline="") as write_csv:
                csv_writer = writer(write_csv)
                csv_writer.writerow(["image_path", "bulging", "edges", "good", "porous", "powder"])

        with open(output_path, "a+", newline="") as write_csv:
            csv_writer = writer(write_csv)
            csv_writer.writerow(
                [
                    proba_to_text["image_path"],
                    proba_to_text["bulging"],
                    proba_to_text["edges"],
                    proba_to_text["good"],
                    proba_to_text["porous"],
                    proba_to_text["powder"],
                ]
            )

    return proba_to_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Will classify one image.")
    parser.add_argument(
        "-i", "--input_img", type=Path, help="Path to the image to load", default=None
    )
    parser.add_argument(
        "-b", "--batch_folder", type=Path, help="To classify multiple images, take the folder path", default=None
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="If not none, the prediction will be added to the targeted csv",
    )
    args = parser.parse_args()

    if args.input_img is None and args.batch_folder is None:
        raise "No inputs images nor folder was given. Please specify what image(s) to classify."

    # Create the torch model
    model = create_pretrain_model()

    if not args.input_img is None:
        # Classify the image provided
        classify_an_image(model, args.input_img, args.output)

    else:
        # Classify a folder of images
        list_of_images = list(Path(args.batch_folder).glob("*.jpg"))
        list_of_images.extend(list(Path(args.batch_folder).glob("*.png")))
        batch_classify(model, list_of_images , args.output)