import PIL
import qrcode
import tkinter as tk
from tkinter import filedialog as fd

from PIL.Image import Image


def simple_code(version=1, box_size=10, border=4):
    """
    Create a basic QR Code
    
    :param version: controls the size of the qr code [1-40] 1 being the smallest at a 21x21 matrix
    :param box_size: controls how many pixels each square in the code is
    :param border: controls how many boxes thick the border is (ex: box_size=10 and border=4 gives a 40 pixel border)
    
    :return: an image of the generated qr code
    """
    print("Creating a simple code")
    url = input("What would you like to embed? ")

    # setting up the QR code
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Creating the QR code image
    img = qr.make_image(fill_color="black", back_color="white")

    return img


def logo_code(version=1, box_size=10, border=4, max_logo_size=50, preserve_aspect=True):
    """
    Create a QR Code with an image embedded in it
    
    :param version: controls the size of the qr code [1-40] 1 being the smallest at a 21x21 matrix
    :param box_size: controls how many pixels each square in the code is
    :param border: controls how many boxes thick the border is (ex: box_size=10 and border=4 gives a 40 pixel border)
    :param max_logo_size: the maximum nuber of pixels in any direction that the image will be
    :param preserve_aspect: a boolean to control whether the aspect ratio of the image will be preserved
    
    :return: an image of the generated qr code
    """
    print("Creating a code with an image in the center")
    url = input("What would you like to embed? ")

    # navigation to and opening the logo image
    logo_path = fd.askopenfile(mode="r",
                               title="What logo would you like to embed?",
                               filetypes=[("PNG", ".png"),
                                          ("JPEG", ".jpeg")],
                               defaultextension=".png")

    logo = PIL.Image.open(logo_path.name, "r")
    logo_width, logo_height = logo.size

    if preserve_aspect:
        if logo_width > logo_height:
            scale_ratio = max_logo_size / logo_width
            final_logo_size = int(logo_width * scale_ratio), int(logo_height * scale_ratio)
        else:
            scale_ratio = max_logo_size / logo_height
            final_logo_size = int(logo_width * scale_ratio), int(logo_height * scale_ratio)
    else:
        final_logo_size = max_logo_size, max_logo_size

    # setting up the QR code
    qr = qrcode.QRCode(
        version=version,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=box_size,
        border=border,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Creating the QR code image and getting it's data
    img = qr.make_image(fill_color="black", back_color="white")
    code_width, code_height = img.size
    img = img.convert("RGBA")

    x_min = int((code_width / 2) - (final_logo_size[0] / 2))
    y_min = int((code_height / 2) - (final_logo_size[1] / 2))
    x_max = int((code_width / 2) + (final_logo_size[0] / 2))
    y_max = int((code_height / 2) + (final_logo_size[1] / 2))

    # resizing logo
    logo = logo.resize((x_max - x_min, y_max - y_min))

    # Pasting logo onto 
    img.paste(logo, (x_min, y_min, x_max, y_max), mask=logo)

    return img

if __name__ == '__main__':
    welcome_string = "Welcome to the qr code generator.\n" \
                     "What type of code would you like?\n" \
                     "\t [1] Simple Black and White\n" \
                     "\t [2] Black and white with a logo embedded in the middle\n"

    print(welcome_string)
    type = int(input("Please enter the code number: "))

    settings = input("Would you like [d]efault or [c]ustom settings? ")

    if settings == "d":
        if type == 1:
            code_img = simple_code()
        elif type == 2:
            code_img = logo_code()
    else:
        version = int(input("Code version number: "))
        box_size = int(input("Number of pixels wide/tall for each box: "))
        border_size = int(input("Number of boxes wide for the border: "))

        if type == 1:
            code_img = simple_code(version, box_size, border_size)
        elif type == 2:
            max_logo_size = int(input("Number of pixels wide the logo should be: "))
            aspect_preserve = input("Preserve logo aspect ratio [t]/[f]: ") == "t"
            code_img = logo_code(version, box_size, border_size, max_logo_size, aspect_preserve)

    code_img.show()
