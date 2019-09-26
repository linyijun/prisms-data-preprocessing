from geoalchemy2 import Geometry
from sqlalchemy import Column, Float, BigInteger, DateTime, Text, Integer

from data_models.common_db import Base


# ------------------------------------- Air Quality Data Tables Definition  ------------------------------------- #

class AirQualityTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    uid = Column(BigInteger, primary_key=True, autoincrement=True)
    gid = Column(Integer, nullable=False, index=True)
    sensor_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False, index=True)
    pm = Column(Float(53))
    source = Column(Text, nullable=False)


class LosAngeles100mGridAirQuality201811(AirQualityTemplate, Base):
    __tablename__ = 'los_angeles_100m_grid_air_quality_201811'


class LosAngeles500mGridAirQuality201811(AirQualityTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_air_quality_201811'


class LosAngeles1000mGridAirQuality201811(AirQualityTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_air_quality_201811'

# --------------------------------------------------------------------------------------------------------------- #


# ---------------------------------- Air Quality Location Table Definition  ------------------------------------- #

class LosAngelesAirQualityLocations(Base):
    __table_args__ = {'schema': 'preprocess'}
    __tablename__ = 'los_angeles_air_quality_locations'

    sensor_id = Column(Integer, primary_key=True, index=True)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    location = Column(Geometry('POINT', srid=4326), nullable=False)

# --------------------------------------------------------------------------------------------------------------- #


# ------------------------------------ Trimmed Air Quality Table Definition  ------------------------------------ #

class AirQualityTrimmedTemplate(object):
    __table_args__ = {'schema': 'preprocess'}

    gid = Column(Integer, primary_key=True, nullable=False, index=True)
    timestamp = Column(DateTime(timezone=True), primary_key=True, nullable=False, index=True)
    pm = Column(Float(53))


class LosAngeles100mGridAirQuality201811Trimmed(AirQualityTrimmedTemplate, Base):
    __tablename__ = 'los_angeles_100m_grid_air_quality_201811_trimmed'


class LosAngeles500mGridAirQuality201811Trimmed(AirQualityTrimmedTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid_air_quality_201811_trimmed'


class LosAngeles1000mGridAirQuality201811Trimmed(AirQualityTrimmedTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid_air_quality_201811_trimmed'

# --------------------------------------------------------------------------------------------------------------- #


# ---------------------------------------------- SQL Definition  ------------------------------------------------ #


"""
DROP TABLE preprocess.los_angeles_air_quality_201811;
CREATE TABLE preprocess.los_angeles_air_quality_201811 ( 
    uid BIGSERIAL PRIMARY KEY,
    sensor_id integer NOT NULL,
    timestamp timestamp with time zone NOT NULL,
    pm real,
    source text NOT NULL);
CREATE INDEX ON preprocess.los_angeles_air_quality_201811 (sensor_id);
CREATE INDEX ON preprocess.los_angeles_air_quality_201811 (timestamp);
INSERT INTO  preprocess.los_angeles_air_quality_201811
SELECT nextval('preprocess.los_angeles_air_quality_201811_uid_seq'::regclass), t.*
FROM (
SELECT a.station_id AS sensor_id, a.date_observed AS timestamp, a.concentration AS pm, 'epa' AS source
FROM air_quality_data.los_angeles_epa_air_quality_2018 a
WHERE a.parameter_name='PM2.5' AND a.date_observed >= '2018-11-05' AND a.date_observed < '2018-12-01'
UNION
SELECT c.device_id AS sensor_id, c.timestamp, c.pm25 AS pm, 'purple air' AS source
FROM air_quality_data.los_angeles_purple_air_pm25_hourly_outside_2018_view c
WHERE c.timestamp >= '2018-11-05' AND c.timestamp < '2018-12-01') t;


DROP TABLE preprocess.los_angeles_air_quality_locations;
CREATE TABLE preprocess.los_angeles_air_quality_locations AS
SELECT a.station_id AS sensor_id, a.lon, a.lat, a.location
FROM air_quality_data.los_angeles_epa_sensor_locations a
UNION
SELECT b.thingspeak_primary_id AS sensor_id, b.lon, b.lat, b.location
FROM air_quality_data.los_angeles_purple_air_outside_locations_view b;
CREATE INDEX ON preprocess.los_angeles_air_quality_locations (sensor_id);


DROP TABLE preprocess.los_angeles_1000m_grid_air_quality_201811;
CREATE TABLE preprocess.los_angeles_1000m_grid_air_quality_201811 ( 
    uid BIGSERIAL PRIMARY KEY,
    gid integer NOT NULL,
    sensor_id integer NOT NULL,
    timestamp timestamp with time zone NOT NULL,
    pm real,
    source text NOT NULL);
CREATE INDEX ON preprocess.los_angeles_1000m_grid_air_quality_201811 (gid);
CREATE INDEX ON preprocess.los_angeles_1000m_grid_air_quality_201811 (timestamp);
INSERT INTO  preprocess.los_angeles_1000m_grid_air_quality_201811
SELECT nextval('preprocess.los_angeles_1000m_grid_air_quality_201811_uid_seq'::regclass), t.* FROM (
SELECT d.gid, c.sensor_id AS sensor_id, c.timestamp, c.pm, c.source
FROM preprocess.los_angeles_air_quality_201811 c, 
(SELECT a.sensor_id, b.gid 
FROM preprocess.los_angeles_air_quality_locations a, geographic_data.los_angeles_1000m_grid b
WHERE ST_Contains(b.geom, a.location)) d
WHERE c.sensor_id = d.sensor_id) t;


DROP VIEW preprocess.los_angeles_1000m_grid_air_quality_201811_trimmed;
CREATE VIEW preprocess.los_angeles_1000m_grid_air_quality_201811_trimmed AS
(SELECT gid, timestamp, median(pm) as pm
FROM preprocess.los_angeles_1000m_grid_air_quality_201811 t
WHERE NOT EXISTS (SELECT * FROM preprocess.los_angeles_anomaly_detection_results WHERE sensor_id = t.sensor_id AND timestamp = t.timestamp)
GROUP BY (t.gid, t.timestamp));



"""