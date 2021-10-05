import PIL
import qrcode
import tkinter as tk
from tkinter import filedialog as fd

from PIL.Image import Image


def simple_code(version=1, box_size=10, border=4):
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
    img.show()

    return img


def logo_code(version=1, box_size=10, border=4, max_logo_size=50, preserve_aspect=True):
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
            scale_ratio = logo_width / max_logo_size
            final_logo_size = int(logo_width * scale_ratio), int(logo_height * scale_ratio)
        else:
            scale_ratio = logo_height / max_logo_size
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
    logo.show()
    logo = logo.resize((x_max - x_min, y_max - y_min))
    logo.show()

    img.show()
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

    settings = input("Would you like [d]efault or [c]ustom settings?")

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
