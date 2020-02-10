import argparse
import pytz
from sqlalchemy import func
import pandas as pd
import numpy as np
import os

from data_models.aq_model import *
from data_models.common_db import session
from data_models.geo_feature_model import *
from data_models.grid_model import *
from data_models.meo_model import *


def gen_geo_vector(geo_obj, geo_name_obj, grid_list):
    """
    load geographic data and construct the geographic vector

    return:
        geo_vector: (n_loc, n_geo_features)
        geo_name_list: a list of geographic feature names
    """

    geo_data = session.query(geo_obj.data) \
        .filter(geo_obj.gid.in_(grid_list)) \
        .order_by(geo_obj.gid).all()

    n_geo_features = len(geo_data[0][0])
    geo_vector = np.array(geo_data).reshape(len(grid_list), n_geo_features)
    print('The shape of geographic vector = {}.'.format(geo_vector.shape))

    geo_name_df = pd.read_sql(session.query(geo_name_obj).statement, session.bind)
    geo_name_list = list(geo_name_df['name'])

    if len(geo_name_list) != n_geo_features:
        print('Something wrong with the geographic feature vector!')

    return geo_vector, geo_name_list


def gen_meo_vector(meo_obj, time_list, grid_list):
    """
    load weather data and construct the meo vector

    return:
        meo_vector: (n_times, n_loc, n_meo_features)
    """

    min_time, max_time = time_list[0], time_list[-1]
    n_times, n_loc = len(time_list), len(grid_list)

    meo_data = session.query(meo_obj.data) \
        .filter(meo_obj.timestamp >= min_time) \
        .filter(meo_obj.timestamp <= max_time) \
        .filter(meo_obj.gid.in_(grid_list)) \
        .order_by(meo_obj.timestamp, meo_obj.gid).all()

    n_meo_features = len(meo_data[0][0])
    meo_vector = np.array(meo_data).reshape((n_times, n_loc, n_meo_features))

    print('The shape of meo vector = {}.'.format(meo_vector.shape))
    return meo_vector


def gen_time_vector(time_list, grid_list):
    """
    construct time vector, including hour of a day, day of a week, and day of a month

    return:
        time_vector: (n_times, n_loc, n_feature=3)
    """

    n_times, n_loc = len(time_list), len(grid_list)

    def expand_dims(arr):
        arr = np.expand_dims(arr, axis=-1)
        arr = np.expand_dims(arr, axis=-1)
        arr = np.repeat(arr, n_loc, axis=1)
        return arr

    hour_arr = np.array([t.hour for t in time_list])
    hour_arr = expand_dims(hour_arr)
    time_vector = hour_arr

    dayofweek_arr = np.array([t.dayofweek for t in time_list])
    dayofweek_arr = expand_dims(dayofweek_arr)
    time_vector = np.concatenate([time_vector, dayofweek_arr], axis=-1)

    day_arr = np.array([t.day for t in time_list])
    day_arr = expand_dims(day_arr)
    time_vector = np.concatenate([time_vector, day_arr], axis=-1)

    month_arr = np.array([t.month for t in time_list])
    month_arr = expand_dims(month_arr)
    time_vector = np.concatenate([time_vector, month_arr], axis=-1)

    print('The shape of time vector = {}.'.format(time_vector.shape))
    return time_vector


def gen_label_mat(pm_obj, time_list, mapping_mat):
    """
    construct the label matrix, if there is no label for a grid, using Nan to fill in.

    return:
        pm_mat: (n_times, n_output=1, n_rows, n_cols)
    """

    min_time, max_time = time_list[0], time_list[-1]
    pm_query_sql = session.query(pm_obj.gid, pm_obj.timestamp, pm_obj.pm25) \
        .filter(pm_obj.timestamp >= min_time) \
        .filter(pm_obj.timestamp <= max_time) \
        .order_by(pm_obj.gid)

    pm_data = pd.read_sql(pm_query_sql.statement, session.bind)

    pm_mat_list = []
    for t in time_list:
        this_pm_data = pm_data[pm_data['timestamp'] == t]
        this_pm_grids = list(this_pm_data['gid'])
        this_pm_data = np.array(this_pm_data['pm25']).reshape((1, 1, -1))
        this_pm_mat = gen_grid_data(this_pm_data, this_pm_grids, mapping_mat)
        pm_mat_list.append(this_pm_mat)

    pm_mat = np.vstack(pm_mat_list)
    print('The shape of PM matrix = {}.'.format(pm_mat.shape))
    return pm_mat


