import sqlalchemy as sa
from sqlalchemy.schema import MetaData, Column, Table, ForeignKey
from sqlalchemy.types import Integer, String

metadata = MetaData()

ontologies = Table(
    'ontologies', metadata,
    Column('id', Integer, primary_key=True),
    Column('ontology', String, nullable=False),
    Column('class_id', String, nullable=False),
    Column('cui', String),
    Column('preferred_label', String),
    Column('definitions', String),
    Column('obsolete', String)
)

parents = Table(
    'parents', metadata,
    Column('id', Integer, primary_key=True),
    Column('ontology_id', Integer, ForeignKey('ontologies.id')),
    Column('parent', Integer, ForeignKey('ontologies.id'))
)

synonyms = Table(
    'synonyms', metadata,
    Column('id', Integer, primary_key=True),
    Column('ontology_id', Integer, ForeignKey('ontologies.id'), index=True),
    Column('synonym', String, index=True)
)

semantic_types = Table(
    'semantic_types', metadata,
    Column('id', Integer, primary_key=True),
    Column('ontology_id', Integer, ForeignKey('ontologies.id'), index=True),
    Column('semantic_type', String, index=True)
)


def create_db(url):
    engine = sa.create_engine(url)
    metadata.drop_all(engine)
    metadata.create_all(engine)
