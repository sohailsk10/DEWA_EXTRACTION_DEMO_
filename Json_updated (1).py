import json
import copy
from Shape_Draw_updated import *
import os

image_name = r'NOC_TailorMade_Updated\NOC_Sample21_3500.png'
image = cv2.imread(image_name)
json_data = None
csv_data = []
final_deleting_list = []
csv_read = r"NOC_TED_compare\csv\NOC_Sample21_3500.csv"
json_read = r"E2030199_24.json"
Output_csv = r"Output_CSV\E2030199_APPROVED_Done_page_24.csv"


def Functn1(topLeft=(0,0), bottomRight=(0,0), pointList=[]):

    x = topLeft[0]      #Rectangle x
    y = topLeft[1]      #Rectangle y
    w = bottomRight[0]  #Rectangle width(which 5ou created with name of x2)
    h = bottomRight[1]  #Rectangle height(which you created with name of y2)

    for i in range(len(pointList)):
        p_x = pointList[i][0]  #Current point x
        p_y = pointList[i][1]  #Current point y

        if not ((p_x >= x and p_x < w) and (p_y >= y and p_y < h)): #Return False if the point wasn't in the rectangle (because you said theyre all must be inside the rectangle)
            return False

    return True  #If non of them was outside the rectangle (Or it wasn't returned False) so return True

def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) +
                x2 * (y3 - y1) +
                x3 * (y1 - y2)) / 2.0)


# A function to check whether point
# P(x, y) lies inside the rectangle
# formed by A(x1, y1), B(x2, y2),
# C(x3, y3) and D(x4, y4)
def check(x1, y1, x2, y2, x3,
          y3, x4, y4, x, y):
    # Calculate area of rectangle ABCD
    A = (area(x1, y1, x2, y2, x3, y3) +
         area(x1, y1, x4, y4, x3, y3))

    # Calculate area of triangle PAB
    A1 = area(x, y, x1, y1, x2, y2)

    # Calculate area of triangle PBC
    A2 = area(x, y, x2, y2, x3, y3)

    # Calculate area of triangle PCD
    A3 = area(x, y, x3, y3, x4, y4)

    # Calculate area of triangle PAD
    A4 = area(x, y, x1, y1, x4, y4)

    # Check if sum of A1, A2, A3
    # and A4 is same as A
    return (A == A1 + A2 + A3 + A4)


def delete_from_polylist(polylist, final_deleting_list):
    fpl = []
    for dl in final_deleting_list:
        for i in polylist:
            if dl in i:
                i.remove(dl)
        fpl.append(i)
    return fpl

def discard_upolyline(polylist, csv_data):
    dd = {}
    for rect in csv_data:
        print('rect ====', rect)
        a1 = int(rect[3])
        a2 = int(rect[4])
        a3 = int(rect[5])
        a4 = int(rect[6])

        for i in range(len(polylist)):
            ilist = []
            for j in polylist[i]:
                if (check(a1, a2, a3, a2, a3, a4,
                          a1, a4, int(j[0]), int(j[1]))):
                    ilist.append(j)
            if len(ilist) != 0:
                dd[i] = ilist
    return dd

with open(json_read, "r") as f:
    json_data = json.load(f)


with open(csv_read, "r") as csv_file:
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
ddict = discard_upolyline(polylist, csv_data)


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


if os.path.exists(Output_csv):
    print("delete")
    os.remove(Output_csv)

min_rect_list, max_rect_list = Rect_Text(json_data)
mod_image = draw_in_image("polyline", final_deleting_list, image)
mod_image = draw_in_image("MText", [min_rect_list, max_rect_list], mod_image)

coords_csv_file = open(Output_csv, "w")
writer = csv.writer(coords_csv_file)
writer.writerow(["Polyline", "X", "Y"])
for i in final_deleting_list:
    if i:
        counter = 1
        for j in i:
            writer.writerow([counter, j[0], j[1]])
            counter += 1

writer.writerow(["text_xmin", "text_ymin", "text_xmax", "text_ymax"])
for _ in range(len(min_rect_list)):
    tl = [min_rect_list[0][0], min_rect_list[0][1], max_rect_list[0][0], max_rect_list[0][1]]
    writer.writerow(tl)
    min_rect_list.remove(min_rect_list[0])
    max_rect_list.remove(max_rect_list[0])
coords_csv_file.close()


cv2.imwrite(image_name.split('.')[0] + '_Output.jpg', mod_image)
