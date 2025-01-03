def get_bounding_square(lat,lon):
    d_max = 3
    top_lat = lat + d_max 
    btm_lat = lat - d_max
    right_lon = lon + d_max 
    left_lon = lon - d_max
    return top_lat,btm_lat,right_lon,left_lon
