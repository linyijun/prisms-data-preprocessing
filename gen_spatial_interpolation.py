import numpy as np
from scipy.interpolate import griddata
from sqlalchemy import func
import pytz
import pandas as pd

from data_models.common_db import session
from data_models.grid_model import *
from data_models.meo_model import *
from utils import create_table


def interpolate_space(**kwargs):

    inter_method = 'cubic'
    old_obj = kwargs['old_obj']
    old_coord_obj = kwargs['old_coord_obj']
    target_obj = kwargs['target_obj']
    target_coord_obj = kwargs['target_coord_obj']
    times = kwargs['times']
    locations = kwargs.get('locations', [])

    try:
        old_obj_w_coord = session.query(old_obj, old_coord_obj.lon_proj, old_coord_obj.lat_proj) \
            .filter(old_obj.gid == old_coord_obj.gid).subquery()

        target_coord = session.query(target_coord_obj).order_by(target_coord_obj.gid).subquery()

        # if given the locations, only interpolate for target locations
        if len(locations):
            target_coord = session.query(target_coord).filter(target_coord.c.gid.in_(locations)).subquery()

        target_id = [item[0] for item in session.query(target_coord.c.gid).all()]
        target_points = session.query(target_coord.c.lon_proj, target_coord.c.lat_proj).all()

        for t in times:

            data = session.query(old_obj_w_coord).filter(old_obj_w_coord.c.timestamp == t) \
                .order_by(old_obj_w_coord.c.gid)

            points = data.with_entities('lon_proj', 'lat_proj').all()
            values = np.array([item[0] for item in data.with_entities('data').all()])

            inter_data = griddata(points, values, target_points, method=inter_method)

            obj_results = [target_obj(gid=target_id[i], timestamp=t, data=v) for i, v in enumerate(inter_data.tolist())]
            session.add_all(obj_results)
            session.commit()

            print('Timestamp {} has finished. {} records has been generated.'.format(t, len(inter_data)))
        return

    except Exception as e:
        print(e)
        exit(-1)


def main(**kwargs):

    """
         meo_features = ['temperature', 'dew_point', 'humidity', 'pressure', 'wind_speed', 'wind_bearing',
                         'cloud_cover', 'visibility']
    """

    max_time = session.query(func.max(kwargs['old_obj'].timestamp)).scalar().strftime('%Y-%m-%d %H:%M:%S')
    min_time = session.query(func.min(kwargs['old_obj'].timestamp)).scalar().strftime('%Y-%m-%d %H:%M:%S')
    tz = pytz.timezone('America/Los_Angeles')
    time_df = pd.date_range(start=min_time, end=max_time, freq='1H')
    time_list = sorted(list(set([tz.localize(x) for x in time_df])))
    kwargs['times'] = time_list
    print(len(time_list))

    if not kwargs['if_all_grids_meo']:

        target_aq_obj = kwargs['target_aq_obj']
        kwargs['locations'] = sorted([loc[0] for loc in session.query(target_aq_obj.gid).distinct().all()])

    """ !!! Be careful, create table would overwrite the original table """
    create_table(kwargs['target_obj'])
    interpolate_space(**kwargs)


