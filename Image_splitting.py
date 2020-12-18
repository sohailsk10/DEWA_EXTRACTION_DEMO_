import os, pytesseract
from PIL import Image
import cv2
import csv
import json
import requests


INPUT_IMAGE = 'sld_25.jpg'
DIR = INPUT_IMAGE.split('.')[0] + '_split'
csv_read = "sld_25.csv"
json_read = "sld_25.json"
Output_csv = "sld_25_output_new_1012.csv"
OUTPUT_CSV = INPUT_IMAGE.split('.')[0] + '_output.csv'


if not os.path.exists(DIR):
    os.makedirs(DIR)
else:
    for root, dirs, files in os.walk(DIR, topdown=False):
        for name in files:
            os.remove(os.path.join(root, name))
        for name in dirs:
            os.rmdir(os.path.join(root, name))


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
            print(filename_to_save)

def area_crop(file_name, imagen, imght, imgwdt, csv_file):
    data = {}
    requests.packages.urllib3.disable_warnings()
    api_url_label_ocr_3 = "https://195.229.90.114/visual-insights/api/dlapis/490f1923-7916-464c-a883-3f97c8445daf"
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


imgcrop(INPUT_IMAGE, 3, 3)

tf = len([name for name in os.listdir(DIR)])
tfn = [name for name in os.listdir(DIR)]

im = cv2.imread(INPUT_IMAGE)
height, width, channel = im.shape
var_width = int(width // 3)
var_height = int(height // 3)

csv_file = open(OUTPUT_CSV, "w")
print(OUTPUT_CSV)
writer = csv.writer(csv_file)
writer.writerow(["blockno", "xmin", "ymin", "xmax", "ymax", "label"])

for i in range(tf):
    area_crop(os.path.join(DIR, tfn[i]), i, var_height, var_width, csv_file)





