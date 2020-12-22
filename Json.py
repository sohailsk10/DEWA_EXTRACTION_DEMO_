import os, sys
import json
import copy
from Shape_Draw import *
from io import StringIO
from prettytable import PrettyTable

# image_name = "TED_Form_Standard_5000.png"
# image = cv2.imread(image_name)
# json_read = r'TED_Tailormade\TED_Form_Standard_5000.json'


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


json_lst = []
png_lst = []
ext_list = []
dirs = []

INPUT_DIR = "HOUSE_IRRIGATION"

for path, dir1, files in os.walk(INPUT_DIR):
    if dir1:
        dirs.append(dir1)
    for file in files:
        if file.endswith(".json"):
            json_lst.append(os.path.join(path, file))
        elif file.endswith(".png"):
            png_lst.append(os.path.join(path, file))
        elif file.endswith(".extents"):
            ext_list.append(os.path.join(path, file))


OUTPUT_DIR = "OUTPUT_" + INPUT_DIR
if not os.path.exists(OUTPUT_DIR):
    for i in dirs:
        for j in i:
            os.makedirs(os.path.join(OUTPUT_DIR, j))
            save_dir = os.path.join(OUTPUT_DIR, j)
        break

if len(json_lst) == len(png_lst) == len(ext_list):
    for i in range(len(json_lst)):
        image_name = png_lst[i]
        image = cv2.imread(image_name)

        tbl = PrettyTable()
        tbl.field_names = ["PNG", "JSON", "EXTENTS"]
        if len(json_lst) == len(png_lst):
            for i in range(len(json_lst)):
                tbl.add_row([png_lst[i], json_lst[i], ext_list[i]])
        tbl.align = "l"
        print(tbl)
        break

        # print(tbl.align("l"))
        # sys.exit()

        # output_csv = image_name.split("\\")[-1].split(".")[0] + ".csv"

if len(json_lst) == len(png_lst) == len(ext_list):
    for i in range(len(json_lst)):

        filename = png_lst[i].split("\\")[-1].split(".")[0]
        wrk_dir = get_dir(png_lst[i], dirs, OUTPUT_DIR)
        csvfilename = wrk_dir + "\\" + filename + ".csv"

        imagefilename = wrk_dir + "\\" + filename + "_output.png"
        print(csvfilename)
        print(imagefilename)

        set_extents_values(ext_list[i])
        image = cv2.imread(png_lst[i])

        with open(json_lst[i], "r") as f:
            # io = StringIO(f)
            json_data = json.load(f)
            # print(json_data)
            # ensure_ascii = False
            # print("Reading Json file....")

        csvfo = open(csvfilename, "w")

        rect_list = Rect_Text(json_data, csvfo)
        polylist = PolyLine(json_data, csvfo)
        min_list, max_list = Line(json_data, csvfo)

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

        cv2.imwrite(imagefilename, mod_image)
        print("output files is written in the output folder")
        print()
