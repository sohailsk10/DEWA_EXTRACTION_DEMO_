from PIL import Image, ImageDraw
import re
import xml.etree.ElementTree as ET
import csv
import os


xml_input = "C:\pdftron\PDFNetPython3\Samples\TestFiles\DEWA_DEMO_SAALEM\LV\pdftron_xml\E2030199-APPROVED-Done_page_25_5000dpi.xml"

path = r'C:\pdftron\PDFNetPython3\Samples\TestFiles\E2030199-APPROVED-Done_page_25_5000dpi.png'

image_name = 'E2030199_APPROVED_Done_page_25_5000dpi.png'

orig_image = Image.open(path)

width, height = orig_image.size
print('width, height ====', width, height)

tree = ET.parse(xml_input)

root = tree.getroot()

# print(root)
if not os.path.exists("csv"):
    os.makedirs("csv")

csv_filename = "csv\\" + image_name.split('.')[0] + ".csv"
print(csv_filename)

with open(csv_filename, "w+") as file:
    writer = csv.writer(file)
    txt_heading = ["Sr No.", "Shape", "Vertices", "x_min", "y_min", "x_max", "y_max","Value", "Attribute = TEXT"]
    writer.writerow(txt_heading)
    count = 1
    for para in root.findall("./Flow/Para"):
        # print('=====', para.attrib)
        for line in para.findall("./Line"):
            # print('00000', line.text)
            # print('00000', line.attrib)
            cord_dict = line.attrib.values()
            # print(cord_dict)
            cord_list = re.findall('\'([^)]+)\'', str(cord_dict))
            # print('9999999', cord_list)
            cord = str(cord_list).split(',')
            # print('striped  ', cord)

            x = cord[0].strip(" ['")
            y = cord[1].strip()
            length = cord[2].strip()
            fnt_size = cord[3].strip(" ]'")
            # print('5555555', x)
            # print('5555555', y)
            # print('5555555', length)
            # print('5555555', fnt_size)

            # tx_min = 2756             # Roof
            # ty_min = 2928.32
            # length = 224.051
            # fnt_size = 39.5625

            # tx_min = 2747             # first
            # ty_min = 2564.84
            # length = 233.051
            # fnt_size = 42.4063

            # tx_min = 494             # (GUEST VILLA)
            # ty_min = 2429.92
            # length = 146.002
            # fnt_size = 24.1563

            # 494, 2429.92, 146.002, 24.1563

            x_min = float(x) - 1
            # print('x_min =======', x_min)

            y_min = height - float(y) - float(fnt_size) - 1
            # print('y_min ======', y_min)

            x_max = float(x_min) + float(length) + 1
            # print('x_max =======', x_max)

            y_max = float(y_min) + float(fnt_size) + 1
            # print('y_max ======', y_max)

            rect_points = [abs(x_min), abs(y_min), abs(x_max), abs(y_max)]

            # Plot rectangle on image ==========

            fnl_img = ImageDraw.Draw(orig_image)
            fnl_img.rectangle(rect_points, outline="red", width=1)


            # Make csv ==========
            Count = count
            shape = "Rectangle"
            vertices = len(rect_points)
            x_min = int(rect_points[0])
            y_min = int(rect_points[1])
            x_max = int(rect_points[2])
            y_max = int(rect_points[3])
            value = str(line.text.strip())
            print(value)
            count += 1

            boxes = Count, shape, vertices, x_min, y_min, x_max, y_max, value
            writer.writerow(boxes)
    print("Text Done....................")




fnl_name = 'out_poly.png'
orig_image.save(fnl_name)
# orig_image.show()
print('Plotting Done')
