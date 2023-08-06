import re

from geodesic.utils.memcache import cache
try:
    from osgeo import gdal
except ImportError:
    gdal = None


gs_re = re.compile(r'gs://([\w\-]{1,})\/([\/\w\.\-]{1,})', re.UNICODE)
s3_re = re.compile(r's3://([\w\-]{1,})\/([\/\w\.\-]{1,})', re.UNICODE)

class Raster:
    """
    Handles raster data, typically MSI
    """
    def __init__(self, item) -> None:
        
        self.item = item

    def export_raster(self, bbox=None, bands=['red', 'green', 'blue'], image_size=None, pixel_size=None, input_srs='EPSG:4326', output_srs='EPSG:3857'):

        band_files = []
        for band in bands:
            if band not in self.item.assets:
                assets = ','.join([k for k in self.item.assets])
                raise ValueError("band '{0}' does not exist for this item. Available assets are: {1}".format(band, assets))
            
            asset = self.item.assets[band]

            band_files.append(format_uri(asset.href))

        vrt = gdal.BuildVRT(
            '/vsimem/chip.vrt', 
            band_files, 
            options=gdal.BuildVRTOptions(
                separate=True
            )
        )
        options = gdal.WarpOptions(
            format="GTiff", 
            outputBounds=bbox,
            outputBoundsSRS=input_srs,
            xRes=30.0,
            yRes=30.0,
            dstSRS=output_srs
        )
        print('warping')
        d = gdal.Warp('/vsimem/test.tiff', vrt, options=options)

        vrt = None
        
        x = d.ReadAsArray()
        d = None

        return x
      

def format_uri(uri):
    m = gs_re.match(uri)
    
    if m:
        bucket = m.group(1)
        key = m.group(2)

        return f'/vsigs/{bucket}/{key}'

    m = s3_re.match(uri)
    
    if m:
        bucket = m.group(1)
        key = m.group(2)

        return f'/vsis3/{bucket}/{key}'

    if uri.startswith('http://') or uri.startswith('https://') or uri.startswith('ftp://'):
        return '/vsicurl/'+uri
    
    return uri

class BandCombination:
    """
    Creates a band combination
    """

'''
def band_composite(bands):
    options = gdal.BuildVRTOptions(separate=True)
    out_path = 'chip.vrt'
    return gdal.BuildVRT(out_path, bands, options=options)

def warp(out_ds, in_ds):
    options = gdal.WarpOptions(
        format="GTiff", 
        outputBounds=rect.bounds,
        outputBoundsSRS='EPSG:4326',
        xRes=10.0,
        yRes=10.0,
        dstSRS='EPSG:3857'
    )
   
    out_ds = gdal.Warp(out_ds, in_ds, options=options)
'''