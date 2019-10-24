# prisms-data-preprocessing
This repository includes all the data pre-processing scripts for the project PRISMS.

### gen_grids.py
------
The script is generating a grid map over the target region in Postgres.
```
Input parameters:
- the bounding box over the target area
- the EPSG of the target area (unit should be "metre")
- the resolution of the grid
- the grid table object

Generating a grid table with cells as [gid, centroid, lon, lat, geom, lon_proj, lat_proj].
```

### gen_geo_features.py
------
The script is computing the values of various geographic features within each cell from OpenStreetMap.
The geo feature table: [gid, feature_type, geo_feature, value, measurement]
```
Input parameters:
- the bounding box over the target area (used for cropping)
- the OpenStreetMap table objects and corresponding geo features (e.g., landuses, roads)
- the grid table object
- the geo feature table object
```
------


- gen_geo_vector.py  # construct the geo features into vector format, each cell can be represented as a long vector
------

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
