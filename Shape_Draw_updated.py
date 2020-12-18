import cv2
import numpy as np
import csv

"""SLD"""
DWG_Min_Point_X = 0.22
DWG_Min_Point_Y = 0.518333
DWG_Max_Point_X = 10.7783
DWG_Max_Point_Y = 7.98333
Raster_Width = 6500
Raster_Height = 4596
Scale_X = 615.627
Scale_Y = 615.673


def draw_in_image(type, type_array, image):
    if type == "polyline":
        for Poly_list in type_array:
            # print(Poly_list)
            # sys.exit()
            pts = np.array(Poly_list, np.int32)
            isClosed = False
            color = (0, 0, 255)
            thickness = 2
            image = cv2.polylines(image, [pts], isClosed, color, thickness)

    if type == "line":
        min_list = type_array[0]
        max_list = type_array[1]
        # print('line======', min_list, max_list)
        color = (0, 255, 0)
        thickness = 2
        for i in range(len(min_list)):
            image = cv2.line(image, tuple(min_list[i]), tuple(max_list[i]), color, thickness)

    if type == "MText":
        min_rect_list = type_array[0]
        max_rect_list = type_array[1]
        color = (0, 255, 0)
        thickness = 3
        for i in range(len(min_rect_list)):
            image = cv2.rectangle(image, tuple(min_rect_list[i]), tuple(max_rect_list[i]), color, thickness)

    return image



def PolyLine(data):
    # with open("sld_25_output_new.csv", "w") as coords_csv_file:
    #     writer = csv.writer(coords_csv_file)
    #     writer.writerow(["Polyline", "X", "Y"])
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

                    # writer.writerow([k["Index"], X, Y])
                    alist.append([X, Y])
                final_list.append(alist)
    return final_list
    
    
def Line(data):
    with open("sld_26_output_new.csv", "a") as coords_csv_file:
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
    final_list = []
    for i in data['Drawing']['Blocks']:
            for j in i['Entities']:
                temp_list = []
                if j['Type'] == "MText":

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
    return final_list

def Rect_Text(data):
    # with open("SLD.csv", "a") as coords_csv_file:
    #     writer = csv.writer(coords_csv_file)
    #     writer.writerow(["Line", "xmin", "ymin", "xmax", "ymax"])
    min_rect_list = []
    max_rect_list = []
    for i in data['Drawing']['Blocks']:
        # print(i['Entities'])
        for j in i['Entities']:
            if j['Type'] == "MText":
                print(j)
                minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                x = int((minx - DWG_Min_Point_X) * Scale_X)
                y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                X = int((maxx - DWG_Min_Point_X) * Scale_X)
                Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)
                print(x, y, X, Y)

                min_rect_list.append([x, y])
                max_rect_list.append([X, Y])
    return min_rect_list, max_rect_list
