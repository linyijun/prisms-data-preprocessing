# prisms-data-preprocessing
This repository includes all the data pre-processing scripts for the project PRISMS

## python3 gen_grids.py
generate a grid map by given the bounding box, resolution, EPSG

- gen_geo_features.py  # compute the value of various geographic features from OpenStreetMap within each cell
- gen_geo_vector.py  # construct the geo features into vector format, each cell can be represented as a long vector
- mapping_mat.py  # map the grid map to a matrix (re-indexing)
- gen_train_val_test_loc.py  # randomly generate training, validation, and testing locations with evenly spatial distribution
- spatial_interpolation.py  # interpolate the features over the space using cubic interpolation
- temporal_interpolation.py  # interpolate the feature over the time using linear interpolation
= gen_training_data  # generate the training data including