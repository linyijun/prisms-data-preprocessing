import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt


### Read files

epa_pm_data = pd.read_csv('/Users/yijunlin/Research/PRISMS/data/los_angeles_epa_1105_1201.csv')
ppa_pm_data = pd.read_csv('/Users/yijunlin/Research/PRISMS/data/los_angeles_ppa_1105_1201.csv')

epa_sensors = epa_pm_data[['sid', 'lon', 'lat']].drop_duplicates()
ppa_sensors = ppa_pm_data[['sid', 'lon', 'lat']].drop_duplicates()

distance_dict = {}


def physical_dis(coord1, coord2):

    lat1, lon1 = coord1
    lat2, lon2 = coord2
    radius = 6371 # km

    dlat = math.radians(lat2-lat1)
    dlon = math.radians(lon2-lon1)
    a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1)) \
        * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c

    return d


# for i, s_1 in epa_sensors.iterrows():
#     epa_sid = s_1['sid']
#     epa_coord = (s_1['lon'], s_1['lat'])
#     min_distance, min_sid = -1, -1
#
#     for j, s_2 in ppa_sensors.iterrows():
#         ppa_sid = s_2['sid']
#         ppa_coord = (s_2['lon'], s_2['lat'])
#         dis = physical_dis(epa_coord, ppa_coord)
#         if dis < min_distance or min_distance == -1:
#             min_distance = dis
#             min_sid = ppa_sid
#
#     distance_dict[int(epa_sid)] = [int(min_sid), min_distance]


for i, s_1 in ppa_sensors.iterrows():
    this_ppa_sid = s_1['sid']
    this_ppa_coord = (s_1['lon'], s_1['lat'])
    min_distance, min_sid = -1, -1

    for j, s_2 in ppa_sensors.iterrows():
        ppa_sid = s_2['sid']

        if this_ppa_sid == ppa_sid:
            continue

        ppa_coord = (s_2['lon'], s_2['lat'])
        dis = physical_dis(this_ppa_coord, ppa_coord)
        if dis < min_distance or min_distance == -1:
            min_distance = dis
            min_sid = ppa_sid

    distance_dict[int(this_ppa_sid)] = [int(min_sid), min_distance]


def plotting(x, y):

    plt.scatter(x, y, s=7, c='r', edgecolors='none')
    plt.title('PM2.5 Concentrations in Nov. 2018, Los Angeles')
    plt.xlabel('EPA Values')
    plt.ylabel('PurpleAir Values')

    fit = np.polyfit(x, y, 1)
    fit_fn = np.poly1d(fit)
    plt.plot(x, fit_fn(x), '--k')
    plt.show()


# for sid_1, sid_2 in distance_dict.items():
#     if sid_2[1] < 0.5:
#         print(sid_2[1])
#         this_epa_pm_data = epa_pm_data[epa_pm_data['sid'] == sid_1]
#         this_ppa_pm_data = ppa_pm_data[ppa_pm_data['sid'] == sid_2[0]]
#         all_data = this_epa_pm_data.merge(this_ppa_pm_data, on='timestamp')
#         all_data = all_data.sort_values('timestamp')
#         x = np.array(all_data['pm_x'])
#         y = np.array(all_data['pm_y'])
#         plotting(x, y)

        # log_x = np.log(x)
        # log_y = np.log(y)
        # plotting(log_x, log_y)


for sid_1, sid_2 in distance_dict.items():
    if sid_2[1] < 0.5:
        print(sid_2[1])
        this_epa_pm_data = epa_pm_data[epa_pm_data['sid'] == sid_1]
        this_ppa_pm_data = ppa_pm_data[ppa_pm_data['sid'] == sid_2[0]]
        all_data = this_epa_pm_data.merge(this_ppa_pm_data, on='timestamp')
        all_data = all_data.sort_values('timestamp')
        x = np.array(all_data['pm_x'])
        y = np.array(all_data['pm_y'])
        plotting(x, y)
