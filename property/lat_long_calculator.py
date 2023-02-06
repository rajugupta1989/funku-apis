import math


class Object(object):
    pass

def get_lat_long_calculated(lat,long,distance):
    noe_obj = Object()
    lat = float(lat)
    long = float(long)
    distance = int(distance)
    print('lat',lat)
    print('long',long)
    print('distance',distance)

    R = 6378.1  # earth radius
    # distance = 10  # distance in km 
    

    noe_obj.lat1 = lat - math.degrees(distance/R)
    noe_obj.lat2 = lat + math.degrees(distance/R)
    noe_obj.long1 = long - math.degrees(distance/R/math.cos(math.degrees(lat)))
    noe_obj.long2 = long + math.degrees(distance/R/math.cos(math.degrees(lat)))

    return noe_obj
