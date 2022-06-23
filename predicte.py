from pathlib import Path
import torch
from torch import nn
from PIL import Image
from torchvision import transforms
import argparse
from csv import writer
from tqdm import tqdm


def create_pretrain_model():
    """
    Create a pretrained model for ELO image classification. Base on the squeezenet architecture.
    :return: torchvision.models.squeezenet.SqueezeNet with weights for the classification.
    """
    # Create model
    model = torch.hub.load("pytorch/vision:v0.10.0", "squeezenet1_0", pretrained=False)
    model.classifier[1] = nn.Conv2d(512, 3, kernel_size=(1, 1), stride=(1, 1))
    model.num_classes = 3
    # Load pre trained weights
    model.load_state_dict(
        torch.load("SqueezeNet_pretrain_epoch-38.pt", map_location=torch.device("cpu"))
    )
    model.eval()

    return model


def batch_classify(images_path, output_path):
    """
    Classify a list of images, dataloader are not use to avoid memory issues with big list of files.
    :param images_path: list of path of images
    :param output_path If not none, the prediction will be added to the targeted csv
    :return:
    """
    # Create the torch model
    model = create_pretrain_model()
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
    input_size = 224
    input_image = Image.open(image_path)
    preprocess = transforms.Compose(
        [
            transforms.Resize(input_size),
            transforms.ToTensor(),
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
        "good": round(probabilities[0], 4),
        "porous": round(probabilities[1], 4),
        "bulging": round(probabilities[2], 4),
    }
    print(proba_to_text)

    # If an ouput path is specified:
    if not output_path is None:
        output_path = Path(output_path)
        # if the file output is not existing, create an empty one with the header
        if not output_path.is_file():
            with open(output_path, "w", newline="") as write_csv:
                csv_writer = writer(write_csv)
                csv_writer.writerow(["image_path", "good", "porous", "bulging"])

        with open(output_path, "a+", newline="") as write_csv:
            csv_writer = writer(write_csv)
            csv_writer.writerow(
                [
                    proba_to_text["image_path"],
                    proba_to_text["good"],
                    proba_to_text["porous"],
                    proba_to_text["bulging"],
                ]
            )

    return proba_to_text


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Will classify one image.")
    parser.add_argument(
        "-i", "--input_img", type=Path, help="Path to the image to load"
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        help="If not none, the prediction will be added to the targeted csv",
    )
    args = parser.parse_args()

    # Create the torch model
    model = create_pretrain_model()

    # Classify the image
    classify_an_image(model, args.input_img, args.output)
