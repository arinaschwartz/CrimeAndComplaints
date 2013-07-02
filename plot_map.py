# Highly influenced by http://hci574.blogspot.com/2010/04/using-google-maps-static-images.html
# Taps into the google static map api
# http://code.google.com/apis/maps/documentation/staticmaps/#Locations


import urllib
from pylab import imshow, imread

__all__ = ('plot_google_static_map')

def get_google_static_map(lat, lng, zoom=18, imgsize=(640,640), imgformat="png",
        maptype="roadmap"):

    request =  "http://maps.google.com/maps/api/staticmap?" # base URL, append query params, separated by &

    request += "center=%f,%f&" % (lat, lng)
    request += "zoom=%i&" % zoom  # zoom 0 (all of the world scale ) to 22 (single buildings scale)

    request += "size=%ix%i&" % (imgsize)  # tuple of ints, up to 640 by 640
    request += "format=%s&" % imgformat
    request += "maptype=%s&" % maptype  # roadmap, satellite, hybrid, terrain
    request += "sensor=false&"   # must be given, deals with getting loction from mobile device
    urllib.urlretrieve(request, "temp."+imgformat) # Option 1: save image directly to disk


# coordinates around woodlawn and 55th
center = (41.7951,-87.5965)
default_zoom = 15
ul = (41.8054,-87.61)
lr = (41.7852, -87.5825)
diffs = (.01, .014) # approximately - although these are quite close
lat_per_pixel = diffs[0] / 640
long_per_pixel = diffs[1] / 640


def extent(clat, clong, xpixels, ypixels, zoom=15):
    lat_diff = lat_per_pixel * ypixels / (2**(zoom-default_zoom))
    long_diff = long_per_pixel * xpixels / (2**(zoom-default_zoom))
    return (clong-long_diff, clong+long_diff, clat-lat_diff, clat+lat_diff)

def plot_google_static_map(lat, lng, imgsize=(640,640), zoom=15,**kwargs):
    """
    Plots a static google map using matplotlib at the coordinates specified
    Inputs:
        lat - Latitude of central point
        lon - Longitude of central point
        imgsize - Number of pixels in x and y directions, tuple
        maptype - Your choice of 'roadmap', 'terrain', 'satellite', 'hybrid'
        zoom - Google maps zoom level, 15 default

    >>> plot_google_static_map(41.7961,-87.5965)

    """
    get_google_static_map(lat, lng, zoom=zoom, imgsize=imgsize, imgformat="png",
            **kwargs)
    im = imread('temp.png')
    imshow(im, extent=extent(lat,lng,imgsize[0],imgsize[1]))


