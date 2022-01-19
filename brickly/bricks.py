from config import Config
from math import sqrt
from PIL import Image


color_list = (
    (1, "White",  (255, 255, 255)),
    (5, "Brick Yellow", (221, 196, 142)),
    (21, "Bright Red", (221, 26, 33)),
    (23, "Bright Blue", (0, 108, 183)),
    (24, "Bright Yellow", (251, 171, 24)),
    (26, "Black", (19, 19, 19)),
    (102, "Medium Blue", (72, 158, 206)),
    (106, "Bright Orange", (245, 125, 32)),
    (107, "Bright Bluish Green", (24, 158, 159)),
    (119, "Bright Yellowish Green", (154, 202, 60)),
    (124, "Bright Reddish Violet", (181, 28, 125)),
    (140, "Earth Blue", (0, 57, 94)),
    (151, "Sand Green", (111, 148, 122)),
    (154, "Dark Red", (127, 19, 27)),
    (194, "Medium Stone Grey", (160, 161, 159)),
    (199, "Dark Stone Grey", (100, 103, 101)),
    (192, "Reddish Brown", (105, 46, 20)),
    (222, "Light Purple", (246, 173, 205)),
    (226, "Cool Yellow", (255, 245, 121)),
    (268, "Medium Lilac", (76, 47, 146)),
    (283, "Light Nougat", (252, 195, 158)),
    (322, "Medium Azur", (0, 190, 211)),
    (324, "Medium Lavender", (150, 117, 180))
)


def color_distance(pixel, color):
    dR = pixel[0] - color[2][0]
    dG = pixel[1] - color[2][1]
    dB = pixel[2] - color[2][2]

    return sqrt(dR*dR + dG*dG + dB*dB)


def closest_color(pixel):
    closest_distance = None
    closest = None    
    
    for color in color_list:
        distance = color_distance(pixel, color)
        if closest_distance is None or distance < closest_distance:
            closest_distance = distance
            closest = color
    return closest


def block_pixels(input_file, output_name, ratio):
    img = Image.open(input_file)
    size = img.size
    new_width = int(size[0] * ratio)
    new_height = int(size[1] * ratio)
    new_size = (new_width, new_height)
    img = img.resize(new_size)

    pixels = img.load()
    for i in range(new_width):
        for j in range(new_height):
            new_color = closest_color(pixels[i, j])
            pixels[i, j] = new_color[2]
    
    print("Creating {} - Pixel Count: {}".format(output_name, (new_height*new_width)))
    img.save(output_name + '.png')
    img.close()


def preview_image(input_file, output_name, ratio):
    img = Image.open(input_file)
    size = img.size
    new_width = int(size[0] * ratio)
    new_height = int(size[1] * ratio)
    new_size = (new_width, new_height)
    img = img.resize(new_size, resample=4)
    img.save(output_name + '.png')
    img.close()


def section_prev(pixel_image, section_number=0, size=300, square_width=20):
    img = Image.open(pixel_image)
    new_img = Image.new(mode="RGBA", size=(square_width, square_width))

    pix_img = img.load()
    pix_new = new_img.load()
    for i in range(square_width):
        for j in range(square_width):
            pix_new[i, j] = pix_img[i, j]
    new_img.save('section-pixels.png')
    new_img = new_img.resize((size, size), resample=4)
    new_img.save('section-prev.png')


def create_block_overlay(block_img, output_name, size):
    block = Image.open(block_img)
    x = block.size[0]
    
    overlay_width = int(size[0] * x)
    overlay_height = int(size[1] * x)
    overlay_size = (overlay_width, overlay_height)

    img = Image.new(mode="RGBA", size=overlay_size)
    for i in range(size[0]):
        for j in range(size[1]):
            img.paste(block, (i * x , j * x))
    img.save(output_name + '.png')
    img.close()


def create_number_overlay(pixel_image, full_image, output_name):
    pix_img = Image.open(pixel_image)
    pixels= pix_img.load()
    img = Image.open(full_image)
    olay = Image.new(mode="RGBA", size=img.size)

    number_matrix = []
    for i in range(pix_img.size[0]):
        col = []
        for j in range(pix_img.size[1]):
            pixel = pixels[i, j]
            for color in color_list:
                if pixel == color[2]:
                    col.append(color)
        number_matrix.append(col)

    print(number_matrix[0])


def combine_overlay(image, overlay):
    img = Image.open(image)
    olay = Image.open(overlay)
    olay = olay.resize(img.size)

    img.paste(olay, (0, 0), olay)
    img.save('test-final.png')
    img.close()


def get_ratio(image, block_count):
    if block_count > Config.MAX_BLOCK_COUNT:
        block_count = Config.MAX_BLOCK_COUNT
    img = Image.open(image)
    pix_count = img.size[0] * img.size[1]
    ratio = sqrt(block_count / pix_count)
    return ratio


if __name__ == '__main__':

    ratio = get_ratio('test.jpg', 5000)
    print(ratio)
    block_pixels('test.jpg', 'output', ratio=ratio)
    img = Image.open('output.png')
    block_size = img.size
    img.close()
    block_count = block_size[0] * block_size[1]
    print(block_count)

    preview_image('output.png', 'output-prev', ratio=(1/ratio))
    create_block_overlay('block-overlay.png', 'test-overlay', block_size)
    combine_overlay('output-prev.png', 'test-overlay.png')
    create_number_overlay('output.png', 'test.jpg', 'test-color.png')
    
    section_prev('output.png')
    section = Image.open('section-pixels.png')
    create_block_overlay('block-overlay.png', 'section-overlay', section.size)
    combine_overlay('section-prev.png', 'section-overlay.png')
