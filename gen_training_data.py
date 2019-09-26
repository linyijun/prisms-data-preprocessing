import argparse
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
        trimmed_geo_name_list: a list of trimmed geographic feature names
        n_trimmed_geo_features
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

    # # remove the features that too few locations have them
    # trimmed_mask = np.count_nonzero(geo_vector, axis=0) > 0.01 * len(grid_list)
    # trimmed_geo_vector = geo_vector[:, trimmed_mask]
    #
    # trimmed_geo_name_list = [name for i, name in enumerate(geo_name_list) if trimmed_mask[i]]
    # n_trimmed_geo_features = trimmed_geo_vector.shape[-1]
    # print('The shape of trimmed geo vector = {}.'.format(trimmed_geo_vector.shape))
    # print('Number of trimmed geo features = {}.'.format(n_trimmed_geo_features))
    # return trimmed_geo_vector, trimmed_geo_name_list

    return geo_vector, geo_name_list


def gen_meo_vector(meo_obj, time_list, grid_list):
    """
    load weather data and construct the meo vector

    return:
        meo_vector: (n_times, n_loc, n_meo_features)
        n_meo_features: 8
    """

    min_time, max_time = time_list[0], time_list[-1]

    meo_data = session.query(meo_obj.data) \
        .filter(meo_obj.timestamp >= min_time) \
        .filter(meo_obj.timestamp <= max_time) \
        .filter(meo_obj.gid.in_(grid_list)) \
        .order_by(meo_obj.timestamp, meo_obj.gid).all()

    n_meo_features = len(meo_data[0][0])
    meo_vector = np.array(meo_data).reshape(len(time_list), len(grid_list), n_meo_features)

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

    print('The shape of time vector = {}.'.format(time_vector.shape))
    return time_vector


def gen_label_mat(pm_obj, time_list, mapping_mat):
    """
    construct the label matrix, if there is no label for a grid, using Nan to fill in.

    return:
        pm_mat: (n_times, n_output=1, n_rows, n_cols)
    """

    min_time, max_time = time_list[0], time_list[-1]
    pm_query_sql = session.query(pm_obj) \
        .filter(pm_obj.timestamp >= min_time) \
        .filter(pm_obj.timestamp <= max_time) \
        .order_by(pm_obj.gid)

    pm_data = pd.read_sql(pm_query_sql.statement, session.bind)

    pm_mat_list = []
    for t in time_list:
        this_pm_data = pm_data[pm_data['timestamp'] == t]
        this_pm_locations = list(this_pm_data['gid'].drop_duplicates())
        this_pm_data = np.array(this_pm_data['pm']).reshape(1, 1, -1)
        this_pm_mat = gen_grid_data(this_pm_data, this_pm_locations, mapping_mat)
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


def main(data_obj, args):

    pm_obj = data_obj['pm_obj']
    meo_obj = data_obj['meo_obj']
    geo_obj = data_obj['geo_obj']
    geo_name_obj = data_obj['geo_name_obj']
    coord_obj = data_obj['coord_obj']

    # get time range of the target
    max_time = session.query(func.max(pm_obj.timestamp)).scalar()
    min_time = session.query(func.min(pm_obj.timestamp)).scalar()
    time_list = pd.date_range(start=min_time, end=max_time, freq='1H')
    times_pd = pd.DataFrame(time_list.tolist(), columns=['timestamp'])
    print('Data from {} to {}.'.format(min_time, max_time))
    print('Number of time points = {}.'.format(len(time_list)))

    # get all grid locations
    coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
    grid_list = list(coord_df['gid'])
    print('Number of grids = {}.'.format(len(grid_list)))

    # load mapping matrix
    mapping_mat = np.load(os.path.join(args.data_dir, args.mapping_mat))['mat']

    print("...Generating label data...")
    label_mat = gen_label_mat(pm_obj, time_list, mapping_mat)

    print("...Generating dynamic data...")
    meo_vector = gen_meo_vector(meo_obj, time_list, grid_list)
    time_vector = gen_time_vector(time_list, grid_list)

    print("...Generating static data...")
    geo_vector, geo_name_list = gen_geo_vector(geo_obj, geo_name_obj, grid_list)

    # combine static vector and dynamic vector
    feature_vector = np.concatenate([meo_vector, time_vector], axis=-1)
    arr = np.expand_dims(geo_vector, axis=0)
    arr = np.repeat(arr, len(time_list), axis=0)
    feature_vector = np.concatenate([feature_vector, arr], axis=-1)

    # convert to feature matrix
    feature_mat = feature_vector.swapaxes(1, 2)
    feature_mat = gen_grid_data(feature_mat, grid_list, mapping_mat)
    print('The shape of feature matrix = {}.'.format(feature_mat.shape))

    np.savez_compressed(
        os.path.join(args.data_dir, args.output_filename),
        label_mat=label_mat,
        feature_mat=feature_mat,
        feature_distribution=np.array([meo_vector.shape[-1], time_vector.shape[-1], geo_vector.shape[-1]]),
        geo_name=np.array(geo_name_list)
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--data_dir', type=str, default='data/', help='data directory')
    parser.add_argument('--mapping_mat', type=str, default='los_angeles_500m_grid_mat.npz', help='')
    parser.add_argument('--output_filename', type=str, default='los_angeles_500m_data.npz', help='output filename')

    args = parser.parse_args()

    # data definition
    data_obj = {
        ('los_angeles', 500):
            {
                'pm_obj': LosAngeles500mGridAirQuality201811Trimmed,
                'meo_obj': LosAngeles500mGridMeoDarkSkyInterpolate201811,
                'geo_obj': LosAngeles500mGridGeoVector,
                'geo_name_obj': LosAngeles500mGridGeoName,
                'coord_obj': LosAngeles500mGrid
        },
        ('los_angeles', 1000):
            {
                'pm_obj': LosAngeles1000mGridAirQuality201811Trimmed,
                'meo_obj': LosAngeles1000mGridMeoDarkSkyInterpolate201811,
                'geo_obj': LosAngeles1000mGridGeoVector,
                'geo_name_obj': LosAngeles1000mGridGeoName,
                'coord_obj': LosAngeles1000mGrid
        }
    }

    target_data_obj = data_obj[('los_angeles', 500)]
    main(target_data_obj, args)
