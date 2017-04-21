"""
A program that encodes and decodes hidden messages in images through LSB steganography
Encodes some longer passage in the red channel;
Encodes a template revealing the message hidden in the passage on the green channel
"""
from PIL import Image, ImageFont, ImageDraw
import textwrap


def decode_image(file_location="images/encoded_sample.png"):
    """Decodes the hidden message in an image

    file_location: the location of the image file to decode. By default is the
    provided encoded image in the images folder
    """
    # opens the encoded image file and reads its attributes
    encoded_image = Image.open(file_location)
    red_channel = encoded_image.split()[0]
    green_channel = encoded_image.split()[1]
    x_size = encoded_image.size[0]
    y_size = encoded_image.size[1]

    # creates a new image to put things on
    decoded_image = Image.new("RGB", encoded_image.size, (255,255,255))
    decoded_image.load()

    # parses the image pixel per pixel
    for xposition in range(x_size):
        for yposition in range(y_size):
            xy = (xposition, yposition)
            binintred = bin(red_channel.getpixel(xy))
            binintgreen = bin(green_channel.getpixel(xy))
            if binintred[-1] == '1' or binintgreen[-1] == '1':
                decoded_image.putpixel(xy, (0, 0, 0))

    # saves the new image
    decoded_image.save("images/decoded_image.png")


def write_text(text_to_write, message, image_size):
    """Writes text to an RGB image. Creates blocks around words of the message
    in another RGB image.

    text_to_write: the text to write to the image
    message: what you actually want to get across
    image_size: size of the resulting text image. Is a tuple (x_size, y_size)
    """
    # initialize two new images and their drawers
    image_text = Image.new("RGB", image_size)
    image_blankouts = Image.new("RGB", image_size, color=(255, 255, 255))
    font = ImageFont.load_default().font
    textdrawer = ImageDraw.Draw(image_text)
    blankdrawer = ImageDraw.Draw(image_blankouts)
    word_locs = dict()

    # Text wrapping. Change parameters for different text formatting
    margin = offset = 10
    counter = 0
    for line in textwrap.wrap(text_to_write, width=80):
        for word in line.split():
            textdrawer.text((margin, offset), word, font=font)
            # adds the location and size of the word to the dictionary
            word_locs[word] = word_locs.get(word, tuple()) + ((counter, margin-1, offset-1, margin+textdrawer.textsize(word)[0]+1, offset+textdrawer.textsize(word)[1]+1),)
            margin += textdrawer.textsize(word)[0] + 4
            counter += 1
        offset += 15
        margin = 10

    # creates second image with 'blank' boxes around message words by finding
    # the next instance of the word and using its coordinates
    curr_word_index = -1
    for word in message.split():
        short_distance = 1000
        for location in word_locs[word]:
            if location[0] > curr_word_index:
                new_short_distance = location[0]-curr_word_index
                if new_short_distance < short_distance:
                    short_distance = new_short_distance
                    new_location = location
        blankdrawer.rectangle(list(new_location[1:]), (0,0,0))
        curr_word_index = new_location[0]
    return image_text, image_blankouts


def encode_image(text_to_encode, message, template_image="images/cutekitty.png"):
    """Encodes a text message into an image

    text_to_encode: the text to encode into the template image
    template_image: the image to use for encoding. An image is provided by default.
    """
    # takes out the image and looks at its attributes
    template_image = Image.open(template_image)
    red_channel = template_image.split()[0]
    green_channel = template_image.split()[1]
    x_size = template_image.size[0]
    y_size = template_image.size[1]

    # get the images from write_text
    image_text, image_blankouts = write_text(text_to_encode, message, (x_size, y_size))
    text_red = image_text.split()[0]
    blanks_red = image_blankouts.split()[0]

    # create new image to encode the message in
    encoded_image = Image.new("RGB", template_image.size)
    encoded_image.load()

    for xposition in range(x_size):
        for yposition in range(y_size):
            xy = (xposition, yposition)
            # values of red text pixel and red blanks pixel
            textbin = bin(text_red.getpixel(xy))
            blanksbin = bin(blanks_red.getpixel(xy))

            #values of pixels in original image
            imageintred = red_channel.getpixel(xy)
            imagebinred = bin(imageintred)
            imageintgreen = green_channel.getpixel(xy)
            imagebingreen = bin(imageintgreen)
            b = template_image.getpixel(xy)[2]

            red, green = imageintred, imageintgreen
            # normalizes all pixels to even numbers
            if imagebinred[-1] == '1':
                red += -1
            if imagebingreen[-1] == '1':
                green += -1

            # makes appropriate pixels odd numbers
            if textbin[-1] == '1':
                red += 1
            if blanksbin[-1] == '1':
                green += 1

            #puts the pixels into the image
            encoded_image.putpixel(xy, (red, green, b))
    encoded_image.save("images/encoded_image.png")


if __name__ == '__main__':
    # text to encode: some message that will appear on the red channel
    text_to_encode = 'Four score and seven years ago our fathers brought forth on this continent, a new nation, conceived in Liberty, and dedicated to the proposition that all men are created equal. Now we are engaged in a great civil war, testing whether that nation, or any nation so conceived and so dedicated, can long endure. We are met on a great battlefield of that war. We have come to dedicate a portion of that field, as a final resting place for those who here gave their lives that that nation might live. It is altogether fitting and proper that we should do this. But, in a larger sense, we can not dedicate - we can not consecrate- we can not hallow - this ground. The brave men, living and dead, who struggled here, have consecrated it, far above our poor power to add or detract. The world will little note, not long remember what we say here, but it can never forget what they did here. It is for us the living, rather, to be dedicated there to the unfinished work which they ...'
    # message: what you actually want to show up from the text, on the green channel
    message = 'our nation can forget'
    print("Encoding the image...")
    encode_image(text_to_encode, message)
    print("Decoding the image...")
    decode_image('images/encoded_image.png')
