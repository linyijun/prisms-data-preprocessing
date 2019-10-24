import pandas as pd
from sqlalchemy import func

from data_models.common_db import session
from data_models.meo_model import *
from utils import create_table, check_status


def interpolate_time(old_obj, target_obj, times, features):

    try:
        locations = session.query(old_obj.gid).distinct(old_obj.gid).all()
        locations = sorted([loc[0] for loc in locations])

        for loc in locations:

            data = session.query(old_obj).filter(old_obj.gid == loc) \
                .outerjoin(times, old_obj.timestamp == times.c.timestamp).order_by(old_obj.timestamp) \
                .with_entities(old_obj.timestamp, *features).all()

            df = pd.DataFrame(data, columns=['timestamp'] + features).set_index('timestamp', drop=True)
            df['wind_bearing'] = df['wind_bearing'].apply(lambda x: x - 360 if x > 180 else x)

            inter_data = df.interpolate(method='time').reset_index()

            obj_results = [target_obj(gid=loc, timestamp=dt[0], data=dt[1:]) for dt in inter_data.values.tolist()]
            session.add_all(obj_results)
            session.commit()

            print('Location {} has finished. {} records has been generated.'.format(loc, len(inter_data)))

        return {'status': 1, 'msg': ''}

    except Exception as e:
        return {'status': 0, 'msg': e}


def main(old_meo_obj, target_meo_obj):

    meo_features = ['temperature', 'dew_point', 'humidity', 'pressure', 'wind_speed', 'wind_bearing',
                    'cloud_cover', 'visibility']

    max_time = session.query(func.max(old_meo_obj.timestamp)).scalar()
    min_time = session.query(func.min(old_meo_obj.timestamp)).scalar()
    times = session.query(func.generate_series(min_time, max_time, '1 hour').label('timestamp')).subquery()

    # one time execution
    status = create_table(target_meo_obj)
    check_status(status)
    status = interpolate_time(old_meo_obj, target_meo_obj, times, meo_features)
    check_status(status)


if __name__ == '__main__':

    old_meo = LosAngeles5000mGridMeoDarkSky201802
    target_meo = LosAngeles5000mGridMeoDarkSkyInterpolate201802
    main(old_meo, target_meo)
