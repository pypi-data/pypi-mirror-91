import numpy as np
import sys
import multiprocessing
from cryolo import imagereader
from PIL import Image


def enhance_images(input_images, maskcreator, num_cpus = -1):
    is_path_list = isinstance(input_images,list)

    if not is_path_list:
        if input_images.shape[1] != maskcreator.get_mask_size() or input_images.shape[2] != maskcreator.get_mask_size():
            sys.exit("Mask and image dimensions are different. Stop")

    fft_masks = maskcreator.get_mask_fft_stack()
    #global all_kernels
    #all_kernels = fft_masks
    input_img_and_kernel= []
    for img in input_images:
        for frame in range(imagereader.get_num_frames(img)):
            input_img_and_kernel.append((img, fft_masks, frame))

    if num_cpus > -1:
        pool = multiprocessing.Pool(processes=num_cpus)
    else:
        pool = multiprocessing.Pool()
    if is_path_list:
        #enhanced_images = enhance_image_by_path(fourier_kernel_stack=all_kernels, input_image_path=input_images[0])
        enhanced_images = pool.map(wrapper_fourier_stack_paths, input_img_and_kernel)
    else:
        enhanced_images = pool.map(wrapper_fourier_stack, input_img_and_kernel)

    pool.close()
    pool.join()
    enhanced_images_list = []
    for img in input_images:
        enhanced_frames_list = []

        for input_index, input_tuble in enumerate(input_img_and_kernel):
            img_input, _, frame = input_tuble
            if img_input == img:
                enhanced_frames_list.append(enhanced_images[input_index])
        enhanced_images_list.append(enhanced_frames_list)

    for img in enhanced_images:
        img["max_angle"] = img["max_angle"]*maskcreator.get_angle_step()

    return enhanced_images_list

def enhance_images_to_dir(input_images, maskcreator, outdir,subset_size=12):
    input_images_subsets = [
        input_images[i: i + subset_size]
        for i in range(0, len(input_images), subset_size)
    ]
    import os
    import mrcfile
    out_max_dir = os.path.join(outdir,"max_dir")
    out_max_val = os.path.join(outdir, "max_val")
    out_mask = os.path.join(outdir, "mask")
    try:
        os.makedirs(out_max_dir)
        os.makedirs(out_max_val)
        os.makedirs(out_mask)
    except FileExistsError:
        pass
    results = []
    for subset in input_images_subsets:
        enhanced_imags_list = enhance_images(subset, maskcreator)
        mstack = maskcreator.get_mask_stack()
        # Write them to disk
        for i, enhanced_imags in enumerate(enhanced_imags_list):
            for framei, framedict in enumerate(enhanced_imags):
                filename_no_ext = os.path.splitext(os.path.basename(subset[i]))[0]
                if len(enhanced_imags) > 1:
                    filename_no_ext = filename_no_ext + "_"+str(i).zfill(4)
                print("write", filename_no_ext)
                img_direction_path = os.path.join(out_max_dir,filename_no_ext+".mrc")
                img_val_path = os.path.join(out_max_val, filename_no_ext + ".mrc")
                out_mask_path = os.path.join(out_mask, filename_no_ext + ".mrc")

                with mrcfile.new(img_direction_path) as mrc:
                    mrc.set_data(np.flipud(framedict["max_angle"].astype(np.float32)))
                with mrcfile.new(img_val_path) as mrc:
                    mrc.set_data(np.flipud(framedict["max_value"].astype(np.float32)))
                with mrcfile.new(out_mask_path) as mrc:
                    mrc.set_data(mstack[20].astype(np.float32))

                results.append((img_val_path,img_direction_path))

    return results


def convolve(fft_image, fft_mask):

   # fft_mask = np.array(fft_mask)
    if len(fft_mask.shape) > 2:
        fft_image = np.expand_dims(fft_image, 2)
    result_fft = np.multiply(fft_mask, fft_image)
    result = np.fft.irfft2(result_fft, axes=(0, 1))
    result = np.fft.fftshift(result, axes=(0, 1))

    return result

