from sqlalchemy import Column, BigInteger, DateTime, REAL, Text, Integer, ARRAY

from data_models.common_db import Base


# ----------------------------------------- DarkSky Tables Definition ----------------------------------------- #

class DarkSkyTemplate(object):
    __table_args__ = {'schema': 'auxiliary_data'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)
    summary = Column(Text)
    icon = Column(Text)
    precip_intensity = Column(REAL)
    precip_probability = Column(REAL)
    temperature = Column(REAL)
    apparent_temperature = Column(REAL)
    dew_point = Column(REAL)
    humidity = Column(REAL)
    pressure = Column(REAL)
    wind_speed = Column(REAL)
    wind_bearing = Column(REAL)
    cloud_cover = Column(REAL)
    uv_index = Column(REAL)
    visibility = Column(REAL)
    ozone = Column(REAL)


class LosAngeles5000mGridMeoDarkSky201811(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201811'


class SaltLakeCity5000mGridMeoDarkSky201703201803(DarkSkyTemplate, Base):
    __tablename__ = 'salt_lake_city_5000m_grid_meo_darksky_201703_201803'

# --------------------------------------------------------------------------------------------------------------- #


# --------------------------------------- Interpolation Tables Definition --------------------------------------- #

class DarkSkyInterpolateTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    uid = Column(BigInteger, nullable=False, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    data = Column(ARRAY(REAL), nullable=False)


class LosAngeles500mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201811'


class LosAngeles1000mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201811'


class LosAngeles5000mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201811'


class SaltLakeCity500mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_500m_grid_meo_darksky_interpolate_201703_201803'


class SaltLakeCity1000mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_1000m_grid_meo_darksky_interpolate_201703_201803'


class SaltLakeCity5000mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_5000m_grid_meo_darksky_interpolate_201703_201803'

# --------------------------------------------------------------------------------------------------------------- #


