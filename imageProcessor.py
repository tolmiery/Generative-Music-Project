from PIL import Image, ImageTk
import math

'''
This module provides an ImageProcessor class to manage image operations such as loading,
resizing, checking color formats, and saving images. It also includes functions to calculate
pixel distances and find the closest color from a predefined set of colors.

''' 
class ImageProcessor:
    def __init__(self, image_path=None):
        self.image = None
        self.current_height = 0
        self.current_width = 0
        if image_path:
            self.load_image(image_path)

    def load_image(self, image_path, current_height=0, current_width=0):
        self.image = Image.open(image_path)
        self.image = self.image.convert("RGBA")  # Ensure it's in RGBA format
        self.current_height = current_height
        self.current_width = current_width

    # Check if the image is grayscale
    # A grayscale image has equal values for R, G, and B for all pixels
    def is_grey_scale(self):
        w, h = self.image.size
        for j in range(w):
            for i in range(h):
                r, g, b, a = self.image.getpixel((j, i))
                if r != g or g != b or r != b:
                    return False
        return True

    # Check if the image has an alpha value (transparency) or if any pixel is not fully opaque
    def is_rgba(self):
        if self.image.info.get("transparency", None) is not None:
            return True
        extrema = self.image.getextrema()
        if extrema[3][0] < 255:
            return True
        return False

    # Resize the image by a given factor
    # The new size is calculated by dividing the original dimensions by the factor
    def resize(self, factor):
        w, h = self.image.size
        new_size = math.ceil(w / factor), math.ceil(h / factor)
        resized_image = self.image.resize(new_size)
        return resized_image

    # Save the image to a specified file path with optimization and quality settings
    def save_image(self, file_path):
        self.image.save(file_path, optimize=True, quality=50)

    # Get the pixel value at a specific (x, y) coordinate
    def get_pixel(self, x, y):
        return self.image.getpixel((x, y))

    # Get the size of the image (width, height)
    def get_size(self):
        return self.image.size

    # Get the image object itself
    def get_image(self):
        return self.image
    
    def get_current_height(self):
        return self.current_height
    
    def get_current_width(self):
        return self.current_width
    
    def set_current_height(self, height):
        self.current_height = height
    
    def set_current_width(self, width):
        self.current_width = width
    
## Calculate the distance between a pixel and a color
# The distance is computed using a modified Euclidean distance formula
def distance(pixel, color):
    x = pixel[0] - color[0]
    y = pixel[1] - color[1]
    z = pixel[2] - color[2]
    if (x + y + z >= 0): return math.sqrt(math.sqrt(x * x + y * y + z * z))
    else: return -math.sqrt(math.sqrt(x * x + y * y + z * z))

## Find the closest color from a list of colors to a given pixel
# The function iterates through the list of colors and calculates the distance to each color
def find_closest(pixel, colors):
    maxi = float('inf')
    mini = float('-inf')
    for idx, rgb in colors:
        d = distance(pixel, rgb)
        if d < maxi and d > mini:
            if (d > 0):
                maxi = d
                mini = -d
            else:
                maxi = -d
                mini = d
            color = idx
    return color

## Determine the color of a pixel based on its RGB values and the image's color format
def find_color(pixel, img, blackwhite, colors):
    if not img.is_grey_scale():
        if abs(pixel[0] - pixel[1]) < 10 and abs(pixel[0] - pixel[2]) < 10 and abs(pixel[2] - pixel[1]) < 10:
            bw = (pixel[0] + pixel[1] + pixel[2]) / (3 * 255)
            if bw >= 0.5:
                return 1
            else:
                return 0
        return find_closest(pixel, colors)
    else:
        for i in range(len(blackwhite)):
            if pixel[0] < blackwhite[i][1]:
                return i

## Define a color set based on the number of colors specified
def color_set(colorNum):
    if colorNum == 2:
        colors = [(0, (0, 0, 0)),
                    (1, (255, 255, 255))]

    elif colorNum == 5:
        colors = [(0, (0, 0, 0)),
                    (1, (255, 255, 255)),
                    (2, (0, 255, 0)),
                    (3, (0, 0, 255)),
                    (4, (255, 0, 0))]

    elif colorNum == 8:
        colors = [(0, (0, 0, 0)),
                    (1, (255, 255, 255)),
                    (2, (0, 255, 0)),
                    (3, (0, 0, 255)),
                    (4, (255, 0, 0)),
                    (5, (255, 255, 0)),
                    (7, (0, 255, 255)),
                    (7, (255, 0, 255))]
    return colors

# Define a black and white color set based on the number of colors specified
def bw_set(colorNum):
    colors_bw = [None] * int(colorNum)
    colors_bw[0] = (0, 0, 0)
    for i in range(int(colorNum)):
        temp = int(255 * (float(i) / int(colorNum)))
        if (i + 1 < len(colors_bw)): colors_bw[i + 1] = (temp, temp, temp)
    colors_bw[int(colorNum) - 1] = (255, 255, 255)
    return colors_bw