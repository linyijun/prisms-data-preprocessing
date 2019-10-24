import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import pytz
import random
from scipy.cluster.vq import kmeans2, whiten
from sqlalchemy import func

from data_models.aq_model import *
from data_models.grid_model import *
from data_models.common_db import session


# k means determine k
# distortions = []
# K = range(1, 10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(coordinates)
#     kmeanModel.fit(coordinates)
#     distortions.append(sum(np.min(cdist(coordinates, kmeanModel.cluster_centers_, 'euclidean'),
#                                   axis=1)) / coordinates.shape[0])
#     # plt.scatter(coordinates[:, 0], coordinates[:, 1], c=kmeanModel.labels_)
#     # plt.show()
#
# # Plot the elbow
# plt.plot(K, distortions, 'bx-')
# plt.xlabel('k')
# plt.ylabel('Distortion')
# plt.title('The Elbow Method showing the optimal k')
# plt.show()

# k=6

def plot(coordinates, label):
    plt.scatter(coordinates[:, 0], coordinates[:, 1], c=label)
    plt.show()


def cluster(coordinates, n_clusters):
    x, y = kmeans2(whiten(coordinates), k=n_clusters, iter=20)
    return y


def gen_train_val_test(locations, labels):
    train_radio, val_radio, test_radio = 0.6, 0.2, 0.2
    train_loc, val_loc, test_loc = [], [], []

    for n in range(len(set(labels))):
        this_locations = []
        for i, label in enumerate(labels):
            if label == n:
                this_locations.append(locations[i])
        random.shuffle(this_locations)
        n_loc = len(this_locations)
        train_loc += this_locations[: int(train_radio * n_loc)]
        val_loc += this_locations[int(train_radio * n_loc): int((train_radio + val_radio) * n_loc)]
        test_loc += this_locations[int((train_radio + val_radio) * n_loc):]

    return sorted(train_loc), sorted(val_loc), sorted(test_loc)


def main(pm_obj, coord_obj, **kwargs):

    n_clusters = kwargs.get('n_clusters', 3)
    min_time, max_time = kwargs.get('min_time', '2018-01-01'), kwargs.get('max_time', '2018-02-01')
    tz = pytz.timezone('America/Los_Angeles')
    time_list = pd.date_range(start=min_time, end=max_time, closed='left', freq='1H')
    time_list = [tz.localize(x) for x in time_list]
    print('Data from {} to {}.'.format(min_time, max_time))
    print('Number of time points = {}.'.format(len(time_list)))

    # get all the pm locations
    pm_locations = session.query(pm_obj.gid) \
        .filter(pm_obj.timestamp >= min_time) \
        .filter(pm_obj.timestamp <= max_time) \
        .group_by(pm_obj.gid).having(func.count(pm_obj.gid) > 0.01 * len(time_list)).all()
    pm_locations = sorted([loc[0] for loc in pm_locations])
    print('Number of pm2.5 locations = {}.'.format(len(pm_locations)))

    # get all the grid locations
    coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
    pm_location_coord = coord_df[coord_df['gid'].isin(pm_locations)]

    locations = list(pm_location_coord['gid'])
    coordinates = np.array(pm_location_coord)[:, 1:]
    cluster_labels = cluster(coordinates, n_clusters)
    train_loc, val_loc, test_loc = gen_train_val_test(locations, cluster_labels)
    print(len(train_loc), train_loc)
    print(len(val_loc), val_loc)
    print(len(test_loc), test_loc)

    rows = pm_location_coord
    plt.scatter(rows['lon'], rows['lat'])
    plt.show()

    for s in [train_loc, val_loc, test_loc]:
        rows = pm_location_coord[pm_location_coord['gid'].isin(s)]
        plt.scatter(rows['lon'], rows['lat'])
        plt.show()


if __name__ == '__main__':

    pm = LosAngeles500mGridPurpleAirPM2018Trimmed
    coord = LosAngeles500mGrid
    main(pm, coord, min_time='2018-02-01', max_time='2018-03-01')

