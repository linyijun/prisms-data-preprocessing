from geoalchemy2 import WKTElement
from sqlalchemy import func, literal, Sequence

from data_models.common_db import session, engine
from data_models.grid_model import *
from data_models.osm_model import *
from data_models.geo_feature_model import *


def create_geo_feature_table(config):

    geo_feature = config['GEO_FEATURE_OBJ']

    try:
        geo_feature.__table__.drop(bind=engine, checkfirst=True)
        geo_feature.__table__.create(bind=engine)
        return {'status': 1, 'msg': ''}

    except Exception as e:
        return {'status': 0, 'msg': e}


def crop_osm(osm_table, bounding_box):

    if bounding_box is not None:
        return session.query(osm_table.wkb_geometry, osm_table.fclass) \
            .filter(func.ST_Intersects(osm_table.wkb_geometry, bounding_box)) \
            .filter(osm_table.fclass is not None).subquery()
    else:
        return session.query(osm_table.wkb_geometry, osm_table.fclass) \
            .filter(osm_table.fclass is not None).subquery()


def compute_features_from_osm(config):

    osm_tables = config['OSM']
    bounding_box = WKTElement(config['BOUNDING_BOX'], srid=4326)
    grid_obj = config['GRID_OBJ']
    geo_feature_obj = config['GEO_FEATURE_OBJ']

    try:
        for feature_name, osm_table in osm_tables.items():
            geo_feature_type = osm_table.wkb_geometry.type.geometry_type
            cropped_osm = crop_osm(osm_table, bounding_box)

            sub_query = session.query(grid_obj.gid, cropped_osm.c.fclass,
                                      func.ST_GeogFromWKB(
                                          func.ST_Intersection(grid_obj.geom, cropped_osm.c.wkb_geometry))
                                      .label('intersection')) \
                .filter(func.ST_Intersects(grid_obj.geom, cropped_osm.c.wkb_geometry)).subquery()

            results = []
            if geo_feature_type == 'MULTIPOLYGON':
                results = session.query(sub_query.c.gid.label('gid'),
                                        sub_query.c.fclass.label('feature_type'),
                                        literal(feature_name).label('geo_feature'),
                                        func.SUM(func.ST_AREA(sub_query.c.intersection)).label('value'),
                                        literal('area').label('measurement')) \
                    .group_by(sub_query.c.gid, sub_query.c.fclass).all()

            elif geo_feature_type == 'MULTILINESTRING':
                results = session.query(sub_query.c.gid.label('gid'),
                                        sub_query.c.fclass.label('feature_type'),
                                        literal(feature_name).label('geo_feature'),
                                        func.SUM(func.ST_LENGTH(sub_query.c.intersection)).label('value'),
                                        literal('length').label('measurement')) \
                    .group_by(sub_query.c.gid, sub_query.c.fclass).all()

            elif geo_feature_type == 'POINT':
                results = session.query(sub_query.c.gid.label('gid'),
                                        sub_query.c.fclass.label('feature_type'),
                                        literal(feature_name).label('geo_feature'),
                                        func.COUNT(sub_query.c.intersection).label('value'),
                                        literal('count').label('measurement')) \
                    .group_by(sub_query.c.gid, sub_query.c.fclass).all()

            else:
                pass

            obj_results = []
            for res in results:
                obj_results.append(geo_feature_obj(gid=res[0], feature_type=res[1], geo_feature=res[2],
                                                   value=res[3], measurement=res[4]))
            session.add_all(obj_results)
            session.commit()
            print('{} has finished'.format(feature_name))

        return {'status': 1, 'msg': ''}

    except Exception as e:
        return {'status': 0, 'msg': e}


def check_status(status):
    if status['status'] == 0:
        print(status['msg'])
        exit(1)
    else:
        pass


if __name__ == '__main__':

    LOS_ANGELES = {
        'AREA': 'los_angeles',
        'OSM': {
            'landuse_a': CaliforniaOsmLanduseA,
            'natural': CaliforniaOsmNatural,
            'natural_a': CaliforniaOsmNaturalA,
            'places': CaliforniaOsmPlaces,
            'places_a': CaliforniaOsmPlacesA,
            'pois': CaliforniaOsmPois,
            'pois_a': CaliforniaOsmPoisA,
            'pofw': CaliforniaOsmPofw,
            'pofw_a': CaliforniaOsmPofwA,
            'railways': CaliforniaOsmRailways,
            'roads': CaliforniaOsmRoads,
            'traffic': CaliforniaOsmTraffic,
            'traffic_a': CaliforniaOsmTrafficA,
            'transport': CaliforniaOsmTransport,
            'transport_a': CaliforniaOsmTransportA,
            'water_a': CaliforniaOsmWaterA,
            'waterways': CaliforniaOsmWaterway
        },
        "BOUNDING_BOX": 'POLYGON((-118.5246 33.7322, -118.5246 34.1455, -118.1158 34.1455, -118.1158 33.7322, '
                        '-118.5246 33.7322))',
        500: {
            "GRID_OBJ": LosAngeles500mGrid,
            "GEO_FEATURE_OBJ": LosAngeles500mGridGeoFeature,
        },
        1000: {
            "GRID_OBJ": LosAngeles1000mGrid,
            "GEO_FEATURE_OBJ": LosAngeles1000mGridGeoFeature,
        }
    }

    target = LOS_ANGELES
    res = 1000
    conf = target[res]
    conf['OSM'] = target['OSM']
    conf['BOUNDING_BOX'] = target['BOUNDING_BOX']

    status = create_geo_feature_table(conf)
    check_status(status)
    status = compute_features_from_osm(conf)
    check_status(status)
