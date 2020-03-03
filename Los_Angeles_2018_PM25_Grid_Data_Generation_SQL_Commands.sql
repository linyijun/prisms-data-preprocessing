-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --
--	Los Angeles Purple Air 2018 PM2.5 Data Generation SQL Commands   --
-- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- -- --

-- 
-- Create table: preprocess.los_angeles_purple_air_pm25_2018
-- Description: select 2018 Purple Air PM2.5 data from the raw data, merge channel a and b by taking average
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
SELECT nextval('preprocess.los_angeles_purple_air_pm25_2018_uid_seq'::regclass), t.sensor_id, t.timestamp, (t.pm25_a + t.pm25_b) / 2 as pm25
FROM (
SELECT m.sensor_id, m.timestamp, m.pm25_a, n.pm25_b, abs(pm25_a-pm25_b) as diff
FROM
-- select pm2.5 from channel a
(SELECT b.parent_id AS sensor_id, a.timestamp, a.pm2_5_atm as pm25_a
FROM purple_air.los_angeles_purple_air_hourly_2018 a, purple_air.purple_air_locations b
WHERE a.sensor_id = b.sensor_id and a.pm2_5_atm > 0 and a.pm2_5_atm is not NULL and a.channel='a') m,
-- select pm2.5 from channel b
(SELECT b.parent_id AS sensor_id, a.timestamp, a.pm2_5_atm as pm25_b
FROM purple_air.los_angeles_purple_air_hourly_2018 a, purple_air.purple_air_locations b
WHERE a.sensor_id = b.sensor_id and a.pm2_5_atm > 0 and a.pm2_5_atm is not NULL and a.channel='b') n
WHERE m.sensor_id = n.sensor_id and m.timestamp = n.timestamp) t
-- filter out the instances that channel a and b are very different; need to decide a proper threshold
WHERE diff < 10;
-------------------------------------------------------------------------------------------------------------------------------------------------

-- 
-- Create table: preprocess.los_angeles_purple_air_pm25_2018_sensor_locations
-- Description: 2018 Purple Air PM2.5 sensor locations
--
DROP TABLE IF EXISTS preprocess.los_angeles_purple_air_pm25_2018_sensor_locations;
CREATE TABLE preprocess.los_angeles_purple_air_pm25_2018_sensor_locations AS
SELECT DISTINCT(a.sensor_id) AS sensor_id, b.lon, b.lat, b.location
FROM (SELECT DISTINCT(sensor_id) FROM  preprocess.los_angeles_purple_air_pm25_2018) a, purple_air.purple_air_locations b
WHERE a.sensor_id = b.parent_id;
CREATE INDEX ON preprocess.los_angeles_purple_air_pm25_2018_sensor_locations (sensor_id);
-------------------------------------------------------------------------------------------------------------------------------------------------

-- 
-- Create table: los_angeles_1000m_grid_purple_air_pm25_2018, los_angeles_500m_grid_purple_air_pm25_2018
-- Description: 2018 Purple Air PM2.5 gridded data for the cell size of 500m and 1000m
--
DROP TABLE IF EXISTS preprocess.los_angeles_1000m_grid_purple_air_pm25_2018;
CREATE TABLE preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 AS 
SELECT d.gid AS gid, c.timestamp, median(c.pm25) as pm25
FROM preprocess.los_angeles_purple_air_pm25_2018 c,
(SELECT a.sensor_id, b.gid
FROM preprocess.los_angeles_purple_air_pm25_2018_sensor_locations a, geographic_data.los_angeles_1000m_grid b
WHERE ST_Contains(b.geom, a.location)) d
WHERE c.sensor_id = d.sensor_id
GROUP BY d.gid, c.timestamp;
CREATE INDEX ON preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 (gid);
CREATE INDEX ON preprocess.los_angeles_1000m_grid_purple_air_pm25_2018 (timestamp);

DROP TABLE IF EXISTS preprocess.los_angeles_500m_grid_purple_air_pm25_2018;
CREATE TABLE preprocess.los_angeles_500m_grid_purple_air_pm25_2018 AS
SELECT d.gid AS gid, c.timestamp, median(c.pm25) as pm25
FROM preprocess.los_angeles_purple_air_pm25_2018 c,
(SELECT a.sensor_id, b.gid
FROM preprocess.los_angeles_purple_air_pm25_2018_sensor_locations a, geographic_data.los_angeles_500m_grid b
WHERE ST_Contains(b.geom, a.location)) d
WHERE c.sensor_id = d.sensor_id
GROUP BY d.gid, c.timestamp;
CREATE INDEX ON preprocess.los_angeles_500m_grid_purple_air_pm25_2018 (gid);
CREATE INDEX ON preprocess.los_angeles_500m_grid_purple_air_pm25_2018 (timestamp);
--------------------------------------------------------------------------------------------------------------------------------------------------
