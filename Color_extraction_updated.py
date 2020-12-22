import json
import csv
import cv2
import math
import numpy as np
import sys

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

# final_list = []
# for i in json_data['Drawing']['Blocks']:
#     for j in i["Entities"]:
#         if j.get("Color") and j['Color']['Color_Method'] == 3 and j['Type'] == "Polyline":
#             tl = []
#             for k in j['Vertices']:
#                 DWG_X = float(k["Location"]["x"])
#                 DWG_Y = float(k["Location"]["y"])
#
#                 X = int((DWG_X - DWG_Min_Point_X) * Scale_X)
#                 Y = int(Raster_Height - (DWG_Y - DWG_Min_Point_Y) * Scale_Y)
#
#                 tl.append([X, Y])
#             pts = np.array([tl], np.int32)
#             cv2.polylines(image, [pts], False, (153, 51, 255), 2)

final_list = []
for i in json_data['Drawing']['Blocks']:
        for j in i['Entities']:
            temp_list = []
            if j['Type'] == "MText":
                print(j['Text_String'])
                xmin = int((float(j["Entity_Extents"]["Minimum_Point"]["x"]) - DWG_Min_Point_X) * Scale_X)
                ymin = int(Raster_Height - (float(j["Entity_Extents"]["Minimum_Point"]["y"]) - DWG_Min_Point_Y) * Scale_Y)
                xmax = int((float(j["Entity_Extents"]["Maximum_Point"]["x"]) - DWG_Min_Point_X) * Scale_X)
                ymax = int(Raster_Height - (float(j["Entity_Extents"]["Maximum_Point"]["y"]) - DWG_Min_Point_Y) * Scale_Y)
                temp_list.append(xmin)
                temp_list.append(ymin)
                temp_list.append(xmax)
                temp_list.append(ymax)
            if len(temp_list) != 0:
                final_list.append(temp_list)
    # return final_list
    
cv2.imwrite("color_output.jpg", image)


