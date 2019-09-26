import argparse
import pandas as pd
import numpy as np
import decimal
import os

from data_models.aq_model import *
from data_models.common_db import session
from data_models.grid_model import *


def get_horizontal_neighbor(this_lon, this_lat, lat_dict, coord_dict, direction=1):
    """
        left: direction = -1, right: direction = 1
    """

    lon_list = lat_dict[this_lat]
    lon_index = lon_list.index(this_lon) + direction
    if 0 <= lon_index < len(lon_list):
        return coord_dict[(lon_list[lon_index], this_lat)]
    else:
        return None


def get_vertical_neighbor(this_lon, this_lat, lat_list, lat_dict, coord_dict, direction=1):
    """
        down: direction = -1, up: direction = 1
    """

    lat_index = lat_list.index(this_lat) + direction
    if 0 <= lat_index < len(lat_list):
        neighbor_lat = lat_list[lat_index]
        lon_list = lat_dict[neighbor_lat]
        neighbor_lon = min(lon_list, key=lambda x: abs(x - this_lon))
        return coord_dict[(neighbor_lon, neighbor_lat)]
    else:
        return None


def gen_matrix(coord_obj):

    coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
    coord_df = coord_df.round(10)
    coord_dict = {(row[1], row[2]): int(row[0]) for row in coord_df.values.tolist()}

    lat_list = sorted(coord_df['lat'].drop_duplicates())
    lat_dict = coord_df[['lon', 'lat']].groupby('lat')['lon'].apply(lambda x: sorted(x)).to_dict()

    n_rows = len(lat_list)
    n_cols = min([len(v) for k, v in lat_dict.items()])

    # find neighbors ["left", "right", "up", "down"] for the gid
    neighbors = {}
    for idx, row in coord_df.iterrows():
        gid, this_lon, this_lat = int(row['gid']), row['lon'], row['lat']
        neighbors[gid] = {}
        neighbors[gid]['left'] = get_horizontal_neighbor(this_lon, this_lat, lat_dict, coord_dict, direction=-1)
        neighbors[gid]['right'] = get_horizontal_neighbor(this_lon, this_lat, lat_dict, coord_dict, direction=1)
        neighbors[gid]['up'] = get_vertical_neighbor(this_lon, this_lat, lat_list, lat_dict, coord_dict, direction=1)
        neighbors[gid]['down'] = get_vertical_neighbor(this_lon, this_lat, lat_list, lat_dict, coord_dict, direction=-1)

    # convert neighbors to the matrix
    mat = np.full(([n_rows, n_cols]), -1)
    curr_gid = min(coord_dict.values())
    curr_row = curr_gid

    for i in range(n_rows-1, -1, -1):
        for j in range(n_cols):
            mat[i][j] = curr_gid
            if j < n_cols - 1:
                curr_gid = neighbors[curr_gid]['right']
            else:
                curr_gid = neighbors[curr_row]['up']
                curr_row = curr_gid

    """
        mat = array([[6917, 6918, 6919, ..., 6990, 6991, 6992],
                     [6841, 6842, 6843, ..., 6914, 6915, 6916],
                     [6765, 6766, 6767, ..., 6838, 6839, 6840],
                     ...,
                     [153, 154, 155, ..., 226, 227, 228],
                     [77, 78, 79, ..., 150, 151, 152],
                     [1, 2, 3, ..., 74, 75, 76]])
    """

    return mat


def main(coord_obj, args):

    mat = gen_matrix(coord_obj)
    global_n_rows, global_n_cols = mat.shape

    print('Number of rows = {}.'.format(global_n_rows))
    print('Number of cols = {}.'.format(global_n_cols))

    np.savez_compressed(
        os.path.join(args.output_dir, args.output_filename),
        mat=mat
    )


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument('--output_dir', type=str, default='data/', help='output directory')
    parser.add_argument('--output_fname', type=str, default='salt_lake_city_500m_grid_mat.npz', help='output filename')
    args = parser.parse_args()

    target_coord_obj = SalkLakeCity500mGrid
    main(target_coord_obj, args)
