import math

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
import json
import random
from sklearn.cluster import DBSCAN, KMeans
from sqlalchemy import func

from data_models.aq_model import *
from data_models.grid_model import *
from data_models.common_db import session


class Location:
    def __init__(self, gid, lon, lat):
        self.gid = gid
        self.lon = lon
        self.lat = lat
        self.coord = (lon, lat)


class LocationSet:
    def __init__(self, grid_list, coordinate_arr):
        self.gid_list = grid_list  # a list of gid
        self.coordinate_arr = coordinate_arr  # an array of (n, 2)
        self.locations = self.build_location_list()
        self.location_dict = self.build_location_dict()

    def build_location_list(self):
        locations = []
        for i, gid in enumerate(self.gid_list):
            loc = Location(gid=gid, lon=self.coordinate_arr[i][0], lat=self.coordinate_arr[i][1])
            locations.append(loc)
        return locations

    def build_location_dict(self):
        return {self.gid_list[i]: loc for i, loc in enumerate(self.locations)}


def plot(locations):
    lon_list, lat_list = [i.lon for i in locations], [i.lat for i in locations]
    plt.scatter(lon_list, lat_list)
    plt.show()


def gen_train_val_test(label_dict, **kwargs):  # label_dict: {label: [locations]}
    train_radio = kwargs.get('train_radio', 0.6)
    val_radio = kwargs.get('val_radio', 0.2)

    train_loc, val_loc, test_loc = [], [], []

    for _, lo in label_dict.items():
        if len(lo) <= 1:
            train_loc += lo
        elif len(lo) == 2:
            train_loc += lo[0: 1]
            test_loc += lo[1: 2]
        else:
            random.shuffle(lo)
            train_loc += lo[: int(train_radio * len(lo))]
            val_loc += lo[int(train_radio * len(lo)): int((train_radio + val_radio) * len(lo))]
            test_loc += lo[int((train_radio + val_radio) * len(lo)):]

    return train_loc, val_loc, test_loc


def gen_labels_with_lon_lat(location_set):

    n = 2
    lon_list = [i[0] for i in location_set.coordinate_arr]
    lat_list = [i[1] for i in location_set.coordinate_arr]

    lon_split = [min(lon_list)] + [(max(lon_list) - min(lon_list)) * i / n + min(lon_list) for i in range(1, n)] + [max(lon_list)]
    lat_split = [min(lat_list)] + [(max(lat_list) - min(lat_list)) * i / n + min(lat_list) for i in range(1, n)] + [max(lat_list)]

    label_dict = {i: [] for i in range(n * n)}

    key = 0
    for i in range(n):
        for j in range(n):
            for loc in location_set.locations:
                if lon_split[i] <= loc.lon <= lon_split[i + 1] and lat_split[j] <= loc.lat <= lat_split[j + 1]:
                    label_dict[key].append(loc.gid)
            key += 1
    return label_dict


def main(pm_obj, coord_obj, **kwargs):

    # compute the number of time points in the period
    min_time, max_time = kwargs.get('min_time', '2018-01-01'), kwargs.get('max_time', '2018-02-01')
    time_list = pd.date_range(start=min_time, end=max_time, closed='left', freq='1H')

    # query all the pm locations that a certain number of observations
    pm_locations = session.query(pm_obj.gid) \
        .filter(pm_obj.timestamp >= min_time) \
        .filter(pm_obj.timestamp < max_time) \
        .group_by(pm_obj.gid).having(func.count(pm_obj.gid) > 0.01 * len(time_list)).all()
    pm_locations = [i[0] for i in pm_locations]
    print('Number of pm2.5 locations = {}.'.format(len(pm_locations)))

    # query the coordinates of the locations
    coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
    grid_coordinates = coord_df[coord_df['gid'].isin(pm_locations)]

    grid_list = list(grid_coordinates['gid'])
    coordinate_arr = grid_coordinates[['lon', 'lat']].values
    location_set = LocationSet(grid_list, coordinate_arr)

    label_dict = gen_labels_with_lon_lat(location_set)
    # if kw

    if min_time == '2018-01-01':
        train_loc, val_loc, test_loc = gen_train_val_test(label_dict, train_radio=0.6, val_radio=0.1)
    else:
        train_loc, val_loc, test_loc = gen_train_val_test(label_dict, train_radio=0.6, val_radio=0.2)

    print(len(train_loc), train_loc)
    print(len(val_loc), val_loc)
    print(len(test_loc), test_loc)

    fig, ax = plt.subplots()
    x = [location_set.location_dict[i].lon for i in train_loc]
    y = [location_set.location_dict[i].lat for i in train_loc]
    ax.scatter(x, y, c='r', label='train')

    x = [location_set.location_dict[i].lon for i in val_loc]
    y = [location_set.location_dict[i].lat for i in val_loc]
    ax.scatter(x, y, c='b', label='val')

    x = [location_set.location_dict[i].lon for i in test_loc]
    y = [location_set.location_dict[i].lat for i in test_loc]
    ax.scatter(x, y, c='g', label='test')

    plt.legend()
    plt.show()

    return sorted(train_loc), sorted(val_loc), sorted(test_loc)


if __name__ == '__main__':

    pm = LosAngeles500mGridPurpleAirPM2018
    coord = LosAngeles500mGrid

    # get the train, val, test location for January
    train, val, test = main(pm, coord, min_time='2018-01-01', max_time='2018-02-01')

    query_obj = {
        2: ['201802', '2018-02-01', '2018-03-01'],
        3: ['201803', '2018-03-01', '2018-04-01'],
        4: ['201804', '2018-04-01', '2018-05-01'],
        5: ['201805', '2018-05-01', '2018-06-01'],
        6: ['201806', '2018-06-01', '2018-07-01'],
        7: ['201807', '2018-07-01', '2018-08-01'],
        8: ['201808', '2018-08-01', '2018-09-01'],
        9: ['201809', '2018-09-01', '2018-10-01'],
        10: ['201810', '2018-10-01', '2018-11-01'],
        11: ['201811', '2018-11-01', '2018-12-01'],
        12: ['201812', '2018-12-01', '2019-01-01'],
    }

    results = {}
    for obj in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]:
        train, val, test = main(pm, coord, min_time=query_obj[obj][1], max_time=query_obj[obj][2])
        time_idx = query_obj[obj][0]
        results[time_idx] = {
            'train_loc': train,
            'val_loc': val,
            'test_loc': test
        }
    #
    # with open('data/los_angeles_500m_train_val_test.json', 'w') as f:
    #     json.dump(results, f)
