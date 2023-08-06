#!/usr/bin/env python
# This uses a HYPOTHETICAL API wrapper!!!
# 
# EXAMPLES:
#   PYTHONPATH=. helpers/contrib/exposure_map.py --help
#   PYTHONPATH=. helpers/contrib/exposure_map.py -v --apiurl "http://marsnat1.pat.dm.noao.edu:8000/"

# Python library
import sys
import argparse
import copy
from pprint import pprint as pp  # pretty print
import pandas as pd
import math
import json
import warnings
# External packages
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import requests
import healpy as hp
# Local Packages
import helpers.api

##############################################################################
# functions to order the vertices of HDU corners in counter-clockwise
# direction, so that their polygon is convex
#
# reference:
# https://algorithmtutor.com/Computational-Geometry/Area-of-a-polygon-given-a-set-of-points/

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return '(' + str(self.x) + ', ' + str(self.y) + ')'
    
def distance(p1, p2):
    d = np.sqrt((p2.x - p1.x)**2 + (p2.y - p1.y)**2)
    return d
    
def average_point_inside(points):
    x = 0
    y = 0
    for point in points:
        x += point.x
        y += point.y
    return Point(x / len(points), y / len(points))

def angle(p1, p2):
    k = (p2.y - p1.y) / distance(p1, p2)

    x2 = p2.x
    x1 = p1.x

    if k >= 0:
        if x2 >= x1: # First Quadrant
            return (2.0 * math.pi - math.asin(k))
        else: # Second Quadrant
            return (math.pi + math.asin(k))
    else:
        if x2 >= x1: # Fourth Quadrant
            return math.asin(-k)
        else: # Third Quadrant
            return (math.pi - math.asin(-k))
        
def sort_angular(points, reference_point):
    return sorted(points, key = lambda point: -angle(point, reference_point))

def sort_radec(ra,dec):
    points = [Point(ra[0],dec[0]), Point(ra[1],dec[1]), Point(ra[2],dec[2]), Point(ra[3],dec[3])]
    reference_point = average_point_inside(points)
    spoints =  sort_angular(points, reference_point)
    ra1s=[]
    dec1s=[]
    for p in spoints:
        ra1s.append(p.x)
        dec1s.append(p.y)
    return np.array(ra1s),np.array(dec1s)


##############################################################################