def wrapper_fourier_stack(input_img_and_kernel):
    img_paths, kernels = input_img_and_kernel
    return enhance_image(fourier_kernel_stack=kernels, input_image=img_paths)

def wrapper_fourier_stack_paths(input_img_and_kernel):
    img_paths, kernels, slice = input_img_and_kernel
    return enhance_image_by_path(fourier_kernel_stack=kernels, input_image_path=img_paths, slice=slice)

def enhance_image_by_path(fourier_kernel_stack, input_image_path, slice=0):
    image = imagereader.image_read(input_image_path, use_mmap=True)
    if len(image.shape) == 3:
        original_image = image[slice, :, :]
    else:
        original_image = image
    # create square image with mask size
    height = original_image.shape[0]
    width = original_image.shape[1]
    max_dim = height if height > width else width
    scaling = 1.0*fourier_kernel_stack.shape[0]/max_dim

    #original_image_resized = cv2.resize(original_image, dsize=(0,0), fx=scaling, fy=scaling)
    original_image_resized = np.array(Image.fromarray(original_image).resize((int(original_image.shape[1]*scaling), int(original_image.shape[0]*scaling)), resample=Image.BILINEAR))

    vertical_offset = (fourier_kernel_stack.shape[0]-original_image_resized.shape[0])
    top_offset = int(vertical_offset/2)
    bottom_offset = top_offset + (0 if vertical_offset % 2 == 0 else 1)

    horizontal_offset = (fourier_kernel_stack.shape[0]-original_image_resized.shape[1])
    left_offset = int(horizontal_offset/2)
    right_offset = left_offset + (0 if horizontal_offset % 2 == 0 else 1)
   # fill_value = np.mean(original_image_resized)
   # sc = np.asscalar(np.array([fill_value]))
    '''
    input_image = cv2.copyMakeBorder(src=original_image_resized,
                                     top=top_offset,
                                     bottom=bottom_offset,
                                     left=left_offset,
                                     right=right_offset,
                                     borderType=cv2.BORDER_REPLICATE)
                                    # value=np.asscalar(np.array([fill_value])))
    '''
    input_image = np.pad(original_image_resized, pad_width=((top_offset,bottom_offset),(left_offset,right_offset)),mode="reflect")
    input_image_fft = np.fft.rfft2(input_image)

    number_kernels = fourier_kernel_stack.shape[2]
    result = convolve(input_image_fft, fourier_kernel_stack[:, :, 0])

    enhanced_images = np.empty((original_image_resized.shape[0], original_image_resized.shape[1], number_kernels))
    result_cropped = result[top_offset:(top_offset + original_image_resized.shape[0]),
                     left_offset:(left_offset + original_image_resized.shape[1])]
    enhanced_images[:, :, 0] = result_cropped
    for i in range(1,number_kernels):
        result = convolve(input_image_fft, fourier_kernel_stack[:, :, i])
        #crop result
        result_cropped = result[top_offset:(top_offset + original_image_resized.shape[0]),
                         left_offset:(left_offset + original_image_resized.shape[1])]

        enhanced_images[:, :, i] = result_cropped

    max = np.amax(enhanced_images, axis=2)
    maxID = np.argmax(enhanced_images, axis=2)
    return {"max_value": max, "max_angle": maxID}

def enhance_image(fourier_kernel_stack, input_image):
    input_image_fft = np.fft.rfft2(input_image)
    number_kernels = fourier_kernel_stack.shape[2]
    result = convolve(input_image_fft, fourier_kernel_stack[:, :, 0])
    enhanced_images = np.empty((result.shape[0], result.shape[1], number_kernels))
    enhanced_images[:, :, 0] = result
    for i in range(1,number_kernels):
        result = convolve(input_image_fft, fourier_kernel_stack[:, :, i])
        enhanced_images[:, :, i] = result

    max = np.amax(enhanced_images, axis=2)
    maxID = np.argmax(enhanced_images, axis=2)
    return {"max_value": max, "max_angle": maxID}
