from sqlalchemy import Column, String, Float, Integer, Sequence
from geoalchemy2 import Geometry

from data_models.common_db import Base


class GridTemplate(object):
    __table_args__ = {'schema': 'geographic_data'}

    gid = Column(Integer, primary_key=True, autoincrement=True)
    centroid = Column(Geometry('POINT', srid=4326), nullable=False)
    lon = Column(Float(53), nullable=False)
    lat = Column(Float(53), nullable=False)
    geom = Column(Geometry('POLYGON', srid=4326), nullable=False)
    lon_proj = Column(Float(53), nullable=False)
    lat_proj = Column(Float(53), nullable=False)


class LosAngeles500mGrid(GridTemplate, Base):
    __tablename__ = 'los_angeles_500m_grid'


class LosAngeles1000mGrid(GridTemplate, Base):
    __tablename__ = 'los_angeles_1000m_grid'


class LosAngeles5000mGrid(GridTemplate, Base):
    __tablename__ = 'los_angeles_5000m_grid'


class SaltLakeCity500mGrid(GridTemplate, Base):
    __tablename__ = 'salt_lake_city_500m_grid'


class SaltLakeCity1000mGrid(GridTemplate, Base):
    __tablename__ = 'salt_lake_city_1000m_grid'


class SaltLakeCity5000mGrid(GridTemplate, Base):
    __tablename__ = 'salt_lake_city_5000m_grid'

