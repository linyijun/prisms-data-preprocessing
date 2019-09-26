import numpy as np
import pandas as pd
import os
import copy
import matplotlib.pyplot as plt
import folium
import geopandas as gpd
import random
from shapely.wkt import loads
from scipy.cluster.vq import kmeans2, whiten
from scipy.spatial.distance import cdist
from sklearn.cluster import KMeans


from data_models.aq_model import *
from data_models.grid_model import *
from data_models.common_db import session

pm_obj = LosAngeles500mGridAirQuality201811Trimmed
coord_obj = LosAngeles500mGrid


# get all the pm locations

pm_locations = session.query(pm_obj.gid).distinct().all()
pm_locations = [loc[0] for loc in pm_locations]

# get all the grid locations

coord_df = pd.read_sql(session.query(coord_obj.gid, coord_obj.lon, coord_obj.lat).statement, session.bind)
pm_location_coord = coord_df[coord_df['gid'].isin(pm_locations)]



def plot_base_map(coord_df, zoom_start=11):
    min_lat, max_lat = min(coord_df['lat']), max(coord_df['lat'])
    min_lon, max_lon = min(coord_df['lon']), max(coord_df['lon'])
    start_lat, start_lon = (min_lat + max_lat) / 2, (min_lon + max_lon) / 2
    m = folium.Map(location=[start_lat, start_lon], zoom_start=zoom_start)
    return m

def convert_df_to_geo_df(data):
    geo_data = copy.copy(data)
    geo_data['geom'] = geo_data['geom'].apply(lambda x: loads(x))
    geo_data  = gpd.GeoDataFrame(geo_data, geometry='geom')
    geo_data.crs = {'init': 'epsg:4326'}
    return geo_data


coordinates = np.array(pm_location_coord)[:, 1:]

# k means determine k
# distortions = []
# K = range(1, 10)
# for k in K:
#     kmeanModel = KMeans(n_clusters=k).fit(coordinates)
#     kmeanModel.fit(coordinates)
#     distortions.append(sum(np.min(cdist(coordinates, kmeanModel.cluster_centers_, 'euclidean'), axis=1)) / coordinates.shape[0])
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
x, y = kmeans2(whiten(coordinates), 6, iter=20)
plt.scatter(coordinates[:, 0], coordinates[:, 1], c=y)
plt.show()

labels = np.stack([np.array(pm_location_coord['gid']).astype(int), y], axis=1)
labels = pd.DataFrame(labels, columns=['gid', 'label'])
train_loc = []
val_loc = []
test_loc = []

train_radio = 0.6
val_radio = 0.2
test_radio = 0.2

for i in range(6):
    this_df = labels[labels['label'] == i]
    locations_copy = copy.copy(list(this_df['gid']))
    random.shuffle(locations_copy)

    this_train_loc = locations_copy[: int(train_radio * len(locations_copy))]
    this_val_loc = locations_copy[int(train_radio * len(locations_copy)):int((train_radio + val_radio) * len(locations_copy))]
    this_test_loc = locations_copy[int((train_radio + val_radio) * len(locations_copy)):]
    train_loc += this_train_loc
    val_loc += this_val_loc
    test_loc += this_test_loc

train_loc = sorted(train_loc)
val_loc = sorted(val_loc)
test_loc = sorted(test_loc)
print(train_loc)
print(val_loc)
print(test_loc)

for s in [train_loc, val_loc, test_loc]:
    rows = pm_location_coord[pm_location_coord['gid'].isin(s)]
    plt.scatter(rows['lon'], rows['lat'])
    plt.show()
