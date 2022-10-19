# import os
# import cv2
import json
import numpy as np 
import PIL.Image
import PIL.ImageDraw
import math
import matplotlib.pyplot as plt
import glob

def shape_to_mask(img_shape, points, shape_type=None,
                  line_width=10, point_size=5):
    mask = np.zeros(img_shape[:2], dtype=np.uint8)
    mask = PIL.Image.fromarray(mask)
    draw = PIL.ImageDraw.Draw(mask)
    for polygon in points:
        xy = [tuple(point) for point in polygon]
        if shape_type == 'circle':
            assert len(xy) == 2, 'Shape of shape_type=circle must have 2 points'
            (cx, cy), (px, py) = xy
            d = math.sqrt((cx - px) ** 2 + (cy - py) ** 2)
            draw.ellipse([cx - d, cy - d, cx + d, cy + d], outline=1, fill=1)
        elif shape_type == 'rectangle':
            assert len(xy) == 2, 'Shape of shape_type=rectangle must have 2 points'
            draw.rectangle(xy, outline=1, fill=1)
        elif shape_type == 'line':
            assert len(xy) == 2, 'Shape of shape_type=line must have 2 points'
            draw.line(xy=xy, fill=1, width=line_width)
        elif shape_type == 'linestrip':
            draw.line(xy=xy, fill=1, width=line_width)
        elif shape_type == 'point':
            assert len(xy) == 1, 'Shape of shape_type=point must have 1 points'
            cx, cy = xy[0]
            r = point_size
            draw.ellipse([cx - r, cy - r, cx + r, cy + r], outline=1, fill=1)
        else:
            assert len(xy) > 2, 'Polygon must have points more than 2'
            draw.polygon(xy=xy, outline=1, fill=1)
    mask = np.array(mask, dtype=bool)
    return mask

# path = '/home/rushabh/AMT/Framos-data/small dataset/*.json'
path = '/home/messnix/bagfiles/pam_images_annotated/annotations/*.json'
#path = '/home/messnix/bagfiles/test/test_png/*.json'

json_files = glob.glob(path)
counter = 0
st = 0

for file in json_files:
    with open(file, "r",encoding="utf-8") as f:
        dj = json.load(f)
    points = []
    for labels in dj['shapes']:
        if labels['label'] == 'Slag':
            points.append(labels['points'])
            print(len(points))
            print(points[st])
            print(type(points))
            st += 1
    st = 0

    # mask = shape_to_mask((dj['imageHeight'],dj['imageWidth']), dj['shapes'][0]['points'], shape_type=None,line_width=1, point_size=1)
    mask = shape_to_mask((dj['imageHeight'], dj['imageWidth']), points, shape_type=None,
                         line_width=1, point_size=1)
    mask_img = mask.astype(int)#boolean to 0,Convert to 1
    plt.imsave(str(file).replace(".json", "_mask.png"), mask_img)
    counter += 1
    print(str(counter)+" images saved!")
