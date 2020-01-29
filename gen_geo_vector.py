from sqlalchemy import func
import pandas as pd

from data_models.common_db import session
from data_models.geo_feature_model import *
from data_models.grid_model import *
from utils import create_table


DEFAULT = {

    "geo_features": [
        "landuse_a",
        "natural",
        "natural_a",
        "places",
        "places_a",
        "pofw",
        "pofw_a"
        "pois"
        "pois_a",
        "railways",
        "roads",
        "traffic",
        "traffic_a",
        "transport",
        "transport_a",
        "water_a",
        "waterways"
    ],

    "exempt_types": [
        "unknown",
        "unclassified"
    ]
}


def construct_geo_vector(**kwargs):

    geo_feature_obj = kwargs['geo_feature_obj']
    coord_obj = kwargs['coord_obj']
    geo_vector_obj = kwargs['geo_vector_obj']
    geo_name_obj = kwargs['geo_name_obj']

    locations = sorted([i[0] for i in session.query(coord_obj.gid).all()])
    geo_name_df = pd.read_sql(session.query(geo_name_obj.name).statement, session.bind)

    try:
        for loc in locations:

            geo_data_sql = session.query(geo_feature_obj.value, func.concat(
                geo_feature_obj.geo_feature, '_', geo_feature_obj.feature_type).label('name')) \
                .filter(geo_feature_obj.gid == loc).statement

            geo_data_df = pd.read_sql(geo_data_sql, session.bind)
            geo_data = geo_name_df.merge(geo_data_df, on='name', how='left')
            geo_data = geo_data['value'].fillna(0.0)

            coord = session.query(coord_obj.lon, coord_obj.lat).filter(coord_obj.gid == loc).first()
            obj_result = geo_vector_obj(gid=loc, data=list(geo_data) + list(coord))

            session.add(obj_result)
            session.commit()

            if loc % 1000 == 0:
                print('Geo Vector {} has finished.'.format(len(list(geo_data) + list(coord))))

        # adding lon, lat into geo feature names
        obj_results = [geo_name_obj(name='lon', geo_feature='location', feature_type='lon'),
                       geo_name_obj(name='lat', geo_feature='location', feature_type='lat')]
        # session.add_all(obj_results)
        # session.commit()

        return

    except Exception as e:
        print(e)
        exit(-1)


def construct_geo_name(geo_feature_obj, geo_name_obj):

    try:
        #  filter geographic data by features and feature types

        geo_data = session.query(geo_feature_obj) \
            .filter(geo_feature_obj.geo_feature.in_(DEFAULT['geo_features'])) \
            .filter(~geo_feature_obj.feature_type.in_(DEFAULT['exempt_types'])).subquery()

        geo_name = session.query(func.concat(geo_data.c.geo_feature, '_', geo_data.c.feature_type).label('name'),
                                 geo_data.c.geo_feature, geo_data.c.feature_type).distinct().order_by('name').all()

        obj_results = [geo_name_obj(name=item[0], geo_feature=item[1], feature_type=item[2]) for item in geo_name]
        # session.add_all(obj_results)
        # session.commit()

        print('Generated {} Geo Names.'.format(len(geo_name)))
        return

    except Exception as e:
        print(e)
        exit(-1)


def main(**kwargs):

    """ !!! Be careful, create table would overwrite the original table """
    # create_table(kwargs['geo_name_obj'])
    construct_geo_name(kwargs['geo_feature_obj'], kwargs['geo_name_obj'])

    # create_table(kwargs['geo_vector_obj'])
    construct_geo_vector(**kwargs)


if __name__ == '__main__':

    configs = [

        # {
        #     'coord_obj': LosAngeles500mGrid,
        #     'geo_feature_obj': LosAngeles500mGridGeoFeature,
        #     'geo_vector_obj': LosAngeles500mGridGeoVector,
        #     'geo_name_obj': LosAngeles500mGridGeoName
        # },

        # {
        #     'coord_obj': LosAngeles1000mGrid,
        #     'geo_feature_obj': LosAngeles1000mGridGeoFeature,
        #     'geo_vector_obj': LosAngeles1000mGridGeoVector,
        #     'geo_name_obj': LosAngeles1000mGridGeoName
        # },

        {
            'coord_obj': SaltLakeCity500mGrid,
            'geo_feature_obj': SaltLakeCity500mGridGeoFeature,
            'geo_vector_obj': SaltLakeCity500mGridGeoVector,
            'geo_name_obj': SaltLakeCity500mGridGeoName
        },
        {
            'coord_obj': SaltLakeCity1000mGrid,
            'geo_feature_obj': SaltLakeCity1000mGridGeoFeature,
            'geo_vector_obj': SaltLakeCity1000mGridGeoVector,
            'geo_name_obj': SaltLakeCity1000mGridGeoName
        }
    ]

    for conf in configs:
        main(**conf)
