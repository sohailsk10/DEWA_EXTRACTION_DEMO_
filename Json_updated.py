import json
import cv2
import numpy as np
from Shape_Draw import *
import csv

image = cv2.imread("sld.jpg")
json_data = None
csv_data = []

def delete_from_polylist(polylist, final_deleting_list):
    fpl = []
    for dl in final_deleting_list:
        for i in polylist:
            if dl in i:
                i.remove(dl)
        fpl.append(i)
    return fpl

def discard_upolyline1(polylist, csv_data):
    dd = {}
    for rect in csv_data:
        for i in range(len(polylist)):
            ilist = []
            for j in polylist[i]:
                if int(rect[3]) < int(j[0]) < int(rect[5]) and int(rect[4]) < int(j[1]) < int(rect[6]):
                    ilist.append(j)
            if len(ilist) != 0:
                dd[i] = ilist
    return dd

with open("sld.json", "r") as f:
    json_data = json.load(f)

with open("sld_1.csv", "r") as csv_file:
    reader = csv.reader(csv_file)
    for data in reader:
        if data != []:
            temp = 0
            try:
                temp = float(data[3])
            except ValueError:
                continue
            if temp != 0:
                csv_data.append(data)


polylist = PolyLine(json_data)

ddict = discard_upolyline1(polylist, csv_data)

mod_image = draw_in_image("polyline", ddict, polylist, image)

cv2.imwrite("sld_out2.jpg", mod_image)
