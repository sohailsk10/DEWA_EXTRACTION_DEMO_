import os
from PIL import Image
import cv2
import csv
import json
import requests
import copy
import numpy as np


INPUT_IMAGE = r'TED_Image_2_6500.png'
OUTPUT_IMAGE = INPUT_IMAGE.split('.')[0] + "_output.jpg"
DIR = INPUT_IMAGE.split('.')[0] + '_split'
INPUT_CSV = r"NOC_TED_compare\csv\TED_Image_2_6500.csv"
INPUT_JSON = r"TED_Tailormade\TED_Image_2_6500.json"
OUTPUT_CSV = "Output_CSV\\" + INPUT_IMAGE.split('.')[0] + '_output.csv'

DWG_Min_Point_X = 0
DWG_Min_Point_Y = 0
DWG_Max_Point_X = 11
DWG_Max_Point_Y = 8.5
Raster_Width = 6500
Raster_Height = 5023
Scale_X = 590.909
Scale_Y = 590.941

if not os.path.exists(DIR):
    os.makedirs(DIR)
else:
    for root, dirs, files in os.walk(DIR, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))

def draw_in_image(type, type_array, image):
    if type == "polyline":
        for Poly_list in type_array:
            pts = np.array(Poly_list, np.int32)
            isClosed = False
            color = (0, 0, 255)
            thickness = 5
            image = cv2.polylines(image, [pts], isClosed, color, thickness)

    if type == "line":
        min_list = type_array[0]
        max_list = type_array[1]
        color = (0, 255, 0)
        thickness = 5
        for i in range(len(min_list)):
            image = cv2.line(image, tuple(min_list[i]), tuple(max_list[i]), color, thickness)
            
    if type == "mtext":
        color = (0, 255, 255)
        thickness = 5
        for rect in type_array:
            image = cv2.rectangle(image, (rect[0], rect[1]), (rect[2], rect[3]), color, thickness)
    return image


def imgcrop(input, xPieces, yPieces):
    global count, arr_list
    filename, file_extension = os.path.splitext(input)
    im = Image.open(input)
    imgwidth, imgheight = im.size
    height = imgheight // yPieces
    width = imgwidth // xPieces
    for i in range(0, yPieces):
        for j in range(0, xPieces):
            box = (j * width, i * height, (j + 1) * width, (i + 1) * height)
            a = im.crop(box)
            a = a.convert('RGB')
            filename_to_save = DIR + '/' + filename + "0" + str(i) + "0" + str(j) + file_extension
            a.save(filename_to_save)

def area_crop(file_name, imagen, imght, imgwdt, csv_file):
    data = {}
    requests.packages.urllib3.disable_warnings()
    api_url_label_ocr_3 = "https://195.229.90.114/visual-insights/api/dlapis/490f1923-7916-464c-a883-3f97c8445daf"
    # api_url_label_ocr_3 = "https://195.229.90.110/visual-insights/api/dlapis/c7d21db9-8cc2-4b0b-ac51-f7484b847a5a"
    with open(file_name, 'rb') as f:
        s = requests.Session()
        r = s.post(api_url_label_ocr_3, files={'files': (file_name, f), 'confthre': '0.80'}, verify=False, timeout=10)
        data = json.loads(r.text)

    testdata = data["classified"]
    image = cv2.imread(file_name)
    imgh, imgw, _ = image.shape

    writer = csv.writer(csv_file)

    for counter in range((len(testdata))):
        minX = int(testdata[counter].get('xmin'))
        minY = int(testdata[counter].get('ymin'))
        maxX = int(testdata[counter].get('xmax'))
        maxY = int(testdata[counter].get('ymax'))
        label = testdata[counter].get('label')
        cv2.rectangle(image, (minX, minY), (maxX, maxY), (0, 0, 255), 2)

        if imagen == 0:
            writer.writerow([imagen, minX, minY, maxX, maxY, label])
        if imagen == 1:
            writer.writerow([imagen, (minX + imgwdt), minY, (maxX + imgwdt), maxY, label])
        if imagen == 2:
            writer.writerow([imagen, (minX + imgwdt + imgwdt), minY, (maxX + imgwdt + imgwdt), maxY, label])
        if imagen == 3:
            writer.writerow([imagen, (minX), (minY + imght), (maxX), (maxY + imght), label])
        if imagen == 4:
            writer.writerow([imagen, (minX + imgwdt), (minY + imght), (maxX + imgwdt), (maxY + imght), label])
        if imagen == 5:
            writer.writerow([imagen, (minX + imgwdt + imgwdt), (minY + imght), (maxX + imgwdt + imgwdt), (maxY + imght), label])
        if imagen == 6:
            writer.writerow([imagen, (minX), (minY + imght + imght), (maxX), (maxY + imght + imght), label])
        if imagen == 7:
            writer.writerow([imagen, (minX + imgwdt), (minY + imght + imght), (maxX + imgwdt), (maxY + imght + imght), label])
        if imagen == 8:
            writer.writerow([imagen, (minX + imgwdt + imgwdt ), (minY + imght + imght), (maxX + imgwdt + imgwdt ), (maxY + imght + imght), label])

