import json
import copy
import csv
import cv2

json_read = r'LinkList_2020_W32_20_02_06\E2030199-APPROVED-Done_page_25.json'

image_name = 'LinkList_2020_W32_20_02_06\E2030199-APPROVED-Done_page_25.png'
image = cv2.imread(image_name)

DWG_Min_Point_X = 15.8333
DWG_Min_Point_Y = 37.3333
DWG_Max_Point_X = 776
DWG_Max_Point_Y = 574.833
Raster_Width = 5000
Raster_Height = 3536
Scale_X = 6.5775
Scale_Y = 6.5786

with open(json_read, "r") as f:
    json_data = json.load(f)
    print("Reading Json file....")

OUTPUT_CSV = "Shape_extract_new.csv"

Csv_file = open(OUTPUT_CSV, 'w')
writer = csv.writer(Csv_file)
writer.writerow(["Arc", "xmin", "ymin", "xmax", "ymax"])

# def PolyLine(data):
# with open(OUTPUT_CSV, "w") as coords_csv_file:
#     writer = csv.writer(coords_csv_file)
#     writer.writerow(["Polyline", "X", "Y"])
# with open(OUTPUT_CSV, "w") as coords_csv_file:
#     writer = csv.writer(coords_csv_file)
#     writer.writerow(["Arc", "xmin", "ymin", "xmax", "ymax"])
final_list = []
for i in json_data['Drawing']['Blocks']:
    for j in i["Entities"]:
        if j.get("Feature_Type"):
            if j['Feature_Type']['Type'] == "Arc":
                # print(j['Entity_Extents'])
                alist = []
                for k in j['Entity_Extents']:
                    minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                    miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                    maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                    maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                    Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
                    Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                    Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
                    Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                    writer.writerow(["Arc", Rect_x, Rect_y, Rect_X, Rect_Y])
                    cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 255, 0), 2)
                    # coords_csv_file.close()

            if j['Feature_Type']['Type'] == "Circle":
                alist = []
                for k in j['Entity_Extents']:
                    minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                    miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                    maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                    maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                    Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
                    Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                    Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
                    Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                    writer.writerow(["Circle", Rect_x, Rect_y, Rect_X, Rect_Y])
                    cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 255, 255), 2)

# if j['Layer'] == "Text":
#     alist = []
#     for k in j['Entity_Extents']:
#         # print(k)
#         minx = float(j['Entity_Extents']['Minimum_Point']["x"])
#         miny = float(j['Entity_Extents']['Minimum_Point']["y"])
#         maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
#         maxy = float(j['Entity_Extents']['Maximum_Point']["y"])
#
#         Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
#         Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
#         Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
#         Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)
#
#         cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 0, 255), 2)

# Rect_x = int((302 - DWG_Min_Point_X) * Scale_X)
# Rect_y = int(Raster_Height - (299.167 - DWG_Min_Point_Y) * Scale_Y)
# Rect_X = int((303.833 - DWG_Min_Point_X) * Scale_X)
# Rect_Y = int(Raster_Height - (301 - DWG_Min_Point_Y) * Scale_Y)
#
# cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 0, 255), 2)

# radius = int(0.916667)
# color = (0, 0, 255)
#
# # Line thickness of 2 px
# thickness = 9
# cv2.circle(image, tuple((Rect_x, Rect_y)), radius, color, thickness)

# Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
# Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)


cv2.imwrite("E2030199-APPROVED-Done_page_25_5000_rect.jpg", image)

# writer.writerow([k["Index"], X, Y])
# alist.append([X, Y])
# final_list.append(alist)
# return final_list
