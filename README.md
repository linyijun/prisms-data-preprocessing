# prisms-data-preprocessing
This repository includes all the data pre-processing scripts for the project PRISMS.

### gen_grids.py
The script is generating a grid map over the target region in Postgres. ＜/br＞

The grid table consists of generated cells, which are represented as ["gid", "centroid", "lon", "lat", "geom", "lon_proj", "lat_proj"]. ＜/br＞
You need to provide the following information: ＜/br＞
(1) A bounding box over the target area ＜/br＞
(2) EPSG of the target area ＜/br＞
(3) Required resolution of the grid ＜/br＞
(4) The grid table object in the database ＜/br＞

### gen_geo_features.py
The function is computing the values of various geographic features within each cell from OpenStreetMap.


- gen_geo_vector.py  # construct the geo features into vector format, each cell can be represented as a long vector
- mapping_mat.py  # map the grid map to a matrix (re-indexing)
- gen_train_val_test_loc.py  # randomly generate training, validation, and testing locations with evenly spatial distribution
- spatial_interpolation.py  # interpolate the features over the space using cubic interpolation
- temporal_interpolation.py  # interpolate the feature over the time using linear interpolation
= gen_training_data  # generate the training data including