def gen_exposure_map(api, verbose=False):
    if verbose:
        print('Get AIRMASS and G-TRANSP for DECam files with selected filter.')

    jj = {
        "outfields" : [
            # Files
            "md5sum",
            "archive_filename",
            "exposure",
            "ifilter",
            "AIRMASS",
            "G-TRANSP",
            # HDUs
            "hdu:ra_min",
            "hdu:ra_max",
            "hdu:dec_min",
            "hdu:dec_max",
            "hdu:FWHM",
            "hdu:AVSKY", 
        ],
        "search" : [
            ["hdu:ra_center", -400, 400], # eliminate recs without ra/dec
            ["caldat", "2018-09-01", "2020-12-31"] ,
            ["instrument", "decam"],
            ["proc_type", "instcal"],
            ["prod_type", "image"],
            ["obs_type", "object"],
            ["proposal", "2012B-0001"],
            ["ifilter", "r DECam", "contains"]
        ]}
    
    info, rows = api.find(jj, record_type='hdu', limit=None)
    
    dfm = pd.DataFrame(rows)
    if verbose:
        print(f"Found {info['RESULTS']['COUNT']} HDUs")
    dfmc = dfm.dropna()

    apix = 0.263 # arcsec/pixel
    sky = dfmc['AVSKY']/dfmc['exposure'] # sky rate
    tau = dfmc['G-TRANSP']**2/(dfmc['FWHM']*apix/0.9)**2/(sky/3.)

    if verbose:
        print(f"Plot tau histogram")
    a = plt.hist(tau,bins=200,range=(0,1))
    plt.xlabel('tau')

    tau_trim = np.clip(tau,0,1) # tau should be between 0 and 1

    ########################
    # Making the depth map
    #
    # NOTE: Some of the complexity of the following could be reduced by using
    # the bounding box of HDU instead of corners. Not as accurate but bbox is
    # ordered. Use ra_min, ra_max, dec_min, dec_max
    #
    # Now that we have the needed quantities, we can begin to make our
    # depth map. Our procedure will be to create a Healpix map, use
    # the coordinates of the HDU corners to identify which healpixels
    # are spanned by each HDU, and add the value of 𝜏
    # 
    # for those HDUs to the appropriate Healpixels. A couple of notes:
    # 
    #     Because the corners of the HDUs aren't guaranteed to go
    #     clockwise, or counter-clockwise, around the HDU, we might
    #     not be defining convex polygons when we do the healpixel
    #     mapping. We'll need to order the corners so that they go in
    #     one direction, and don't jump an HDU along its diagonal
    #
    #     We'll need to loop over all of the HDUs one at a time, which
    #     can be slow. Parallel processing might help here.
    
    # Pull out the HDU corners
    #! ratab = [np.array([row[0],row[1],row[2],row[3]])
    #!   for row in dfmc[['COR1RA1','COR2RA1','COR3RA1','COR4RA1']].values]
    #! dectab = [np.array([row[0],row[1],row[2],row[3]])
    #!   for row in dfmc[['COR1DEC1','COR2DEC1','COR3DEC1','COR4DEC1']].values]
    #! radectab_s = [sort_radec(ra1,dec1) for ra1,dec1 in zip(ratab,dectab)]

    radectab_s = [np.array([row['ra'].lower,
                            row['ra'].upper,
                            row['ra'].upper,
                            row['ra'].lower]),
                  np.array([row['dec'].upper
                            row['dec'].upper
                            row['dec'].lower
                            row['dec'].lower])]
    # Knute NOTE: above uses bounding box.
    # Creates point order that is clockwise from upper left (low RA, high DEC).
                            
    vectab = [hp.ang2vec(ra1,dec1,lonlat=True) for ra1, dec1 in radectab_s]    

    # Define the Healpix map
    nside = 4096
    if verbose:
        print(f'Resolution is {hp.nside2resol(nside,arcmin=True):5.2f} arcmin.')
    map = np.zeros(hp.nside2npix(nside)) # raw exposure map
    tmap = map.copy() # teff map

    # Loop over HDUs (slow!)
    for vec,exptime,tau1 in zip(vectab,dfmc['fitsfile__exposure'],tau_trim):
        try:
            ipix = hp.query_polygon(nside,vec)
            map[ipix] += exptime
            tmap[ipix] += tau1 * exptime
        except:
            pass

    # Show the map
    if verbose:
        print(f"Show exposure map in Orthographic view")
    cmap = copy.copy(matplotlib.cm.get_cmap("inferno"))
    fig = plt.figure(figsize=(15,15))
    hp.orthview(tmap,rot=(20,-30),fig=1,cmap=cmap,half_sky=True,min=0,max=1000)

    # Zooming in
    if verbose:
        print(f"Show exposure map in Gnomonic view")
    hp.gnomview(tmap,reso=0.75,cmap=cmap,rot=(8,-44),min=0,max=1000)
    
    return tmap 


##############################################################################


def main():
    parser = argparse.ArgumentParser(
        #version='1.0.0',
        description='Generate exposure map for a survey (from: Knut Olsen)',
        epilog='EXAMPLE: "%(prog)s -v"'
        )
    parser.add_argument('--save',
                        help=('Name of file in which to save exposure map'
                              ' (numpy array)'))
    parser.add_argument('--apiurl',  help='URL of Archive API service',
                        default='https://astroarchive.noao.edu/')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help=('Tell what is going on.'))
    parser.add_argument('--no_plot', action='store_true',
                        help=('Suppress display of plots.'))

    args = parser.parse_args()

    fapi =  helpers.api.FitsFile(args.apiurl)
    hapi =  helpers.api.FitsHdu(args.apiurl)

    warnings.filterwarnings('ignore') # suppress ALL warnings (dangerous)

    if args.verbose:
        print(f'Using API server at {args.apiurl}')
        
    map = gen_exposure_map(fapi,hapi, verbose=args.verbose)
    
    if args.verbose:
        print(f'Non-zeros: {np.count_nonzero(map):,} of {np.size(map):,}')
    if args.save:
        np.save(args.save, map)
        print(f'Wrote exposure map (numpy array) to {args.save}')

    if not args.no_plot:
        plt.show()

if __name__ == '__main__':
    main()
