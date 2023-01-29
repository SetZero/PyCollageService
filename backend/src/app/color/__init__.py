import binascii
from multiprocessing import Pool
from os import listdir
from os.path import isfile, join
import sys
from PIL import Image, UnidentifiedImageError, ImageDraw
import numpy as np
import scipy
import scipy.misc
import scipy.cluster
import math


CPU_THREADS = 24
MAX_RESOLUTION = (128,128)
INPUT_IMAGES = "block"
MAPPING_IMAGE = "D:/Seafile/Main/Main2/Bilder/Character/87.webp"
THUMBNAIL_IMAGE_SIZE = (32, 32)

def get_files(path: str) -> list[str]:
    """
    Get files inside a given path

    This will only return the first layer of files, without any subdirectories

    Parameters
    ----------
    path: str
        Path to the folder which shall be inspected
    """
    return [join(path, f) for f in listdir(path) if isfile(join(path, f))]


def analyse_color(file: str) -> dict[str, any]:
    """
    Returns the most dominant color of a given image

    This will use kmeans to extract color clusters

    Parameters
    ----------
    file: str
        Path to the image which should be inspected

    Returns
    -------
    dict[str, any]
        file: input parameter file
        color: The most dominant color
        data: A dictionary containing the processed file as PIL
    """
    NUM_CLUSTERS = 1

    try:
        im = Image.open(file)
        im = im.resize(THUMBNAIL_IMAGE_SIZE)
        ar = np.asarray(im)
        shape = ar.shape
        ar = ar.reshape(np.product(shape[:2]), shape[2]).astype(float)
        codes, _ = scipy.cluster.vq.kmeans(ar, NUM_CLUSTERS)
        vecs, _ = scipy.cluster.vq.vq(ar, codes)
        counts, _ = np.histogram(vecs, len(codes))
        index_max = np.argmax(counts)
        peak = codes[index_max]
        color = binascii.hexlify(bytearray(int(c) for c in peak)).decode('ascii')

        return {'file': file, 'color': color, 'data': im }
    except IndexError:
        pass
    except UnidentifiedImageError:
        pass


def create_color_map(images: list[dict[str, any]]) -> None:
    """
    Creates an output image with a block representation of each available color for the input images

    Parameters
    ----------
    images: list[dict[str, any]]
        List of images returned from ``analyse_color(file: str) -> dict[str, any]``
    """
    IMAGES_PER_ROW = 10
    SQUARE_SIZE = 32

    width = SQUARE_SIZE * IMAGES_PER_ROW
    height = math.ceil(len(images) / IMAGES_PER_ROW) * SQUARE_SIZE
    im = Image.new('RGB', (width, height))
    draw = ImageDraw.Draw(im)

    for i, image in enumerate(images):
        xstart = int((i % IMAGES_PER_ROW) * SQUARE_SIZE)
        ystart = int((i // IMAGES_PER_ROW) * SQUARE_SIZE)

        shape = [(xstart, ystart), (xstart + SQUARE_SIZE, ystart + SQUARE_SIZE)]
        draw.rectangle(shape, fill='#' + image['color'])

    im.save('chart.png', "PNG")


def transform_input_image(img: str):
    """
    Crops a given image to ``MAX_RESOLUTION`` and transforms it into an np array in RGB colorspace

    Parameters
    ----------
    images: str
        Path to the image

    Returns
    -------
    NDArray
        cropped RGB image
    """
    im = Image.open(img)
    im.thumbnail(MAX_RESOLUTION, Image.Resampling.LANCZOS)
    im.convert('RGB')
    return np.array(im)

def generate_color_map(image_colors: list[dict[str, any]]) -> dict[str, dict[str, any]]:
    """
    Transforms a list of color information dicts from ``create_color_map```to a dict with color
    as its key of color information dicts

    Parameters
    ----------
    image_colors: list[dict[str, any]]
        list of color information dicts

    Returns
    -------
    dict[str, dict[str, any]]
        Dict with color as its key
    """
    colors = {}
    for img in image_colors:
        color = tuple(int(img['color'][i:i+2], 16) for i in (0, 2, 4))
        colors[color] = img
    return colors

def closest(color_data: tuple):
    """
    Find the clostest color out of a list of colors

    Parameters
    ----------
    color_data: tuple
        tuple containing the list of color as first parameter and the color as its seconds parameter

    Returns
    -------
    tuple:
        RGB tuple with the clostest color
    """
    colors = np.array(list(color_data[0].keys()))
    color = np.array(color_data[1])
    distances = np.sqrt(np.sum((colors-color)**2,axis=1))
    index_of_smallest = np.where(distances==np.amin(distances))
    smallest_distance = colors[index_of_smallest[0]]
    return (smallest_distance[0], color_data[0][tuple(smallest_distance[0])]['data'])

def color_to_collage(img_obj: list[tuple], shape: tuple):
    """
    Find the clostest color out of a list of colors

    Parameters
    ----------
    img_obj: list[tuple]
        flat list of rgb values of the image
    shape: tuple
        original dimensions of the image

    Returns
    -------
    Image:
        Image collage object
    """
    x_size = shape[1]
    y_size = shape[0]
    new_im = Image.new('RGB', (x_size*THUMBNAIL_IMAGE_SIZE[0], y_size*THUMBNAIL_IMAGE_SIZE[1]))

    for i, img in enumerate(img_obj):
        new_im.paste(img, ((i % x_size)*THUMBNAIL_IMAGE_SIZE[0],(i // x_size)*THUMBNAIL_IMAGE_SIZE[1]))

    return new_im


def find_closest(image: np.ndarray, color_map: dict[str, dict[str, any]]):
    """
    Convert a image into a custom color palette of images

    Parameters
    ----------
    image: np.ndarray
        numpy array of RGB image information
    color_map: dict[str, dict[str, Any]]
        Map of available colors given from ``generate_color_map``

    Returns
    -------
    Image:
        Image collage object
    """
    original_shape = image.shape
    img = image.reshape(-1, image.shape[-1])
    with Pool(CPU_THREADS) as p:
        el = [(color_map, color) for color in img]
        _, img_obj = zip(*p.map(closest, el))
        return color_to_collage(img_obj, original_shape)


def generate_collage(image_folder: str, mapping_image: str):
    image_map = []
    with Pool(CPU_THREADS) as p:
        image_map= p.map(analyse_color, get_files(image_folder))
    image_map = list(filter(lambda im: im is not None and len(im['color']) == 6, image_map))
    image_map = generate_color_map(image_map)
    image = transform_input_image(mapping_image)

    return find_closest(image, image_map)
