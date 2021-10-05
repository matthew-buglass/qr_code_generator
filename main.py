import PIL
import qrcode
import tkinter as tk
from tkinter import filedialog as fd

from PIL.Image import Image


def simple_code():
    print("Creating a simple code")
    url = input("What would you like to embed? ")

    # setting up the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Creating the QR code image
    img = qr.make_image(fill_color="black", back_color="white")
    img.show()

    return img


def logo_code():
    print("Creating a code with an image in the center")
    url = input("What would you like to embed? ")

    # navigation to and opening the logo image
    logo_path = fd.askopenfile(mode="r",
                               title="What logo would you like to embed?",
                               filetypes=[("PNG", ".png"),
                                          ("JPEG", ".jpeg")],
                               defaultextension=".png")

    logo = PIL.Image.open(logo_path.name, "r")
    logo_size = 50

    # setting up the QR code
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=30,
        border=1,
    )
    qr.add_data(url)
    qr.make(fit=True)

    # Creating the QR code image and getting it's data
    img = qr.make_image(fill_color="black", back_color="white")
    width, height = img.size
    img = img.convert("RGBA")

    x_min = y_min = int((width / 2) - (logo_size / 2))
    x_max = y_max = int((width / 2) + (logo_size / 2))

    # resizing logo
    logo = logo.resize((x_max - x_min, y_max - y_min))

    img.paste(logo, (x_min, y_min, x_max, y_max))
    img.show()

    return img

if __name__ == '__main__':
    welcome_string = "Welcome to the qr code generator.\n" \
                     "What type of code would you like?\n" \
                     "\t [1] Simple Black and White\n" \
                     "\t [2] Black and white with a logo embedded in the middle\n"

    print(welcome_string)
    type = int(input("Please enter the code number: "))

    if type == 1:
        code_img = simple_code()
    elif type == 2:
        code_img = logo_code()