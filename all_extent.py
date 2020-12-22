import json



def get_extents_values(filename):
    locx = ""
    DWG_MINX, DWG_MINY, DWG_MAXX, DWG_MAXY, RAS_WIDTH, RAS_HEIGHT, SCALE_X, SCALE_Y = 0, 0, 0, 0, 0, 0, 0, 0
    with open(filename, 'r') as f:
        for i in f:
            locx = locx + str(i)
            if (locx.find('Scale_Y') != -1):
                locx = locx[0:locx.rindex(',')] + "}]}"
                break
        y = json.loads(str(locx))
        for i in y['Views']:
            DWG_MINX = i['DWG_Min_Point']["x"]
            DWG_MINY = i['DWG_Min_Point']["y"]

            DWG_MAXX = i['DWG_Max_Point']["x"]
            DWG_MAXY = i['DWG_Max_Point']["y"]

            RAS_WIDTH = i["Raster_Width"]
            RAS_HEIGHT = i["Raster_Height"]

            SCALE_X = i["Scale_X"]
            SCALE_Y = i["Scale_Y"]

    return DWG_MINX, DWG_MINY, DWG_MAXX, DWG_MAXY, RAS_WIDTH, RAS_HEIGHT, SCALE_X, SCALE_Y

print(get_extents_values('sld_25_cropped-converted.extents'))