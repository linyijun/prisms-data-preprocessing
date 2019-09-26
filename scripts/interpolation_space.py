import numpy as np
import datetime
from scipy.interpolate import griddata
from sqlalchemy import func

from data_models.aq_model import *
from data_models.common_db import session
from data_models.grid_model import *
from data_models.meo_model import *
from utils import create_table, check_status


def spatial_interpolate(**kwargs):

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

        if len(locations):
            target_coord = session.query(target_coord).filter(target_coord.c.gid.in_(locations)).subquery()

        target_id = [item[0] for item in session.query(target_coord.c.gid).all()]
        target_points = session.query(target_coord.c.lon_proj, target_coord.c.lat_proj).all()

        for t in times:

            data = session.query(old_obj_w_coord).filter(old_obj_w_coord.c.timestamp == t).order_by(old_obj_w_coord.c.gid)
            points = data.with_entities('lon_proj', 'lat_proj').all()
            values = np.array([item[0] for item in data.with_entities('data').all()])

            inter_data = griddata(points, values, target_points, method=inter_method)

            obj_results = [target_obj(gid=target_id[i], timestamp=t, data=v) for i, v in enumerate(inter_data.tolist())]
            session.add_all(obj_results)
            session.commit()

            print('Timestamp {} has finished. {} records has been generated.'.format(t, len(inter_data)))

        return {'status': 1, 'msg': ''}

    except Exception as e:
        return {'status': 0, 'msg': e}


def main(**kwargs):

    # meo_features = ['temperature', 'dew_point', 'humidity', 'pressure', 'wind_speed', 'wind_bearing',
    #                 'cloud_cover', 'visibility']

    if kwargs['if_all_grids_meo']:

        min_time = session.query(func.min(kwargs['old_obj'].timestamp)).scalar()
        max_time = session.query(func.max(kwargs['old_obj'].timestamp)).scalar()
        kwargs['times'] = [i[0] for i in session.query(func.generate_series(min_time, max_time, '1 hour')).all()]

    else:

        min_time = session.query(func.min(kwargs['old_obj'].timestamp)).scalar()
        max_time = session.query(func.max(kwargs['old_obj'].timestamp)).scalar()
        kwargs['times'] = [i[0] for i in session.query(func.generate_series(min_time, max_time, '1 hour')).all()]

        target_aq_obj = kwargs['target_aq_obj']
        kwargs['locations'] = sorted([loc[0] for loc in session.query(target_aq_obj.gid).distinct().all()])

    status = create_table(kwargs['target_obj'])
    check_status(status)
    status = spatial_interpolate(**kwargs)
    check_status(status)


if __name__ == '__main__':

    settings = [

        {
            'old_obj': LosAngeles5000mGridMeoDarkSkyInterpolate201811,
            'old_coord_obj': LosAngeles5000mGrid,
            'target_obj': LosAngeles500mGridMeoDarkSkyInterpolate201811,
            'target_coord_obj': LosAngeles500mGrid,
            'if_all_grids_meo': True
        },

        {
            'old_obj': LosAngeles5000mGridMeoDarkSkyInterpolate201811,
            'old_coord_obj': LosAngeles5000mGrid,
            'target_obj': LosAngeles1000mGridMeoDarkSkyInterpolate201811,
            'target_coord_obj': LosAngeles1000mGrid,
            'if_all_grids_meo': True
        }
    ]

    for setting in settings:
        main(**setting)
