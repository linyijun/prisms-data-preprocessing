from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, BigInteger, DateTime, Text, Integer

from data_models.common_db import Base


# ------------------------------------- Air Quality Data Tables Definition  ------------------------------------- #

class AirQualityTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    gid = Column(Integer, primary_key=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), primary_key=True, nullable=False, index=True)
    pm25 = Column(Float(53))


class LosAngeles500mGridPurpleAirPM2018(AirQualityTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_purple_air_pm25_2018'


class LosAngeles1000mGridPurpleAirPM2018(AirQualityTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_purple_air_pm25_2018'

# --------------------------------------------------------------------------------------------------------------- #


# ---------------------------------- Air Quality Location Table Definition  ------------------------------------- #

class LosAngelesAirQualityLocations(Base):
    __table_args__ = {'schema': 'preprocess'}
    __tablename__ = 'los_angeles_purple_air_pm25_2018_sensor_locations'

    sensor_id = Column(Integer, primary_key=True, index=True)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)

# --------------------------------------------------------------------------------------------------------------- #


# # ------------------------------------ Trimmed Air Quality Table Definition  ------------------------------------ #
#
# class AirQualityTrimmedTemplate(object):
#     __table_args__ = {'schema': 'preprocess'}
#
#     gid = Column(Integer, primary_key=True, nullable=False, index=True)
#     timestamp = Column(DateTime(timezone=True), primary_key=True, nullable=False, index=True)
#     pm25 = Column(Float(53))
#
#
# class LosAngeles500mGridPurpleAirPM2018Trimmed(AirQualityTrimmedTemplate, Base):
#     __tablename__ = 'los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view'
#
#
# class LosAngeles1000mGridPurpleAirPM2018Trimmed(AirQualityTrimmedTemplate, Base):
#     __tablename__ = 'los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view'
#
# # --------------------------------------------------------------------------------------------------------------- #
