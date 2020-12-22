import json
import csv
import cv2
import math

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

OUTPUT_CSV = "Shape_extract_new.csv"

Arc_Circle_Csv = 'Arc_Circle.csv'


def Arc():
    with open(Arc_Circle_Csv, "w") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Arc", "xmin", "ymin", "xmax", "ymax"])
        final_list = []
        for i in json_data['Drawing']['Blocks']:
            for j in i["Entities"]:
                if j.get("Feature_Type"):
                    if j['Feature_Type']['Type'] == "Arc":
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

                            cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 255, 255), 2)
                            final_list.append([Rect_x, Rect_y, Rect_X, Rect_Y])


# Arc()


def Circle():
    with open(Arc_Circle_Csv, "a") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Circle", "xmin", "ymin", "xmax", "ymax"])
        final_list = []
        for i in json_data['Drawing']['Blocks']:
            for j in i["Entities"]:
                if j.get("Feature_Type"):
                    if j['Feature_Type']['Type'] == "Circle":
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

                            cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (0, 0, 255), 2)
                            final_list.append([Rect_x, Rect_y, Rect_X, Rect_Y])


# Circle()


def Rectangle():
    with open(OUTPUT_CSV, "w") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Rectangle", "xmin", "ymin", "xmax", "ymax"])
        final_list = []
        for i in json_data['Drawing']['Blocks']:
            for j in i["Entities"]:
                if j.get("Feature_Type"):
                    if j['Feature_Type']['Type'] == "Rectangle":
                        for k in j['Entity_Extents']:
                            minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                            miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                            maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                            maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                            Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
                            Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                            Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
                            Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                            writer.writerow(["Rectangle", Rect_x, Rect_y, Rect_X, Rect_Y])

                            cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (255, 0, 0), 8)
                            final_list.append([Rect_x, Rect_y, Rect_X, Rect_Y])


Rectangle()


def Triangle():
    with open(OUTPUT_CSV, "a") as coords_csv_file:
        writer = csv.writer(coords_csv_file)
        writer.writerow(["Triangle", "xmin", "ymin", "xmax", "ymax"])
        final_list = []
        for i in json_data['Drawing']['Blocks']:
            for j in i["Entities"]:
                if j.get("Feature_Type"):
                    if j['Feature_Type']['Type'] == "Triangle":
                        for k in j['Entity_Extents']:
                            minx = float(j['Entity_Extents']['Minimum_Point']["x"])
                            miny = float(j['Entity_Extents']['Minimum_Point']["y"])
                            maxx = float(j['Entity_Extents']['Maximum_Point']["x"])
                            maxy = float(j['Entity_Extents']['Maximum_Point']["y"])

                            Rect_x = int((minx - DWG_Min_Point_X) * Scale_X)
                            Rect_y = int(Raster_Height - (miny - DWG_Min_Point_Y) * Scale_Y)
                            Rect_X = int((maxx - DWG_Min_Point_X) * Scale_X)
                            Rect_Y = int(Raster_Height - (maxy - DWG_Min_Point_Y) * Scale_Y)

                            writer.writerow(["Triangle", Rect_x, Rect_y, Rect_X, Rect_Y])

                            cv2.rectangle(image, tuple((Rect_x, Rect_y)), tuple((Rect_X, Rect_Y)), (255, 0, 102), 2)
                            final_list.append([Rect_x, Rect_y, Rect_X, Rect_Y])


# Triangle()

