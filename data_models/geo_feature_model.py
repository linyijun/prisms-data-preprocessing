from sqlalchemy import Column, BigInteger, Integer, String, Float, Text, REAL, ARRAY

from data_models.common_db import Base


# ---------------------------------------- Geo Feature Tables Definition ---------------------------------------- #

class GeoFeatureTemplate(object):
    __table_args__ = {'schema': 'geographic_data'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False)
    geo_feature = Column(Text, nullable=False)
    feature_type = Column(Text, nullable=False)
    value = Column(Float(53), nullable=False)
    measurement = Column(Text, nullable=False)


class LosAngeles500mGridGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_geo_feature'


class LosAngeles1000mGridGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_geo_feature'


class SaltLakeCity500mGridGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'salt_lake_city_500m_grid_geo_feature'


class SaltLakeCity1000mGridGeoFeature(GeoFeatureTemplate, Base):
    __tablename__ = 'salt_lake_city_1000m_grid_geo_feature'

# --------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------- Geo Vector Tables Definition  ---------------------------------------- #

class GeoVectorTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    uid = Column(BigInteger, nullable=False, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False, index=True)
    data = Column(ARRAY(REAL), nullable=False)


class LosAngeles500mGridGeoVector(GeoVectorTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_geo_vector'


class LosAngeles1000mGridGeoVector(GeoVectorTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_geo_vector'


class SaltLakeCity500mGridGeoVector(GeoVectorTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_500m_grid_geo_vector'


class SaltLakeCity1000mGridGeoVector(GeoVectorTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_1000m_grid_geo_vector'

# --------------------------------------------------------------------------------------------------------------- #


# ----------------------------------------   Geo Name Tables Definition  ---------------------------------------- #

class GeoNameTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    uid = Column(BigInteger, nullable=False, primary_key=True, autoincrement=True)
    name = Column(Text, nullable=False)
    geo_feature = Column(Text, nullable=False)
    feature_type = Column(Text, nullable=False)


class LosAngeles500mGridGeoName(GeoNameTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_geo_name'


class LosAngeles1000mGridGeoName(GeoNameTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_geo_name'


class SaltLakeCity500mGridGeoName(GeoNameTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_500m_grid_geo_name'


class SaltLakeCity1000mGridGeoName(GeoNameTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_1000m_grid_geo_name'

# --------------------------------------------------------------------------------------------------------------- #