def gen_grid_data(ori_data, loc_list, mapping_mat):
    """
    transferring original data to the matrix data

    params:
        ori_data: (n_times, n_features, n_loc)
        loc_list: list of corresponding locations
    return:
        tar_data: (n_times, n_features, n_rows, n_cols)
    """

    n_rows, n_cols = mapping_mat.shape
    n_times, n_features, n_loc = ori_data.shape  # n_times = 1 means transforming to a 2D array

    tar_data = np.full([n_times, n_features, n_rows, n_cols], np.nan)

    def get_index(tar):
        try:
            return loc_list.index(tar)
        except ValueError:
            return None

    for i in range(n_rows):
        for j in range(n_cols):
            gid = mapping_mat[i][j]
            idx = get_index(gid)
            if idx is not None:
                tar_data[..., i, j] = ori_data[..., idx]
    return tar_data


def main(input_obj):

    pm_obj = input_obj['pm_obj']
    meo_obj = input_obj['meo_obj']
    geo_obj = input_obj['geo_obj']
    geo_name_obj = input_obj['geo_name_obj']
    coord_obj = input_obj['coord_obj']

    # load mapping matrix
    mapping_mat = np.load(input_obj['mapping_mat_file'])['mat']

    # load grids
    coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
    grid_list = list(coord_df['gid'])
    print('Number of grids = {}.'.format(len(grid_list)))

    # get time list
    min_time, max_time = input_obj['min_time'], input_obj['max_time']
    tz = pytz.timezone('America/Los_Angeles')
    time_list = pd.date_range(start=min_time, end=max_time, closed='left', freq='1H')
    time_list = sorted(list(set([tz.localize(x) for x in time_list])))
    print('Data from {} to {}.'.format(min_time, max_time))
    print('Number of time points = {}.'.format(len(time_list)))

    # generate label data
    print('...Generating label data...')
    label_mat = gen_label_mat(pm_obj, time_list, mapping_mat)

    # generate dynamic data
    print('...Generating dynamic data...')
    meo_vector = gen_meo_vector(meo_obj, time_list, grid_list)
    time_vector = gen_time_vector(time_list, grid_list)
    dynamic_vector = np.concatenate([meo_vector, time_vector], axis=-1)

    # convert to feature matrix
    dynamic_mat = dynamic_vector.swapaxes(1, 2)  # (n_times, n_loc, n_features) => (n_times, n_features, n_loc)
    dynamic_mat = gen_grid_data(dynamic_mat, grid_list, mapping_mat)
    print('The shape of dynamic matrix = {}.'.format(dynamic_mat.shape))

    # generate static data
    print('...Generating static data...')
    geo_vector, geo_name_list = gen_geo_vector(geo_obj, geo_name_obj, grid_list)
    geo_vector = geo_vector.reshape(1, geo_vector.shape[0], geo_vector.shape[1])

    # convert to feature matrix
    static_mat = geo_vector.swapaxes(1, 2)  # (1, n_loc, n_features) => (1, n_features, n_loc)
    static_mat = gen_grid_data(static_mat, grid_list, mapping_mat)
    print('The shape of static matrix = {}.'.format(static_mat.shape))

    # combine static vector and dynamic vector
    # arr = np.expand_dims(geo_vector, axis=0)
    # arr = np.repeat(arr, len(time_list), axis=0)
    # feature_vector = np.concatenate([feature_vector, arr], axis=-1)

    np.savez_compressed(
        os.path.join(input_obj['output_file']),
        label_mat=label_mat,
        dynamic_mat=dynamic_mat,
        static_mat=static_mat,
        dynamic_features=np.array(['temperature', 'dew_point', 'humidity', 'pressure', 'wind_speed', 'wind_direction',
                                   'cloud_cover', 'visibility', 'hourofday', 'dayofweek', 'day', 'month']),
        static_features=np.array(geo_name_list),
        mapping_mat=mapping_mat
    )


