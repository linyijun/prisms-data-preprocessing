import pandas as pd
import pytz
from sqlalchemy import func

from data_models.common_db import session
from data_models.meo_model import *
from utils import create_table


def interpolate_time(old_obj, target_obj, time_list, features):

    try:
        time_df = pd.DataFrame(time_list, columns=['timestamp']).set_index(['timestamp'])
        locations = session.query(old_obj.gid).distinct(old_obj.gid).all()
        locations = sorted([loc[0] for loc in locations])

        for loc in locations:

            data = session.query(old_obj.timestamp, *features).filter(old_obj.gid == loc)\
                .order_by(old_obj.timestamp).all()

            df = pd.DataFrame(data, columns=['timestamp'] + features).set_index(['timestamp'])
            df = df.loc[~df.index.duplicated(keep='first')]  # remove the potential duplicates in index
            df = df.join(time_df, how='right').sort_index()
            # df['wind_bearing'] = df['wind_bearing'].apply(lambda x: x - 360 if x > 180 else x)

            inter_data = df.interpolate(method='linear').reset_index()

            obj_results = [target_obj(gid=loc, timestamp=dt[0], data=dt[1:]) for dt in inter_data.values.tolist()]
            # session.add_all(obj_results)
            # session.commit()

            print('Location {} has finished. {} records has been generated.'.format(loc, len(inter_data)))
        return

    except Exception as e:
        print(e)
        exit(-1)


def main(old_meo_obj, target_meo_obj):

    meo_features = ['temperature', 'dew_point', 'humidity', 'pressure', 'wind_speed', 'wind_bearing',
                    'cloud_cover', 'visibility']

    max_time = session.query(func.max(old_meo_obj.timestamp)).scalar().strftime('%Y-%m-%d %H:%M:%S')
    min_time = session.query(func.min(old_meo_obj.timestamp)).scalar().strftime('%Y-%m-%d %H:%M:%S')
    tz = pytz.timezone('America/Los_Angeles')
    time_df = pd.date_range(start=min_time, end=max_time, freq='1H')
    time_list = sorted(list(set([tz.localize(x) for x in time_df])))
    print(len(time_list))

    """ !!! Be careful, create table would overwrite the original table """
    # create_table(target_meo_obj)
    interpolate_time(old_meo_obj, target_meo_obj, time_list, meo_features)


if __name__ == '__main__':

    query_obj = {
        1: [LosAngeles5000mGridMeoDarkSky201801, LosAngeles5000mGridMeoDarkSkyInterpolate201801],
        2: [LosAngeles5000mGridMeoDarkSky201802, LosAngeles5000mGridMeoDarkSkyInterpolate201802],
        3: [LosAngeles5000mGridMeoDarkSky201803, LosAngeles5000mGridMeoDarkSkyInterpolate201803],
        4: [LosAngeles5000mGridMeoDarkSky201804, LosAngeles5000mGridMeoDarkSkyInterpolate201804],
        5: [LosAngeles5000mGridMeoDarkSky201805, LosAngeles5000mGridMeoDarkSkyInterpolate201805],
        6: [LosAngeles5000mGridMeoDarkSky201806, LosAngeles5000mGridMeoDarkSkyInterpolate201806],
        7: [LosAngeles5000mGridMeoDarkSky201807, LosAngeles5000mGridMeoDarkSkyInterpolate201807],
        8: [LosAngeles5000mGridMeoDarkSky201808, LosAngeles5000mGridMeoDarkSkyInterpolate201808],
        9: [LosAngeles5000mGridMeoDarkSky201809, LosAngeles5000mGridMeoDarkSkyInterpolate201809],
        10: [LosAngeles5000mGridMeoDarkSky201810, LosAngeles5000mGridMeoDarkSkyInterpolate201810],
        11: [LosAngeles5000mGridMeoDarkSky201811, LosAngeles5000mGridMeoDarkSkyInterpolate201811],
        12: [LosAngeles5000mGridMeoDarkSky201812, LosAngeles5000mGridMeoDarkSkyInterpolate201812]
    }

    for obj in [1, 2, 3, 4, 5, 6, 7, 8, 9, 11, 12]:
        old_meo, target_meo = query_obj[obj]
        main(old_meo, target_meo)
