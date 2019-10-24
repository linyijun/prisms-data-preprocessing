-- 
--	Los Angeles 2018 PM2.5 Grid Data Generation SQL Commands
--

-- 
-- Create table: los_angeles_purple_air_pm25_2018
-- Description: 2018 Purple Air PM2.5 data from the raw data
--
DROP TABLE IF EXISTS preprocess.los_angeles_purple_air_pm25_2018;
CREATE TABLE preprocess.los_angeles_purple_air_pm25_2018 ( 
    uid BIGSERIAL PRIMARY KEY,
    sensor_id integer NOT NULL,
    timestamp timestamp with time zone NOT NULL,
    pm25 real);
CREATE INDEX ON preprocess.los_angeles_purple_air_pm25_2018 (sensor_id);
CREATE INDEX ON preprocess.los_angeles_purple_air_pm25_2018 (timestamp);

INSERT INTO  preprocess.los_angeles_purple_air_pm25_2018
SELECT nextval('preprocess.los_angeles_purple_air_pm25_2018_uid_seq'::regclass), t.*
FROM (
SELECT c.device_id AS sensor_id, c.timestamp, c.pm25 AS pm25
FROM air_quality_data.los_angeles_purple_air_pm25_hourly_outside_2018_view c
WHERE c.timestamp >= '2018-01-01' AND c.timestamp < '2019-01-01') t;
--------------------------------------------------------------------------------------------------------------------------------------------------

-- 
-- Create table: los_angeles_purple_air_pm25_2018_sensor_locations
-- Description: 2018 Purple Air PM2.5 sensor locations
--
DROP TABLE preprocess.los_angeles_purple_air_pm25_2018_sensor_locations;
CREATE TABLE preprocess.los_angeles_purple_air_pm25_2018_sensor_locations AS
SELECT a.sensor_id AS sensor_id, b.lon, b.lat, b.location
FROM (SELECT distinct(sensor_id) FROM  preprocess.los_angeles_air_quality_201811) a,
air_quality_data.los_angeles_purple_air_outside_locations_view b
WHERE a.sensor_id = b.thingspeak_primary_id;
CREATE INDEX ON preprocess.los_angeles_purple_air_pm25_2018_sensor_locations (sensor_id);
--------------------------------------------------------------------------------------------------------------------------------------------------

-- 
-- Create table: los_angeles_1000m_grid_purple_air_pm25_2018, los_angeles_500m_grid_purple_air_pm25_2018
-- Description: 2018 Purple Air PM2.5 gridded data for the cell size of 500m and 1000m
--
DROP TABLE IF EXISTS preprocess.los_angeles_1000m_grid_purple_air_pm25_2018;
CREATE TABLE preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 AS 
SELECT d.gid AS gid, c.sensor_id AS sensor_id, c.timestamp, c.pm25
FROM preprocess.los_angeles_purple_air_pm25_2018 c, 
(SELECT a.sensor_id, b.gid 
FROM preprocess.los_angeles_purple_air_pm25_2018_sensor_locations a, geographic_data.los_angeles_1000m_grid b
WHERE ST_Contains(b.geom, a.location)) d
WHERE c.sensor_id = d.sensor_id;    
CREATE INDEX ON preprocess.los_angeles_1000m_grid_air_quality_201811 (gid);
CREATE INDEX ON preprocess.los_angeles_1000m_grid_air_quality_201811 (timestamp);

DROP TABLE IF EXISTS preprocess.los_angeles_500m_grid_purple_air_pm25_2018;
CREATE TABLE preprocess.los_angeles_500m_grid_purple_air_pm25_2018 AS 
SELECT d.gid AS gid, c.sensor_id AS sensor_id, c.timestamp, c.pm25
FROM preprocess.los_angeles_purple_air_pm25_2018 c, 
(SELECT a.sensor_id, b.gid 
FROM preprocess.los_angeles_purple_air_pm25_2018_sensor_locations a, geographic_data.los_angeles_500m_grid b
WHERE ST_Contains(b.geom, a.location)) d
WHERE c.sensor_id = d.sensor_id;    
CREATE INDEX ON preprocess.los_angeles_500m_grid_air_quality_201811 (gid);
CREATE INDEX ON preprocess.los_angeles_500m_grid_air_quality_201811 (timestamp);
--------------------------------------------------------------------------------------------------------------------------------------------------

-- 
-- Create materialized view: los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view, los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view
-- Description: Removing the sensors with too low or too high variance; Also, removing the negative and too large pm2.5 values
-- 				Taking the median of the pm2.5 values within one grid for each pair (gid, timestamp)
--
DROP MATERIALIZED VIEW IF EXISTS preprocess.los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view;
CREATE MATERIALIZED VIEW preprocess.los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view AS
SELECT a.gid, a.timestamp, median(a.pm25) as pm25 FROM

	(SELECT base.gid, base.timestamp, base.pm25
	FROM preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 base,
		(SELECT base.gid
		FROM preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 base
		GROUP BY base.gid
		HAVING variance(base.pm25) > 50.0 and variance(base.pm25) < 5000.0) var
	WHERE var.gid = base.gid) a
WHERE a.pm25 > 0.0 and a.pm25 < 500.0
GROUP BY a.gid, a.timestamp;
CREATE INDEX ON preprocess.los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view (gid);
CREATE INDEX ON preprocess.los_angeles_1000m_grid_purple_air_pm25_2018_trimmed_view (timestamp);

DROP MATERIALIZED VIEW IF EXISTS preprocess.los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view;
CREATE MATERIALIZED VIEW preprocess.los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view AS
SELECT a.gid, a.timestamp, median(a.pm25) as pm25 FROM

	(SELECT base.gid, base.timestamp, base.pm25
	FROM preprocess.los_angeles_500m_grid_purple_air_pm25_2018 base,
		(SELECT base.gid
		FROM preprocess.los_angeles_500m_grid_purple_air_pm25_2018 base
		GROUP BY base.gid
		HAVING variance(base.pm25) > 50.0 and variance(base.pm25) < 5000.0) var
	WHERE var.gid = base.gid) a
WHERE a.pm25 > 0.0 and a.pm25 < 500.0
GROUP BY a.gid, a.timestamp;
CREATE INDEX ON preprocess.los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view (gid);
CREATE INDEX ON preprocess.los_angeles_500m_grid_purple_air_pm25_2018_trimmed_view (timestamp);