def polyline(data):
    final_list = []
    for i in data['Drawing']['Blocks']:
        for j in i["Entities"]:
            if j['Type'] == "Polyline":
                alist = []
                for k in j['Vertices']:
                    DWG_X = float(k["Location"]["x"])
                    DWG_Y = float(k["Location"]["y"])

                    X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
                    Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)
                    alist.append([X, Y])
                final_list.append(alist)
    return final_list

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)

def check(x1, y1, x2, y2, x3, y3, x4, y4, x, y):
    A = (area(x1, y1, x2, y2, x3, y3) + area(x1, y1, x4, y4, x3, y3))
    A1 = area(x, y, x1, y1, x2, y2)
    A2 = area(x, y, x2, y2, x3, y3)
    A3 = area(x, y, x3, y3, x4, y4)
    A4 = area(x, y, x1, y1, x4, y4)
    return (A == A1 + A2 + A3 + A4)

def discard_upolyline(polylist, csv_data):
    dd = {}
    for rect in csv_data:
        print("Rect", rect)
        a1 = int(rect[3])
        a2 = int(rect[4])
        a3 = int(rect[5])
        a4 = int(rect[6])

        for i in range(len(polylist)):
            ilist = []
            for j in polylist[i]:
                if (check(a1, a2, a3, a2, a3, a4, a1, a4, int(j[0]), int(j[1]))):
                    ilist.append(j)
            if len(ilist) != 0:
                dd[i] = ilist
    return dd

print("cropping input image...")    
imgcrop(INPUT_IMAGE, 3, 3)

tf = len([name for name in os.listdir(DIR)])
tfn = [name for name in os.listdir(DIR)]

imager = cv2.imread(INPUT_IMAGE)
height, width, channel = imager.shape
var_width = int(width // 3)
var_height = int(height // 3)

csv_file = open(OUTPUT_CSV, "w")
writer = csv.writer(csv_file)
writer.writerow(["blockno", "xmin", "ymin", "xmax", "ymax", "label"])

print("detecting from Visual Insight...")
print("writing symbols in " + OUTPUT_CSV + "...")
for i in range(tf):
    area_crop(os.path.join(DIR, tfn[i]), i, var_height, var_width, csv_file)

json_data = {}
print("getting json...")
with open(INPUT_JSON, "r") as f:
    json_data = json.load(f)

csv_data = []
print("getting csv...")
print("writing text in " + OUTPUT_CSV + "...")
with open(INPUT_CSV, "r") as csv_file:
    reader = csv.reader(csv_file)
    for data in reader:
        if data != []:
            csv_data.append(data)
            writer.writerow(data)
    csv_data.remove(csv_data[0])

print("getting polylist...")
polylist = polyline(json_data)

print("discarding unwanted polylist...")
ddict = discard_upolyline(polylist, csv_data)

final_deleting_list = []
for i in range(len(polylist)):
    temp_l = polylist[i]
    temp_l1 = copy.copy(temp_l)
    if ddict.get(i) != None:
        d_list = ddict.get(i)
        for x in temp_l:
            if x in d_list:
                temp_l1.remove(x)
    temp_l = copy.copy(temp_l1)
    final_deleting_list.append(temp_l)
    
writer.writerow(["Polyline", "X", "Y"])
print("writing polylines in " + OUTPUT_CSV + "...")
for i in final_deleting_list:
    if i:
        counter = 1
        for j in i:
            writer.writerow([counter, j[0], j[1]])
            counter += 1

mod_image = draw_in_image("polyline", final_deleting_list, imager)
cv2.imwrite(OUTPUT_IMAGE, mod_image)
print("output saved in " + OUTPUT_CSV)
print("output image saved", OUTPUT_IMAGE)