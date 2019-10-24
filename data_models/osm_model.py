from sqlalchemy import Column, Integer, String, Numeric
from geoalchemy2 import Geometry

from data_models.common_db import Base


class OsmTemplate(object):
    __table_args__ = {'schema': 'openstreetmap'}

    ogc_fid = Column(Integer, nullable=False, primary_key=True)
    osm_id = Column(String(10), nullable=True)
    code = Column(Numeric(4), nullable=True)
    fclass = Column(String(20), nullable=True)
    name = Column(String(100), nullable=True)


class ChinaOsmBuildingA(OsmTemplate, Base):
    __tablename__ = 'china_osm_buildings_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)
    type = Column(String(20), nullable=True)


class ChinaOsmLanduseA(OsmTemplate, Base):
    __tablename__ = 'china_osm_landuse_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmNatural(OsmTemplate, Base):
    __tablename__ = 'china_osm_natural'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmNaturalA(OsmTemplate, Base):
    __tablename__ = 'china_osm_natural_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmPlaces(OsmTemplate, Base):
    __tablename__ = 'china_osm_places'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmPlacesA(OsmTemplate, Base):
    __tablename__ = 'china_osm_places_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmPofw(OsmTemplate, Base):
    __tablename__ = 'china_osm_pofw'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmPofwA(OsmTemplate, Base):
    __tablename__ = 'china_osm_pofw_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmPois(OsmTemplate, Base):
    __tablename__ = 'china_osm_pois'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmPoisA(OsmTemplate, Base):
    __tablename__ = 'china_osm_pois_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmRailways(OsmTemplate, Base):
    __tablename__ = 'china_osm_railways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class ChinaOsmRoads(OsmTemplate, Base):
    __tablename__ = 'china_osm_roads'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class ChinaOsmTraffic(OsmTemplate, Base):
    __tablename__ = 'china_osm_traffic'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmTrafficA(OsmTemplate, Base):
    __tablename__ = 'china_osm_traffic_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmTransport(OsmTemplate, Base):
    __tablename__ = 'china_osm_transport'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class ChinaOsmTransportA(OsmTemplate, Base):
    __tablename__ = 'china_osm_transport_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmWaterA(OsmTemplate, Base):
    __tablename__ = 'china_osm_water_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class ChinaOsmWaterway(OsmTemplate, Base):
    __tablename__ = 'china_osm_waterways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class CaliforniaOsmBuildingA(OsmTemplate, Base):
    __tablename__ = 'california_osm_buildings_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)
    type = Column(String(20), nullable=True)


class CaliforniaOsmLanduseA(OsmTemplate, Base):
    __tablename__ = 'california_osm_landuse_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmNatural(OsmTemplate, Base):
    __tablename__ = 'california_osm_natural'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmNaturalA(OsmTemplate, Base):
    __tablename__ = 'california_osm_natural_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmPlaces(OsmTemplate, Base):
    __tablename__ = 'california_osm_places'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmPlacesA(OsmTemplate, Base):
    __tablename__ = 'california_osm_places_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmPofw(OsmTemplate, Base):
    __tablename__ = 'california_osm_pofw'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmPofwA(OsmTemplate, Base):
    __tablename__ = 'california_osm_pofw_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmPois(OsmTemplate, Base):
    __tablename__ = 'california_osm_pois'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmPoisA(OsmTemplate, Base):
    __tablename__ = 'california_osm_pois_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmRailways(OsmTemplate, Base):
    __tablename__ = 'california_osm_railways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class CaliforniaOsmRoads(OsmTemplate, Base):
    __tablename__ = 'california_osm_roads'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class CaliforniaOsmTraffic(OsmTemplate, Base):
    __tablename__ = 'california_osm_traffic'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmTrafficA(OsmTemplate, Base):
    __tablename__ = 'california_osm_traffic_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmTransport(OsmTemplate, Base):
    __tablename__ = 'california_osm_transport'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class CaliforniaOsmTransportA(OsmTemplate, Base):
    __tablename__ = 'california_osm_transport_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmWaterA(OsmTemplate, Base):
    __tablename__ = 'california_osm_water_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class CaliforniaOsmWaterway(OsmTemplate, Base):
    __tablename__ = 'california_osm_waterways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class UtahOsmBuildingA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_buildings_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)
    type = Column(String(20), nullable=True)


class UtahOsmLanduseA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_landuse_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmNatural(OsmTemplate, Base):
    __tablename__ = 'utah_osm_natural'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmNaturalA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_natural_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmPlaces(OsmTemplate, Base):
    __tablename__ = 'utah_osm_places'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmPlacesA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_places_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmPofw(OsmTemplate, Base):
    __tablename__ = 'utah_osm_pofw'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmPofwA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_pofw_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmPois(OsmTemplate, Base):
    __tablename__ = 'utah_osm_pois'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmPoisA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_pois_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmRailways(OsmTemplate, Base):
    __tablename__ = 'utah_osm_railways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class UtahOsmRoads(OsmTemplate, Base):
    __tablename__ = 'utah_osm_roads'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


class UtahOsmTraffic(OsmTemplate, Base):
    __tablename__ = 'utah_osm_traffic'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmTrafficA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_traffic_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmTransport(OsmTemplate, Base):
    __tablename__ = 'utah_osm_transport'
    wkb_geometry = Column(Geometry(geometry_type='POINT', srid=4326), nullable=True)


class UtahOsmTransportA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_transport_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmWaterA(OsmTemplate, Base):
    __tablename__ = 'utah_osm_water_a'
    wkb_geometry = Column(Geometry(geometry_type='MULTIPOLYGON', srid=4326), nullable=True)


class UtahOsmWaterway(OsmTemplate, Base):
    __tablename__ = 'utah_osm_waterways'
    wkb_geometry = Column(Geometry(geometry_type='MULTILINESTRING', srid=4326), nullable=True)