if __name__ == "__main__":

    # data definition
    data_obj = {
        500: {
            'pm_obj': LosAngeles500mGridPurpleAirPM2018,
            'geo_obj': LosAngeles500mGridGeoVector,
            'geo_name_obj': LosAngeles500mGridGeoName,
            'coord_obj': LosAngeles500mGrid,
            '01': LosAngeles500mGridMeoDarkSkyInterpolate201801,
            '02': LosAngeles500mGridMeoDarkSkyInterpolate201802,
            '03': LosAngeles500mGridMeoDarkSkyInterpolate201803,
            '04': LosAngeles500mGridMeoDarkSkyInterpolate201804,
            '05': LosAngeles500mGridMeoDarkSkyInterpolate201805,
            '06': LosAngeles500mGridMeoDarkSkyInterpolate201806,
            '07': LosAngeles500mGridMeoDarkSkyInterpolate201807,
            '08': LosAngeles500mGridMeoDarkSkyInterpolate201808,
            '09': LosAngeles500mGridMeoDarkSkyInterpolate201809,
            '10': LosAngeles500mGridMeoDarkSkyInterpolate201810,
            '11': LosAngeles500mGridMeoDarkSkyInterpolate201811,
            '12': LosAngeles500mGridMeoDarkSkyInterpolate201812
        },
        1000: {
            'pm_obj': LosAngeles1000mGridPurpleAirPM2018,
            'geo_obj': LosAngeles1000mGridGeoVector,
            'geo_name_obj': LosAngeles1000mGridGeoName,
            'coord_obj': LosAngeles1000mGrid,
            '01': LosAngeles1000mGridMeoDarkSkyInterpolate201801,
            '02': LosAngeles1000mGridMeoDarkSkyInterpolate201802,
            '03': LosAngeles1000mGridMeoDarkSkyInterpolate201803,
            '04': LosAngeles1000mGridMeoDarkSkyInterpolate201804,
            '05': LosAngeles1000mGridMeoDarkSkyInterpolate201805,
            '06': LosAngeles1000mGridMeoDarkSkyInterpolate201806,
            '07': LosAngeles1000mGridMeoDarkSkyInterpolate201807,
            '08': LosAngeles1000mGridMeoDarkSkyInterpolate201808,
            '09': LosAngeles1000mGridMeoDarkSkyInterpolate201809,
            '10': LosAngeles1000mGridMeoDarkSkyInterpolate201810,
            '11': LosAngeles1000mGridMeoDarkSkyInterpolate201811,
            '12': LosAngeles1000mGridMeoDarkSkyInterpolate201812
        }
    }

    months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

    for res in [500, 1000]:
        m_data_obj = data_obj[res]
        for ix, month in enumerate(months):
            target_data_obj = m_data_obj
            target_data_obj['output_file'] = 'data/los_angeles_{}m_2018{}.npz'.format(res, month)
            target_data_obj['mapping_mat_file'] = 'data/los_angeles_{}m_grid_mat.npz'.format(res)
            target_data_obj['meo_obj'] = m_data_obj[month]
            target_data_obj['min_time'] = '2018-{}-01'.format(month)
            if month != '12':
                target_data_obj['max_time'] = '2018-{}-01'.format(months[ix + 1])
            else:
                target_data_obj['max_time'] = '2019-01-01'

            main(target_data_obj)
