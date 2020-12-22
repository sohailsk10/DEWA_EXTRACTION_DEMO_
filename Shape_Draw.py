import cv2
import numpy as np
import csv
import sys
import json

DWG_MINX, DWG_MINY, DWG_MAXX, DWG_MAXY, RAS_WIDTH, RAS_HEIGHT, SCALE_X, SCALE_Y = 0, 0, 0, 0, 0, 0, 0, 0


def get_dir(png, dirs, output_dir):
    for i in dirs:
        for j in i:
            if j in png.split("\\"):return output_dir + "\\" + j
        break


def set_extents_values(filename):
    global DWG_MINX, DWG_MINY, DWG_MAXX, DWG_MAXY, RAS_WIDTH, RAS_HEIGHT, SCALE_X, SCALE_Y
    locx = ""
    with open(filename, 'r') as f:
        for i in f:
            locx = locx + str(i)
            if locx.find('Scale_Y') != -1:
                locx = locx[0:locx.rindex(',')] + "}]}"
                break
        y = json.loads(str(locx))
        for i in y['Views']:
            DWG_MINX = float(i['DWG_Min_Point']["x"])
            DWG_MINY = float(i['DWG_Min_Point']["y"])

            DWG_MAXX = float(i['DWG_Max_Point']["x"])
            DWG_MAXY = float(i['DWG_Max_Point']["y"])

            RAS_WIDTH = float(i["Raster_Width"])
            RAS_HEIGHT = float(i["Raster_Height"])

            SCALE_X = float(i["Scale_X"])
            SCALE_Y = float(i["Scale_Y"])

    print("DWG MIN X", DWG_MINX, type(DWG_MINX))
    print("DWG MIN Y", DWG_MINY)
    print("DWG MAX X", DWG_MAXX)
    print("DWG MAX Y", DWG_MAXY)
    print("RASTER WIDTH", RAS_WIDTH)
    print("RASTER HEIGHT", RAS_HEIGHT)
    print("SCALE X", SCALE_X)
    print("SCALE Y", SCALE_Y)


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
            # image = cv2.rectangle(image, (i[0], i[1]), (i[2], i[3]), color, thickness)
            image = cv2.rectangle(image, tuple([i[0], i[1]]), tuple([i[2], i[3]]), color, thickness)

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


def PolyLine(data, csv_fo):
    writer = csv.writer(csv_fo)
    writer.writerow(["Polyline", "X", "Y"])
    final_list = []
    if data['Drawing'].get('Blocks') is not None:
        for i in data['Drawing']['Blocks']:
            for j in i["Entities"]:
                if j['Type'] == "Polyline":
                    alist = []
                    for k in j['Vertices']:
                        DWG_X = float(k["Location"]["x"])
                        DWG_Y = float(k["Location"]["y"])

                        X = int((DWG_X - DWG_MINX) * SCALE_X)
                        Y = int(RAS_HEIGHT - (DWG_Y - DWG_MINY) * SCALE_Y)

                        writer.writerow([k["Index"], X, Y])
                        alist.append([X, Y])
                    final_list.append(alist)
    return final_list


def Line(data, csv_fo):
    writer = csv.writer(csv_fo)
    writer.writerow(["Line", "xmin", "ymin", "xmax", "ymax"])
    min_list = []
    max_list = []
    if data['Drawing'].get('Blocks') is not None:
        for i in data['Drawing']['Blocks']:
            # print(i['Entities'])
            for j in i['Entities']:
                if j['Type'] == "Line":
                    minx = float(j['Start_Point']["x"])
                    miny = float(j['Start_Point']["y"])
                    maxx = float(j['End_Point']["x"])
                    maxy = float(j['End_Point']["y"])

                    x = int((minx - DWG_MINX) * SCALE_X)
                    y = int(RAS_HEIGHT - (miny - DWG_MINY) * SCALE_Y)
                    X = int((maxx - DWG_MINX) * SCALE_X)
                    Y = int(RAS_HEIGHT - (maxy - DWG_MINY) * SCALE_Y)

                    writer.writerow(["LINE", x, y, X, Y])
                    min_list.append([x, y])
                    max_list.append([X, Y])
    return min_list, max_list


def Rect_Text(data, csv_fo):
    writer = csv.writer(csv_fo)
    writer.writerow(["xmin", "ymin", "xmax", "ymax", "Text"])
    rect_list = []
    if data['Drawing'].get('Blocks'):
        for i in data['Drawing']['Blocks']:
            for j in i['Entities']:
                if j['Type'] == "MText":
                    text = j['Text_String']
                    minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                    miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                    maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                    maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                    Rect_x = int((minx - DWG_MINX) * SCALE_X)
                    Rect_y = int(RAS_HEIGHT - (miny - DWG_MINY) * SCALE_Y)
                    Rect_X = int((maxx - DWG_MINX) * SCALE_X)
                    Rect_Y = int(RAS_HEIGHT - (maxy - DWG_MINY) * SCALE_Y)

                    writer.writerow([Rect_x, Rect_y, Rect_X, Rect_Y, text])
                    rect_list.append([Rect_x, Rect_y, Rect_X, Rect_Y, text])
    return rect_list
