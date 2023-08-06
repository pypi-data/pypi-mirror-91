import argparse
import matplotlib.pyplot as plt
from lineenhancer.maskstackcreator import MaskStackCreator
import scipy.misc as sp
import time
import numpy as np
import sys
from lineenhancer import image_reader
from lineenhancer import line_enhancer
from PIL import Image
import glob

argparser = argparse.ArgumentParser(
    description='Enhances line images',
    formatter_class=argparse.ArgumentDefaultsHelpFormatter)

argparser.add_argument(
    '-i',
    '--input',
    help='path to input file')

argparser.add_argument(
    '-d',
    '--downsamplesize',
    default=1024,
    type=int,
    help='size image is downsampled to (should be a power of 2')

argparser.add_argument(
    '-lw',
    '--linewidth',
    default=50,
    type=int,
    help='line width with before downsampling')

argparser.add_argument(
    '-m',
    '--maskwidth',
    default=100,
    type=int,
    help='mask width')

argparser.add_argument(
    '-a',
    '--angle_step',
    default=2,
    type=int,
    help='angle step size')

#cuda.init()
#context = make_default_context()
#stream = cuda.Stream()




def _main_():


    args = argparser.parse_args()

    '''
    LOAD IMAGE DATA AS EXAMPLE
    '''

    if args.input is not None:
        example_paths = glob.glob(args.input)
    else:
        sys.exit("No input is given")
    mask_size = args.downsamplesize
    filament_width = args.linewidth
    mask_width = args.maskwidth
    angleStep = args.angle_step
    example = image_reader.image_read(example_paths[0])

    '''
    CREATE EXAMPLE: RESIZE IMAGE, REPEAT IT 12 TIMES (simulates 12 input images)
    '''

    rescale_factor = mask_size / max(example.shape[0], example.shape[1])
    filament_width = filament_width*rescale_factor
    print("Used FW:", filament_width)

    '''
    CREATE EXAMPLE WITH PATHS
    '''
    #example_paths = [example_path]

    '''
    INIT MASK CREATOR
    '''
    mask_creator = MaskStackCreator(filament_width, mask_size, mask_width, angleStep, bright_background=True)
    mask_creator.init()

    '''
    DO ENHANCEMENT
    '''
    start = time.time()
    enhanced_images = line_enhancer.enhance_images_to_dir(example_paths, mask_creator,"testout")
    end = time.time()

    '''
    PLOT RESULT
    '''
    '''
    fig = plt.figure(figsize=(2, 2))
    fig.add_subplot(2,2,1)
    plt.imshow(enhanced_images[0]["max_value"])
    fig.add_subplot(2, 2, 2)
    plt.imshow(enhanced_images[0]["max_angle"])
    fig.add_subplot(2, 2, 3)
    plt.imshow(mask_creator.get_mask_stack()[0])
    fig.add_subplot(2, 2, 4)
    plt.imshow(mask_creator.get_mask_stack()[23])

    plt.show()
    '''
    #np.savetxt("/home/twagner/angle_image.txt",enhanced_images[0]["max_angle"])

    #np.savetxt("/home/twagner/3719.txt",enhanced_images[0]["max_angle"])


if __name__ == '__main__':
    _main_()