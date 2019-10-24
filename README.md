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
Table __GEO_VECTOR__: [gid, data] # data is like a list  <br />
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
E.g., mat = array([[6917, 6918, 6919, ..., 6990, 6991, 6992],  <br />
                   [6841, 6842, 6843, ..., 6914, 6915, 6916],  <br />
                   [6765, 6766, 6767, ..., 6838, 6839, 6840],  <br />
                     ... ...,  <br />
                   [153, 154, 155, ..., 226, 227, 228],  <br />
                   [77, 78, 79, ..., 150, 151, 152],  <br />
                   [1, 2, 3, ..., 74, 75, 76]])  <br />

```
Input parameters:
- the grid table object
- the output filename # the output would be .npz file
```

- mapping_mat.py  # map the grid map to a matrix (re-indexing)
------

- gen_train_val_test_loc.py  # randomly generate training, validation, and testing locations with evenly spatial distribution
------

- spatial_interpolation.py  # interpolate the features over the space using cubic interpolation
------

- temporal_interpolation.py  # interpolate the feature over the time using linear interpolation
------

= gen_training_data  # generate the training data including
------
