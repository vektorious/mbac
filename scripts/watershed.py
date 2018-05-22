import os
import sys
import glob

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm

import cv2
from AmbrosioTortorelliMinimizer import *

dish_radius = 100

def inner_contour(image_path):
    img = cv2.imread(image_path, 0)
    #call detect_container from tools_single.py
    inner_cnt = detect_container(img)

    #conver the frame to BGR
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    #get minimin enclosing circle and draw it 
    #along with inner contour
    (x,y),radius = cv2.minEnclosingCircle(inner_cnt)
    center = (int(x),int(y))
    radius = int(radius)
    circle = cv2.circle(img,center,radius,(0,255,0),1)
    return inner_cnt, circle


def detect_container(img):
    """ detects the inner boundary of the petridish in an image
    input
        img: grayscale image as numpy array
    ouput: 
        cnt: an opencv contour object representing the inner border 
              of the petridish
    """
    # edge detection
    edges = cv2.Canny(img,18,32)

    # dilate edges
    # to close small openings
    kernel = np.ones((2,2),np.uint8)
    edges = cv2.dilate(edges,kernel,iterations = 2)

    #find contours
    im2, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, 
                                               cv2.CHAIN_APPROX_NONE)

    #detect the biggest contour
    outer_cntIndex = np.argmax([cv2.contourArea(cnt) for cnt in contours])
    outer_cnt = contours[outer_cntIndex]

    #filter contours that have area > 0.6*Area of max contour
    filt_cnts = [cnt for cnt in contours if cv2.contourArea(cnt)>0.6*cv2.contourArea(outer_cnt)]

    #get the minimun contour of the filterd ones
    inner_cntIndex = np.argmin([cv2.contourArea(cnt) for cnt in filt_cnts])
    inner_cnt= filt_cnts[inner_cntIndex]
    return inner_cnt

def remove_dish(im, inner_cnt):
    mask = np.zeros_like(im) # Create mask where white is what we want, black otherwise
    idx = -1
    cv2.drawContours(mask, inner_cnt, idx, 255, -1) # Draw filled contour in mask
    out = np.zeros_like(im) # Extract out the object and place into output image
    out[mask == 255] = im[mask == 255]
    return out

def cmask(index,radius,array):
    a,b = index
    nx,ny = array.shape
    y,x = np.ogrid[-a:nx-a,-b:ny-b]
    mask = x*x + y*y > radius*radius
    return mask

def calc_background(images, n=10):
    """ Compute average background from first 10 images, excluding first ones"""
    grays = [cv2.imread(images[i], cv2.IMREAD_GRAYSCALE) for i in range(2,n)]
    gray0 = np.mean(np.asarray(grays), axis=0)
    #mask1 = cmask(np.array(gray0.shape)/2, dish_radius+5, gray0)
    #gray0[mask1] = np.mean(gray0)
    return cv2.convertScaleAbs(gray0)

def ambrosio(img):
    solver = AmbrosioTortorelliMinimizer(img)
    img, edges = solver.minimize()
    return img, edges

def measure_blob(img_path, background):
    img = cv2.imread(img_path)
    gray = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

    # Remove dish
    #inner_cnt, circle = inner_contour(img_path)
    # Simple circular mask, to be substituted by remove dish
    mask1 = cmask(np.array(gray.shape)/2, dish_radius+5, gray)
    gray[mask1] = np.mean(gray)
    background[mask1] = np.mean(background)
    gray = gray.astype(np.uint8)
    background = background.astype(np.uint8)

    # Subtract background from image
    im = ambrosio(cv2.subtract(gray, background))[0]
    im[mask1] = 0.0
    im = cv2.blur(im, (7,7))

    #plt.imshow(np.hstack([gray_smooth, background_smooth,im]))
    #a = plt.imshow(np.hstack([im]))
    #plt.colorbar(a)
    #plt.show()

    # First threshold. I keep the easy solution. To be improved
    limit = 100
    ret, thresh = cv2.threshold(im,limit,255,cv2.THRESH_BINARY_INV)
    #limit = 4.*np.std(background)
    #ret, thresh = cv2.threshold(im,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)

    # noise removal
    kernel = np.ones((3,3),np.uint8)
    opening = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel, iterations = 2)
    # sure background area
    sure_bg = cv2.dilate(opening,kernel,iterations=3)
    # Finding sure foreground area
    dist_transform = cv2.distanceTransform(opening,cv2.DIST_L2,5)
    ret, sure_fg = cv2.threshold(dist_transform,0.1*dist_transform.max(),255,0)
    # Finding unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg,sure_fg)
    
    # Marker labelling
    ret, markers = cv2.connectedComponents(sure_fg)
    # Add one to all labels so that sure background is not 0, but 1
    markers = markers+1
    # Now, mark the region of unknown with zero
    markers[unknown==255] = 0
    
    im_out = cv2.cvtColor(im,cv2.COLOR_GRAY2RGB)
    markers = cv2.watershed(im_out, markers)
    im_out[markers == -1] = [255,0,0]
    
    area = np.count_nonzero(markers == 1)
    return im_out, area


def calc_area_max(images, background):
    # Use last image. But now using fixed value
    #area_max = measure_blob(images[-1], [], 1, 10, background)[0]
    area_max = 25000
    return area_max

def process_images(images, partial=True):
    os.system('rm -r ./images/*')
    background0 = calc_background(images)
    area_max = calc_area_max(images, background0)
    if partial:
        images = images[0::5]
    num_images = len(images)
    areas = []
    for img_path in images:
        print('Processing: {}'.format(img_path))
        img, area = measure_blob(img_path, background0)
        areas.append(area)
        plot_step(img, img_path, areas, num_images, area_max)
    areas = np.asarray(areas)
    np.savetxt('areas.dat', areas, fmt='%i')
    return areas

def plot_step(img, img_path, areas, num_images, area_max):
    outputname = os.path.splitext(os.path.basename(img_path))[0]
    area = areas[-1]
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(20,6))
    axes[0].imshow(img)
    axes[0].set_title('{0}  - area: {1}'.format(outputname, area))
    axes[1].plot(areas, '.k')
    axes[1].set_xlim(0, num_images)
    axes[1].set_ylim(0, area_max)
    fig.savefig('./images/'+outputname+'.png', bbox_inches='tight')
    plt.close()
    return

def plot_areas(areas):
    fig, axes = plt.subplots(nrows=1, ncols=1)
    axes.plot(areas, '.k')
    fig.savefig('areas.png', bbox_inches='tight')

def plot_area_curve(areas):
    np.savetxt('areas.dat', areas, fmt='%i')
    fig, axes = plt.subplots(nrows=1, ncols=1)
    axes.plot(areas, '.k')
    fig.savefig('areas.png', bbox_inches='tight')

def make_video():
    try:
        os.system("ffmpeg -framerate 25 -pattern_type glob -i './images/*.png' -y -movflags faststart -pix_fmt yuv420p -vf 'scale=trunc(iw/2)*2:trunc(ih/2)*2' video.mp4")
    except:
        pass

if __name__ == '__main__':
    images_path = sys.argv[-1]
    if not os.path.isdir(images_path):
        print('Usage: python watershed.py /path/to/images/')
        sys.exit(1)
    images = sorted(glob.glob(images_path+'image*jpg'))
    areas = process_images(images, partial=False)
    plot_areas(areas)
    make_video()

