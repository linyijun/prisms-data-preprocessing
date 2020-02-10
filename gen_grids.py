from geoalchemy2 import WKTElement
from sqlalchemy import func

from data_models.common_db import engine, session
from data_models.grid_model import *
from utils import create_table


def generate_grids(config, area=None):

    bounding_box = WKTElement(config['BOUNDING_BOX'], srid=4326)
    grid_obj = config['GRID_OBJ']
    resolution = config['RESOLUTION']
    epsg = config['EPSG']

    try:

        grids = session.query(func.ST_Dump(
            func.makegrid_2d(bounding_box, resolution, resolution)).geom.label('geom')  # self-defined function in Psql
        ).subquery()

        # using the boundary to crop the area
        # if config['AREA'] == 'los_angeles':
        #     grids = session.query(grids.c.geom) \
        #         .filter(func.ST_Intersects(LosAngelesCountyBoundary.wkb_geometry, grids.c.geom)).subquery()

        results = session.query(
            func.row_number().over().label('gid'),
            func.ST_Centroid(grids.c.geom).label('centroid'),
            func.ST_X(func.ST_Centroid(grids.c.geom)).label('lon'),
            func.ST_Y(func.ST_Centroid(grids.c.geom)).label('lat'),
            grids.c.geom,
            func.ST_X(func.ST_Transform(func.ST_Centroid(grids.c.geom), epsg)).label('lon_proj'),
            func.ST_Y(func.ST_Transform(func.ST_Centroid(grids.c.geom), epsg)).label('lat_proj')).all()

        obj_results = []
        for res in results:
            obj_results.append(grid_obj(gid=res[0], centroid=res[1], lon=res[2], lat=res[3],
                                        geom=res[4], lon_proj=res[5], lat_proj=res[6]))

        # session.add_all(obj_results)
        # session.commit()
        return

    except Exception as e:
        print(e)
        exit(-1)


if __name__ == '__main__':

    LOS_ANGELES = {
        'AREA': 'los_angeles',
        'BOUNDING_BOX': 'POLYGON((-118.5246 33.7322, -118.5246 34.1455, -118.1158 34.1455, -118.1158 33.7322, '
                        '-118.5246 33.7322))',
        'EPSG': 6423,  # epsg for Los Angeles
        500: {
            'GRID_OBJ': LosAngeles500mGrid,
            'RESOLUTION': 500
        },
        1000: {
            'GRID_OBJ': LosAngeles1000mGrid,
            'RESOLUTION': 1000,
        },
        5000: {
            'GRID_OBJ': LosAngeles5000mGrid,
            'RESOLUTION': 5000,
        }
    }

    target, res = LOS_ANGELES, 500
    conf = target[res]
    conf['BOUNDING_BOX'] = target['BOUNDING_BOX']
    conf['EPSG'] = target['EPSG']

    """ !!! Be careful, create table would overwrite the original table """
    # create_table(conf['GRID_OBJ'])
    generate_grids(conf)
