try:
    import arcgis
except ImportError: 
    arcgis = None
try:
    import pandas as pd
except ImportError:
    pd = None

import geopandas as gpd
from geodesic.client import get_client
from geodesic.raster import Raster
from shapely.geometry import shape
from typing import List

class Feature(dict):
    def __init__(self, obj=None):
        if isinstance(obj, dict):
            self.update(obj)

        self._geometry = None
    
    @property
    def geometry(self):
        if self._geometry is not None:
            return self._geometry

        self._geometry = shape(self['geometry'])
        return self._geometry
    
    def _repr_svg_(self):
        return self.geometry._repr_svg_()
    

class FeatureCollection(dict):
    def __init__(self, obj=None, _ds_type=None, _ds_subtype=None):
        # From GeoJSON
        if isinstance(obj, dict):
            self.update(obj)
        self._gdf = None
        self._sedf = None

        self._is_stac = False
        self._ds_type = _ds_type
        self._ds_subtype = _ds_subtype

    @property
    def features(self):
        if self._is_stac:
            return [Item(f, item_type=self._ds_subtype) for f in self['features']]
        else:
            return [Feature(f) for f in self['features']]


    @property
    def gdf(self):
        if gpd is None:
            raise ValueError("this method requires geopandas (not installed)")
        if self._gdf is not None:
            return self._gdf
        df = pd.DataFrame(self['features'])
        geo = [shape(g) for g in df.geometry]
        self._gdf =  gpd.GeoDataFrame(df, geometry=geo, crs='EPSG:4326')
        return self._gdf
    
    @property
    def sedf(self):
        if pd is None:
            raise ValueError("this method requires pandas (not installed)")
        if self._sedf is not None:
            return self._sedf
        df = pd.DataFrame(self['features'])
        geo = [arcgis.geometry.Geometry.from_shapely(shape(g)) for g in df.geometry]
        df.spatial.set_geometry(geo)
        self._sedf = df
        return self._sedf

    @property
    def __geo_interface__(self):
        return dict(self)

    @property
    def _next_link(self):
        links = self.get("links", [])
        for link in links:
            if link.get("rel", None) == "next":
                return link.get("href")

    def get_all(self):
        features = self.get("features", [])
        client = get_client()
        next_uri = self._next_link
        while next_uri is not None:

            res = client.get(next_uri)
            if len(res['features']) == 0:
                return

            features.extend(res['features'])
            next_uri = self._next_link
            break
        

class Item(Feature):
    def __init__(self, obj=None, item_type=None):
        super().__init__(obj)
        self.item_type = item_type

    def _repr_html_(self):
        assets = self.get('assets', {})
        if 'thumbnail' in assets:
            return '<img src="{0}" style="width: 500px;"></img>'.format(assets['thumbnail']['href'])
        else:
            return self._repr_svg_()

    @property
    def raster(self):
        if self.item_type != 'raster':
            raise ValueError("item must be of raster type, is: '{0}'".format(self.item_type))
        return Raster(self)


    @property
    def assets(self):
        return {
            k: Asset(v) for k, v in self['assets'].items()
        }

class Asset(dict):
    
    @property
    def href(self) -> str:
        return self['href']

    @property
    def roles(self) -> List[str]:
        return self.get('roles', [])
    
    def has_role(self, role: str):
        for r in self.roles:
            if role == r:
                return True
        return False
