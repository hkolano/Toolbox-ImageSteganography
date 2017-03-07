"""A program that encodes and decodes hidden messages in images through LSB steganography"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the
    provided encoded image in the images folder
    """
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]

    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    decoded_image = Image.new("RGB", encoded_image.size)
    pixels = decoded_image.load()

    for xposition in range(x_size):
        for yposition in range(y_size):
            xy = (xposition, yposition)
            binint = bin(red_channel.getpixel(xy))
            if binint[-1] == '0':
                decoded_image.putpixel(xy, (0, 0, 0))
            elif binint[-1] == '1':
                decoded_image.putpixel(xy, (255, 255, 255))

    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, image_size):
    """Writes text to an RGB image. Automatically line wraps

    text_to_write: the text to write to the image
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    image_text = Image.new("RGB", image_size)
    font = ImageFont.load_default().font
    drawer = ImageDraw.Draw(image_text)

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    for line in textwrap.wrap(text_to_write, width=60):
        drawer.text((margin, offset), line, font=font)
        offset += 10
    return image_text


def encode_image(text_to_encode, template_image="images/cutekitty.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    template_image = Image.open(template_image)
    red_channel = template_image.split()[0]

    x_size = template_image.size[0]
    y_size = template_image.size[1]

    image_text = write_text(text_to_encode, (x_size, y_size))
    text_red = image_text.split()[0]

    encoded_cats = Image.new("RGB", template_image.size)
    pixels = encoded_cats.load()

    for xposition in range(x_size):
        for yposition in range(y_size):
            xy = (xposition, yposition)
            textbin = bin(text_red.getpixel(xy))
            imageint = red_channel.getpixel(xy)
            imagebin = bin(imageint)
            g = template_image.getpixel(xy)[1]
            b = template_image.getpixel(xy)[2]
            if imagebin[-1] == '0':
                encoded_cats.putpixel(xy, (imageint, g, b))
                if textbin[-1] == '1':
                    encoded_cats.putpixel(xy, (imageint+1, g, b))
            elif imagebin[-1] == '1':
                encoded_cats.putpixel(xy, (imageint-1, g, b))
                if textbin[-1] == '1':
                    encoded_cats.putpixel(xy, (imageint, g, b))
    encoded_cats.save("images/encoded_cats.png")


if __name__ == '__main__':
    text_to_encode = 'Never give up on your dreams. \n Just keep sleeping.'
    print("Encoding the image...")
    encode_image(text_to_encode)
    print("Decoding the image...")
    decode_image()# 'images/encoded_cats.png')
