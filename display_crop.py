import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path
from typing import Tuple
import argparse
from part_extraction import part_extraction

global points
global left_up
global right_down
global right_down
global left_up
global left_up_point
global right_down_point

left_up = (0, 0)
right_down = (0, 0)


def onclick(event) -> None:
    """
    Matplotlib function that will store the right and left click position and add a point to those coordinates.
    :param event:
    :return:
    """
    global right_down
    global left_up
    global left_up_point

    if event.inaxes == ax:
        print(
            "%s click: button=%d, x=%d, y=%d, xd=%d, yd=%d"
            % (
                "double" if event.dblclick else "single",
                event.button,
                event.x,
                event.y,
                event.xdata,
                event.ydata,
            )
        )
        x = int(round(event.xdata, 0))
        y = int(round(event.ydata, 0))
        if event.button == 1:
            # If left click
            left_up = (x, y)
            left_up_point.set_xdata(x)
            left_up_point.set_ydata(y)
        if event.button == 3:
            # If right click
            right_down = (x, y)
            right_down_point.set_xdata(x)
            right_down_point.set_ydata(y)
        text.set_text(
            f"left_up (right click):{left_up}\nright_down (left click):{right_down}"
        )
    plt.draw()


def display(img_path: Path) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Display the desired image and allow to select the area to crop.
    :param img_path: pathlib.Path of the image to load
    :return: left_up, right_down, 2 tuple containing the X,Y coordinates of the rectangle to crop.
    """
    global ax
    global text
    global left_up_point
    global right_down_point

    img = mpimg.imread(img_path)
    fig, ax = plt.subplots()
    ax.imshow(img)
    ax.text(
        -100,
        -50,
        "Right click for the left up coordinate and Left click for the right down coordinate.",
    )

    (left_up_point,) = plt.plot(*left_up, "go")
    (right_down_point,) = plt.plot(*right_down, "yo")
    text = ax.text(
        0,
        ax.get_ylim()[0] * 1.1,
        f"left_up (right click):{left_up}\nright_down (left click):{right_down}",
    )

    cid = fig.canvas.mpl_connect("button_press_event", onclick)

    plt.show()
    return left_up, right_down


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Graphical interface to load an images and found where to crop."
    )
    parser.add_argument("-i", "--input_img", type=Path, help="Path to the image to cut")
    parser.add_argument(
        "-o", "--output_img", type=Path, help="Path to save the sub image"
    )
    args = parser.parse_args()

    # Display the image and allow user to click to select where to crop
    left_up, right_down = display(args.input_img)

    part_extraction(args.input_img, left_up, right_down, args.output_img)
    # Return the selected area;
    print((left_up, right_down))