if __name__ == '__main__':

    query_obj = {
        # (1, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201801, LosAngeles500mGridMeoDarkSkyInterpolate201801],
        # (1, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201801, LosAngeles1000mGridMeoDarkSkyInterpolate201801],
        # (2, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201802, LosAngeles500mGridMeoDarkSkyInterpolate201802],
        # (2, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201802, LosAngeles1000mGridMeoDarkSkyInterpolate201802],
        # (3, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201803, LosAngeles500mGridMeoDarkSkyInterpolate201803],
        # (3, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201803, LosAngeles1000mGridMeoDarkSkyInterpolate201803],
        # (4, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201804, LosAngeles500mGridMeoDarkSkyInterpolate201804],
        # (4, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201804, LosAngeles1000mGridMeoDarkSkyInterpolate201804],
        # (5, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201805, LosAngeles500mGridMeoDarkSkyInterpolate201805],
        # (5, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201805, LosAngeles1000mGridMeoDarkSkyInterpolate201805],
        # (6, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201806, LosAngeles500mGridMeoDarkSkyInterpolate201806],
        # (6, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201806, LosAngeles1000mGridMeoDarkSkyInterpolate201806],
        # (7, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201807, LosAngeles500mGridMeoDarkSkyInterpolate201807],
        # (7, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201807, LosAngeles1000mGridMeoDarkSkyInterpolate201807],
        # (8, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201808, LosAngeles500mGridMeoDarkSkyInterpolate201808],
        # (8, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201808, LosAngeles1000mGridMeoDarkSkyInterpolate201808],
        # (9, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201809, LosAngeles500mGridMeoDarkSkyInterpolate201809],
        # (9, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201809, LosAngeles1000mGridMeoDarkSkyInterpolate201809],
        # (10, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201810, LosAngeles500mGridMeoDarkSkyInterpolate201810],
        # (10, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201810, LosAngeles1000mGridMeoDarkSkyInterpolate201810],
        # (11, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201811, LosAngeles500mGridMeoDarkSkyInterpolate201811],
        # (11, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201811, LosAngeles1000mGridMeoDarkSkyInterpolate201811],
        # (12, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201812, LosAngeles500mGridMeoDarkSkyInterpolate201812],
        # (12, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201812, LosAngeles1000mGridMeoDarkSkyInterpolate201812],
        (1, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201901, LosAngeles500mGridMeoDarkSkyInterpolate201901],
        (1, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201901, LosAngeles1000mGridMeoDarkSkyInterpolate201901],
        (2, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201902, LosAngeles500mGridMeoDarkSkyInterpolate201902],
        (2, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201902, LosAngeles1000mGridMeoDarkSkyInterpolate201902],
        (3, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201903, LosAngeles500mGridMeoDarkSkyInterpolate201903],
        (3, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201903, LosAngeles1000mGridMeoDarkSkyInterpolate201903],
        (4, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201904, LosAngeles500mGridMeoDarkSkyInterpolate201904],
        (4, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201904, LosAngeles1000mGridMeoDarkSkyInterpolate201904],
        (5, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201905, LosAngeles500mGridMeoDarkSkyInterpolate201905],
        (5, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201905, LosAngeles1000mGridMeoDarkSkyInterpolate201905],
        (6, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201906, LosAngeles500mGridMeoDarkSkyInterpolate201906],
        (6, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201906, LosAngeles1000mGridMeoDarkSkyInterpolate201906],
        (7, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201907, LosAngeles500mGridMeoDarkSkyInterpolate201907],
        (7, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201907, LosAngeles1000mGridMeoDarkSkyInterpolate201907],
        (8, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201908, LosAngeles500mGridMeoDarkSkyInterpolate201908],
        (8, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201908, LosAngeles1000mGridMeoDarkSkyInterpolate201908],
        (9, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201909, LosAngeles500mGridMeoDarkSkyInterpolate201909],
        (9, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201909, LosAngeles1000mGridMeoDarkSkyInterpolate201909],
        (10, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201910, LosAngeles500mGridMeoDarkSkyInterpolate201910],
        (10, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201910, LosAngeles1000mGridMeoDarkSkyInterpolate201910],
        (11, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201911, LosAngeles500mGridMeoDarkSkyInterpolate201911],
        (11, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201911, LosAngeles1000mGridMeoDarkSkyInterpolate201911],
        (12, 500): [LosAngeles5000mGridMeoDarkSkyInterpolate201912, LosAngeles500mGridMeoDarkSkyInterpolate201912],
        (12, 1000): [LosAngeles5000mGridMeoDarkSkyInterpolate201912, LosAngeles1000mGridMeoDarkSkyInterpolate201912],
    }

    for obj in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        conf = [{
                'old_obj': query_obj[(obj, 500)][0],
                'old_coord_obj': LosAngeles5000mGrid,
                'target_obj': query_obj[(obj, 500)][1],
                'target_coord_obj': LosAngeles500mGrid,
                'if_all_grids_meo': True},
            {
                'old_obj': query_obj[(obj, 1000)][0],
                'old_coord_obj': LosAngeles5000mGrid,
                'target_obj': query_obj[(obj, 1000)][1],
                'target_coord_obj': LosAngeles1000mGrid,
                'if_all_grids_meo': True
            }]


