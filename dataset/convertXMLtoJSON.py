"""
converterXMLtoJSON

detect all annotations in xml file
it works for one class in mask rcnn - damage class

@author Adonis Gonzalez

"""

import xml.etree.cElementTree as ET
import cv2
import os
import json
import sys
import os

ROOT_DIR = os.path.dirname(os.path.realpath(__file__))

def process_bar(count, total, status=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', status))
    sys.stdout.flush()


def grabNamesImages():
    path=[]
    train = os.path.join(ROOT_DIR, "train")
    val = os.path.join(ROOT_DIR, "val")
    path = [train,val]
    for file in path:
        files = os.listdir(file)
        for name in files:
            imgs = []
            with open(file + '/image.txt', 'w') as f:
                for item in files:
                    if (item.endswith('.jpg')):
                        f.write("%s\n" % item)
            f.close()
        print("List of images, images.txt, in", file)


def XMLtoJson():
    path = []
    train = os.path.join(ROOT_DIR, "train")
    val = os.path.join(ROOT_DIR, "val")
    path = [train, val]

    for dir in path:
        try:
            imgs_list = open(dir+'/image.txt','r').readlines()
        except OSError as err:
            print("no hay ficheros en :", dir)

        images, bndbox, size, polygon = {}, {}, {}, {}
        # images = []
        count = 1
        total = len(imgs_list)
        all_json = {}

        counterObject ={}
        xmin={}
        xmax={}
        ymin={}
        ymax={}
        regionsTemp={}

        regi = {}


        for img in imgs_list: #for each image in the list in image.txt
            process_bar(count, total)
            count += 1
            if 'jpg' in img:
                img_name = img.strip().split('/')[-1]
                namexml = (img_name.split('.jpg')[0])

                images.update({"filename": img_name})
                xml_n = namexml + '.xml'

                try:
                    tree = ET.ElementTree(file=dir+'/'+xml_n)
                    root = tree.getroot()

                except OSError as err:
                    print("no hay ficheros en :", dir)

                number = 0
                for child_of_root in root:
                    if child_of_root.tag == 'filename':
                        image_id = (child_of_root.text)
                        try:
                            sizetmp = os.path.getsize(dir+'/'+image_id)
                        except OSError as err:
                            print("no hay ficheros en :", dir)


                    if child_of_root.tag == 'object':

                        print("estamo aqui")


                        for child_of_object in child_of_root:

                            if child_of_object.tag == 'name':
                                category_id = child_of_object.text
                                counterObject[category_id] = number

                            if child_of_object.tag == 'bndbox':
                                for child_of_root in child_of_object:
                                    if child_of_root.tag == 'xmin':
                                        xmin[category_id] = int(child_of_root.text)

                                    if child_of_root.tag == 'xmax':
                                        xmax[category_id] = int(child_of_root.text)

                                    if child_of_root.tag == 'ymin':
                                        ymin[category_id] = int(child_of_root.text)

                                    if child_of_root.tag == 'ymax':
                                        ymax[category_id] = int(child_of_root.text)



                        xmintmp = int(xmax[category_id] - xmin[category_id]) / 2
                        xvalue = int(xmin[category_id] + xmintmp)


                        ymintemp = int(ymax[category_id] - ymin[category_id]) / 2
                        yvalue = int(ymin[category_id] + ymintemp)

                        regions, regions1 = {} , {}
                        regionsTemp = ({"all_points_x": (xmin[category_id], xvalue, xmax[category_id], xmax[category_id], xmax[category_id], xvalue, xmin[category_id], xmin[category_id], xmin[category_id]),
                                        "all_points_y": (ymin[category_id], ymin[category_id], ymin[category_id], yvalue, ymax[category_id], ymax[category_id], ymax[category_id], yvalue, ymin[category_id])})


                        #print(regionsTemp[category_id])
                        damage = {"damage": "damage"}
                        regions.update({"region_attributes": damage})


                        shapes = {"shape_attributes": regionsTemp}

                        regions.update(shapes)

                        polygon.update({"name": "polygon"})
                        regions.update(shapes)
                        regions.update(polygon)

                        #regions.update(regionsTemp[category_id])

                        #print(regions)
                        regi[number] = regions.copy()


                        # hasta aquí esta bien

                        regions = {"regions": regi}

                        images.update(regions)
                        size = {"size": sizetmp}
                        images.update(size)

                        all_json[img_name] = images.copy()
                        number = +1


    with open(dir+'/'+"dataset.json", "a") as outfile:
        json.dump(all_json, outfile)

       # open(dir+'/'+"dataset.json", "w").close()



if __name__ == "__main__":

    grabNamesImages()
    ## load image list from txt file

    XMLtoJson()





