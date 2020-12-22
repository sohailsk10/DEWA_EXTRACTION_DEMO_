import json
import csv
import cv2
import math
import numpy as np

json_read = r'LinkList_2020_W32_20_02_06_pink_Box\TrialTrench_Sample2_6500.json'

image_name = 'LinkList_2020_W32_20_02_06_pink_Box\TrialTrench_Sample2_6500.png'
image = cv2.imread(image_name)

DWG_Min_Point_X = -0.628932
DWG_Min_Point_Y = 0.778888
DWG_Max_Point_X = 32.5039
DWG_Max_Point_Y = 22.5905
Raster_Width = 6500
Raster_Height = 4280
Scale_X = 196.18
Scale_Y = 196.225

with open(json_read, "r") as f:
    json_data = json.load(f)
    print("Reading Json file....")

# def PolyLine(data):
# final_list = []
# for i in json_data['Drawing']['Blocks']:
#     for j in i["Entities"]:
#                 # print(j['Color'])
#                 if j['Type'] == "Polyline":
#                     if j.get("Color"):
#                         if j['Color']['Color_Method'] == 3:
#                             for k in j['Vertices']:
#                                 DWG_X = float(k["Location"]["x"])
#                                 DWG_Y = float(k["Location"]["y"])
#
#                                 X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
#                                 Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)
# print(X, Y)
final_list = []
for i in json_data['Drawing']['Blocks']:
    for j in i["Entities"]:
        if j['Type'] == "Polyline":
            if j.get("Color"):
                if j['Color']['Color_Method'] == 3:
                    alist = []
                    for k in j['Vertices']:
                        DWG_X = float(k["Location"]["x"])
                        DWG_Y = float(k["Location"]["y"])

                        X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
                        Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)

                        # writer.writerow([k["Index"], X, Y])
                        alist.append([X, Y])
                        # final_list.append(alist)
                            # print(i[0][0])
                        pts = np.array([alist], np.int32)
                        isClosed = False
                        color = (255, 0, 255)
                        thickness = 2

                        image = cv2.polylines(image, [pts], isClosed, color, thickness)


                if j['Color']['Color_Method'] == 0:
                    alist = []
                    for k in j['Vertices']:
                        DWG_X = float(k["Location"]["x"])
                        DWG_Y = float(k["Location"]["y"])

                        X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
                        Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)

                        # writer.writerow([k["Index"], X, Y])
                        alist.append([X, Y])
                        # final_list.append(alist)
                            # print(i[0][0])
                        pts = np.array([alist], np.int32)
                        isClosed = False
                        color = (0,255, 0)
                        thickness = 2

                        image = cv2.polylines(image, [pts], isClosed, color, thickness)

                if j['Color']['Color_Method'] == 2:
                    alist = []
                    for k in j['Vertices']:
                        DWG_X = float(k["Location"]["x"])
                        DWG_Y = float(k["Location"]["y"])

                        X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
                        Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)

                        # writer.writerow([k["Index"], X, Y])
                        alist.append([X, Y])
                        # final_list.append(alist)
                            # print(i[0][0])
                        pts = np.array([alist], np.int32)
                        isClosed = False
                        color = (0, 255, 255)
                        thickness = 2

                        image = cv2.polylines(image, [pts], isClosed, color, thickness)



cv2.imwrite("color.jpg", image)
print("completed")

#     # writer.writerow([k["Index"], X, Y])
#     alist.append([X, Y])
