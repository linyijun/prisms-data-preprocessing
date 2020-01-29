# prisms-data-preprocessing
This repository includes all the data pre-processing scripts for the project PRISMS.

### gen_grids.py
The script is generating a grid map over the target region in Postgres.  <br />
Table __GRID__: [gid, centroid, lon, lat, geom, lon_proj, lat_proj]  <br />
```
Input parameters:
- the bounding box over the target area
- the EPSG of the target area (unit should be "metre")
- the resolution of the grid
- the grid table object
```

### gen_geo_features.py
The script is computing the values of various geographic features within each cell from OpenStreetMap.  <br />
Table __GEO_FEATURE__: [gid, feature_type, geo_feature, value, measurement] <br />
```
Input parameters:
- the bounding box over the target area (used for cropping)
- the OpenStreetMap table objects and corresponding geo features (e.g., landuses, roads)
- the grid table object
- the geo feature table object
```

### gen_geo_vector.py
The script is constructing a geo vector from the geo features.  <br />
Table __GEO_VECTOR__: [gid, data]  # data is a list  <br />
Table __GEO_NAME__: [name, geo_feature, feature_type]  <br />
```
Input parameters:
- the grid table object
- the geo feature table object
- the geo vector table object
- the geo name table object
```

### mapping_mat.py
The script is mapping the grid to a matrix (re-indexing).  <br />
An example of the output matrix:  <br />
[[6917, 6918, 6919, ..., 6990, 6991, 6992],  <br />
&nbsp;[6841, 6842, 6843, ..., 6914, 6915, 6916],  <br />
&nbsp;[6765, 6766, 6767, ..., 6838, 6839, 6840],  <br />
&nbsp;... ...,  <br />
&nbsp;[153, 154, 155, ..., 226, 227, 228],  <br />
&nbsp;[77, 78, 79, ..., 150, 151, 152],  <br />
&nbsp;[1, 2, 3, ..., 74, 75, 76]])  <br />

```
Input parameters:
- the grid table object
- the output filename  # the output would be .npz file
```

### gen_train_val_test_loc.py
The script is randomly generating training, validation, and testing locations with evenly-spatial distribution.  <br />
```
Input parameters:
- the given locations
- the number of pieces dividing the space or the number of clusterst  # extracting locations from each cluster to ensure even distribution
```

### temporal_interpolation.py
The script is interpolate the features (meteorological) across the time using linear interpolation.  <br />
Table __INTERPOLATION__: [gid, timestamp, data]  <br />
```
Input parameters:
- the old meteorological table object
- the target meteorological table object  # having the same spatial resolution as the old one
```

### spatial_interpolation.py
The script is interpolate the features (meteorological) across the space using cubic interpolation.  <br />
Table __INTERPOLATION__: [gid, timestamp, data]  <br />
```
Input parameters:
- the old grid table object
- the old meteorological table object
- the target grid table object
- the target meteorological table object  # having a finer spatial resolution than the old one
```

### main.py
The script is generating the training data including label matrix and feature matrix.  <br />
The output file contains "label_mat", "feature_mat", "feature_distribution", "geo_name", "pm_grids", "grids".  <br />
```
Input parameters:
- the air quality table object
- the meteorological table object
- the geo vector table object
- the geo name table object
- the grid table object & the mapping matrix file
- the time range
- the output filename  # the output would be .npz file
```
