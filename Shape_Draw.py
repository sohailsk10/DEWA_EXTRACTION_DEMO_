import cv2
import numpy as np
import csv
import os

DWG_Min_Point_X = 15.8333
DWG_Min_Point_Y = 37.3333
DWG_Max_Point_X = 776
DWG_Max_Point_Y = 574.833
Raster_Width = 5000
Raster_Height = 3536
Scale_X = 6.5775
Scale_Y = 6.5786

OUTPUT_CSV = r'sld_24.csv'
if os.path.exists(OUTPUT_CSV):
    os.remove(OUTPUT_CSV)


def draw_in_image(type, type_array, image):
    if type == "polyline":
        for Poly_list in type_array:
            pts = np.array(Poly_list, np.int32)
            isClosed = False
            color = (0, 0, 255)
            thickness = 2
            image = cv2.polylines(image, [pts], isClosed, color, thickness)

    if type == "line":
        min_list = type_array[0]
        max_list = type_array[1]
        color = (255, 0, 0)
        thickness = 9
        for i in range(len(min_list)):
            image = cv2.line(image, tuple(min_list[i]), tuple(max_list[i]), color, thickness)

    if type == "MText":
        for i in type_array:
            color = (0, 255, 0)
            thickness = 3
            image = cv2.rectangle(image, (i[0], i[1]), (i[2], i[3]), color, thickness)

    # if type == "circle":
    #     rect_min_list = type_array[0]
    #     rect_max_list = type_array[1]
    #     color = (255, 0, 0)
    #     thickness = 5
    #     print(type_array[0][0])
    #     print(type_array[0][1])
    #     for i in range(len(rect_min_list)):
    #         # cx = type_array[i][0]
    #         # cy = type_array[i][1]
    #         image = cv2.rectangle(image, tuple(rect_min_list[i]), tuple(rect_max_list[i]), color, thickness)
            # image = cv2.circle(image, tuple(type_array[i][0]), type_array[i][1], color, thickness)
    # if type == "arc":
    #     arc_list = type_array[0]
    #     angle_list = type_array[1]
    #     print(type_array[0][0])
    #     print(type_array[0][1])
    #
    #     for i in range(len(arc_list)):
    #         center = tuple(arc_list[i][0])
    #         radius = type_array[i][1]
    #         axes = (radius, radius)
    #         start_angle = angle_list[i][0]
    #         end_angle = angle_list[i][1]
    #         thickness = 5
    #         color = (255, 0, 255)
    #         image = cv2.ellipse(image, center, axes, start_angle, end_angle, color, thickness)
    return image


def PolyLine(data):
    with open(OUTPUT_CSV, "w") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Polyline", "X", "Y"])
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

                        writer.writerow([k["Index"], X, Y])
                        alist.append([X, Y])
                    final_list.append(alist)
    return final_list

def Line(data):
    with open(OUTPUT_CSV, "a") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Line", "xmin", "ymin", "xmax", "ymax"])
        min_list = []
        max_list = []
        for i in data['Drawing']['Blocks']:
            # print(i['Entities'])
            for j in i['Entities']:
                if j['Type'] == "Line":
                    minx = float(j['Start_Point']["x"])
                    miny = float(j['Start_Point']["y"])
                    maxx = float(j['End_Point']["x"])
                    maxy = float(j['End_Point']["y"])

                    x = int((minx - DWG_Min_Point_X) * Scale_X)
                    y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                    X = int((maxx - DWG_Min_Point_X) * Scale_X)
                    Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                    writer.writerow(["LINE", x, y, X, Y])
                    min_list.append([x, y])
                    max_list.append([X, Y])
    return min_list, max_list


def Rect_Text(data):
    with open(OUTPUT_CSV, "a") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["xmin", "ymin", "xmax", "ymax"])
        rect_list = []
        for i in data['Drawing']['Blocks']:
            for j in i['Entities']:
                if j['Type'] == "MText":
                    minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                    miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                    maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                    maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                    Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
                    Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                    Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
                    Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                    writer.writerow([Rect_x, Rect_y, Rect_X, Rect_Y])
                    rect_list.append([Rect_x, Rect_y, Rect_X, Rect_Y])
    return rect_list



# def Circle(data):
#     circle_list = []
#     circle_list_new = []
#     for i in data['Drawing']['Blocks']:
#         # print(i['Entities'])
#         for j in i['Entities']:
#             if j['Type'] == "Viewport" or j['Type'] == "Table":
#                 continue
#
#             if j['Type'] == "Circle":
#                 # ccenter_x = float(j["Center"]["x"])
#                 # ccenter_y = float(j["Center"]["y"])
#                 # r = float(j["Radius"])
#
#                 Min_x = float(j['Entity_Extents']['Minimum_Point']['x'])
#                 Min_y = float(j['Entity_Extents']['Minimum_Point']['y'])
#                 Max_x = float(j['Entity_Extents']['Maximum_Point']['x'])
#                 Max_y = float(j['Entity_Extents']['Maximum_Point']['y'])
#
#                 X = int((Min_x - DWG_Min_Point_Y) * Scale_X)
#                 Y = int(Raster_Height - (Min_y - DWG_Min_Point_Y) * Scale_Y)
#                 Max_X = int((Max_x - DWG_Min_Point_X) * Scale_X)
#                 Max_Y = int(Raster_Height - (Max_y - DWG_Min_Point_Y) * Scale_Y)
#
#                 circle_list.append([X, Y])
#                 circle_list_new.append([Max_X, Max_Y])
#
#                 # x = int((ccenter_x - DWG_Min_Point_X) * Scale_X)
#                 # y = int(Raster_Height - (ccenter_y - DWG_Min_Point_Y) * Scale_Y)
#                 # radi = int(r - DWG_Min_Point_X) * Scale_X
#                 # circle_list.append([[x, y], int(radi)])
#     return circle_list, circle_list_new

# def Arc(data):
#     arc_list = []
#     angle_list = []
#     for i in data['Drawing']['Blocks']:
#         # print(i['Entities'])
#         for j in i['Entities']:
#             if j['Type'] == "Viewport" or j['Type'] == "Table":
#                 continue
#
#             if j['Type'] == "Arc":
#                 ccenter_x = float(j["Center"]["x"])
#                 ccenter_y = float(j["Center"]["y"])
#                 start_angle = float(j["Start_Angle"])
#                 end_angle = float(j["End_Angle"])
#                 r = float(j["Radius"])
#
#                 x = int((ccenter_x - DWG_Min_Point_X) * Scale_X)
#                 y = int(Raster_Height - (ccenter_y - DWG_Min_Point_Y) * Scale_Y)
#                 # radi = int(r - DWG_Min_Point_X) * Scale_X
#                 arc_list.append([[x, y], int(r)])
#                 angle_list.append([start_angle, end_angle])
#     return arc_list, angle_list