# coordinates = []
# text_id = []
# centroids = []
# id_ = 0
# csv_1 = Arc_Circle_Csv
#
#
# def get_values(csv_name):
#     global id_
#     arc_list = []
#     circle_list = []
#     with open(csv_name, 'r') as file:
#         reader = csv.reader(file)
#         for num, row in enumerate(reader):
#             if num % 2 == 0:
#                 if row[0] == 'Arc' and row[1] != 'xmin':
#                     if [int(row[1]), int(row[2]), int(row[3]), int(row[4])] not in arc_list:
#                         arc_list.append([int(row[1]), int(row[2]), int(row[3]), int(row[4])])
#
#                 elif row[0] == 'Circle' and row[1] != 'xmin':
#                     if [int(row[1]), int(row[2]), int(row[3]), int(row[4])] not in circle_list:
#                         circle_list.append([int(row[1]), int(row[2]), int(row[3]), int(row[4])])
#
#     return arc_list, circle_list
#
#
# def draw(image, list):
#     centroids = []
#     coordinates = []
#     for i in list:
#         xmin = i[0]
#         ymin = i[1]
#         xmax = i[2]
#         ymax = i[3]
#         # cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (0, 0, 255), 2)
#
#         x1_midpoint = ((xmin + xmax) // 2, (ymin + ymin) // 2)
#         x2_midpoint = ((xmin + xmax) // 2, (ymax + ymax) // 2)
#         y1_midpoint = ((xmin + xmin) // 2, (ymin + ymax) // 2)
#         y2_midpoint = ((xmax + xmax) // 2, (ymin + ymax) // 2)
#
#         # image = cv2.circle(image, x1_midpoint, 1, (0, 255, 0), 2)
#         # image = cv2.circle(image, x2_midpoint, 1, (0, 255, 0), 2)
#         # image = cv2.circle(image, y1_midpoint, 1, (0, 255, 0), 2)
#         # image = cv2.circle(image, y2_midpoint, 1, (0, 255, 0), 2)
#
#         center_coord = int((xmin + xmax) / 2), int((ymin + ymax) / 2)
#         # image = cv2.circle(image, center_coord, 1, (255, 0, 0), 2)
#
#         centroids.append(center_coord)
#         coordinates.append([xmin, ymin, xmax, ymax])
#
#     return image, centroids, coordinates
#
#
# arc_l, circle_l = get_values(csv_1)
#
# image, arc_cent, arc_coords = draw(image, arc_l)
# image, circle_cent, circle_coords = draw(image, circle_l)
# cv2.imwrite("sld_25_output_1.jpg", image)
#
# '''
# --------------------------------------------------------------------
# findind the euclidean distance from the centroids we calculated
#                         and
# drawing the lines between the boxes who has least euclidean distance
# --------------------------------------------------------------------
# '''
#
#
# def Sort_Tuple(tup):
#     # reverse = None (Sorts in Ascending order)
#     # key is set to sort using second element of
#     # sublist lambda has been used
#     tup.sort(key=lambda x: x[0])
#     return tup
#
#
# final_pts = []
# for i in circle_cent:
#     x1 = i[0]
#     y1 = i[1]
#     matrix = []
#     temp_pts = []
#
#     for num, j in enumerate(arc_cent):
#         x2 = j[0]
#         y2 = j[1]
#
#         e_dist = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
#         matrix.append((int(e_dist), (x1, y1), (x2, y2)))
#
#     l = Sort_Tuple(matrix)
#     if l[0][0] <= 40:
#         pt1 = l[0][1]
#         pt2 = l[0][2]
#         # print(pt1, pt2)
#         # cv2.line(image, pt1, pt2, (255, 0, 0), thickness=3, lineType=3)
#         final_pts.append([pt1, pt2])
#         # for i in temp_pts:
#         #     if i[1] == pt2:
#         #         final_pts.append([i, pt1])
#
#     matrix.clear()
#
# final = []
# with open(OUTPUT_CSV, "a") as coords_csv_file:
#     writer = csv.writer(coords_csv_file)
#     writer.writerow(["Trial_Pole", "xmin", "ymin", "xmax", "ymax"])
#     for num, i in enumerate(final_pts):
#         for j in final_pts:
#             if i == j:
#                 pass
#             else:
#                 if j[1] == i[1]:
#                     cir = (circle_coords[(circle_cent.index(i[0]))])
#                     arc = (arc_coords[(arc_cent.index(i[1]))])
#                     cir1 = (circle_coords[(circle_cent.index(j[0]))])
#                     xmin = (min([cir[0], arc[0], cir1[0]]))
#                     ymax = (max([cir[1], arc[1], cir1[1]]))
#                     xmax = (max([cir[2], arc[2], cir1[2]]))
#                     ymin = (min([cir[3], arc[3], cir1[3]]))
#                     # print(min([(circle_coords[(circle_cent.index(i[0]))][1]), arc_coords[(arc_cent.index(i[1]))][1], circle_coords[(circle_cent.index(j[0]))][1]]))
#                     # print(max([(circle_coords[(circle_cent.index(i[0]))][2]), arc_coords[(arc_cent.index(i[1]))][2], circle_coords[(circle_cent.index(j[0]))][2]]))
#                     # print(max([(circle_coords[(circle_cent.index(i[0]))][3]), arc_coords[(arc_cent.index(i[1]))][3], circle_coords[(circle_cent.index(j[0]))][3]]))
#                     writer.writerow(["Trial_Pole", xmin, xmax, ymin, ymax])
#                     cv2.rectangle(image, (xmin, ymin), (xmax, ymax), (25, 45, 140), 3)
#         final_pts.pop(num)

cv2.imwrite("TrialTrench_Sample2_6500_pink_Box.jpg", image)
