from sqlalchemy import Column, BigInteger, DateTime, REAL, Text, Integer, ARRAY

from data_models.common_db import Base


# ----------------------------------------- DarkSky Tables Definition ----------------------------------------- #

class DarkSkyTemplate(object):
    __table_args__ = {'schema': 'meo_darksky'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
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


class LosAngeles5000mGridMeoDarkSky201801(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201801'


class LosAngeles5000mGridMeoDarkSky201802(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201802'


class LosAngeles5000mGridMeoDarkSky201803(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201803'


class LosAngeles5000mGridMeoDarkSky201804(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201804'


class LosAngeles5000mGridMeoDarkSky201805(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201805'


class LosAngeles5000mGridMeoDarkSky201806(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201806'


class LosAngeles5000mGridMeoDarkSky201807(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201807'


class LosAngeles5000mGridMeoDarkSky201808(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201808'


class LosAngeles5000mGridMeoDarkSky201809(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201809'


class LosAngeles5000mGridMeoDarkSky201810(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201810'


class LosAngeles5000mGridMeoDarkSky201811(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201811'


class LosAngeles5000mGridMeoDarkSky201812(DarkSkyTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_201812'


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


class LosAngeles500mGridMeoDarkSkyInterpolate201801(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201801'


class LosAngeles500mGridMeoDarkSkyInterpolate201802(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201802'


class LosAngeles500mGridMeoDarkSkyInterpolate201803(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201803'


class LosAngeles500mGridMeoDarkSkyInterpolate201804(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201804'


class LosAngeles500mGridMeoDarkSkyInterpolate201805(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201805'


class LosAngeles500mGridMeoDarkSkyInterpolate201806(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201806'


class LosAngeles500mGridMeoDarkSkyInterpolate201807(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201807'


class LosAngeles500mGridMeoDarkSkyInterpolate201808(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201808'


class LosAngeles500mGridMeoDarkSkyInterpolate201809(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201809'


class LosAngeles500mGridMeoDarkSkyInterpolate201810(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201810'


class LosAngeles500mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201811'


class LosAngeles500mGridMeoDarkSkyInterpolate201812(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_meo_darksky_interpolate_201812'

# -------------------------------------------------------------------------------------- #


class LosAngeles1000mGridMeoDarkSkyInterpolate201801(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201801'


class LosAngeles1000mGridMeoDarkSkyInterpolate201802(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201802'


class LosAngeles1000mGridMeoDarkSkyInterpolate201803(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201803'


class LosAngeles1000mGridMeoDarkSkyInterpolate201804(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201804'


class LosAngeles1000mGridMeoDarkSkyInterpolate201805(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201805'


class LosAngeles1000mGridMeoDarkSkyInterpolate201806(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201806'


class LosAngeles1000mGridMeoDarkSkyInterpolate201807(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201807'


class LosAngeles1000mGridMeoDarkSkyInterpolate201808(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201808'


class LosAngeles1000mGridMeoDarkSkyInterpolate201809(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201809'


class LosAngeles1000mGridMeoDarkSkyInterpolate201810(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201810'


class LosAngeles1000mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201811'


class LosAngeles1000mGridMeoDarkSkyInterpolate201812(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_meo_darksky_interpolate_201812'


# -------------------------------------------------------------------------------------- #


class LosAngeles5000mGridMeoDarkSkyInterpolate201801(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201801'


class LosAngeles5000mGridMeoDarkSkyInterpolate201802(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201802'


class LosAngeles5000mGridMeoDarkSkyInterpolate201803(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201803'


class LosAngeles5000mGridMeoDarkSkyInterpolate201804(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201804'


class LosAngeles5000mGridMeoDarkSkyInterpolate201805(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201805'


class LosAngeles5000mGridMeoDarkSkyInterpolate201806(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201806'


class LosAngeles5000mGridMeoDarkSkyInterpolate201807(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201807'


class LosAngeles5000mGridMeoDarkSkyInterpolate201808(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201808'


class LosAngeles5000mGridMeoDarkSkyInterpolate201809(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201809'


class LosAngeles5000mGridMeoDarkSkyInterpolate201810(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201810'


class LosAngeles5000mGridMeoDarkSkyInterpolate201811(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201811'


class LosAngeles5000mGridMeoDarkSkyInterpolate201812(DarkSkyInterpolateTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid_meo_darksky_interpolate_201812'


# -------------------------------------------------------------------------------------- #


class SaltLakeCity500mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_500m_grid_meo_darksky_interpolate_201703_201803'


class SaltLakeCity1000mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_1000m_grid_meo_darksky_interpolate_201703_201803'


class SaltLakeCity5000mGridMeoDarkSkyInterpolate201703201803(DarkSkyInterpolateTemplate, Base):
    __table_args__ = {'schema': 'preprocess2'}
    __tablename__ = 'salt_lake_city_5000m_grid_meo_darksky_interpolate_201703_201803'



