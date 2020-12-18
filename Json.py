import json
import copy
from Shape_Draw import *


image_name = "E2030199-APPROVED-Done_page_25_updated.png"
image = cv2.imread(image_name)
json_read = r'LinkList_2020_W32_20_02_06\E2030199-APPROVED-Done_page_25.json'


with open(json_read, "r") as f:
    json_data = json.load(f)
    print("Reading Json file....")


def area(x1, y1, x2, y2, x3, y3):
    return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)


def check(x1, y1, x2, y2, x3, y3, x4, y4, x, y):
    A = (area(x1, y1, x2, y2, x3, y3) + area(x1, y1, x4, y4, x3, y3))
    A1 = area(x, y, x1, y1, x2, y2)
    A2 = area(x, y, x2, y2, x3, y3)
    A3 = area(x, y, x3, y3, x4, y4)
    A4 = area(x, y, x1, y1, x4, y4)
    return (A == A1 + A2 + A3 + A4)


def discard_upolyline(polylist, data):
    dd = {}
    for rect in data:
        # print('rect ====', rect)
        a1 = int(rect[0])
        a2 = int(rect[1])
        a3 = int(rect[2])
        a4 = int(rect[3])
        for i in range(len(polylist)):
            ilist = []
            for j in polylist[i]:
                if (check(a1, a2, a3, a2, a3, a4, a1, a4, int(j[0]), int(j[1]))):
                    ilist.append(j)
            if len(ilist) != 0:
                dd[i] = ilist
    return dd



polylist = PolyLine(json_data)
min_list, max_list = Line(json_data)
rect_list = Rect_Text(json_data)

print("Discarding Unwanted PolyList...")
ddict = discard_upolyline(polylist, rect_list)


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

mod_image = draw_in_image("MText", rect_list, image)
mod_image = draw_in_image("polyline", final_deleting_list, mod_image)
mod_image = draw_in_image("line", [min_list, max_list], mod_image)

cv2.imwrite(image_name.split('.')[0] + '_Output.jpg', mod_image)
