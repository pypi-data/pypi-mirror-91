import requests
import gzip
import csv
import os
from databases import Database
import asyncio

from .db.models import (ontologies, parents, create_db,
                        synonyms, metadata, semantic_types)


database_url = 'postgresql://sdavis2@localhost/sdavis2'
database = Database(database_url)


def ontology_csv(ontology):
    custom_header = {'Accept-Encoding': 'gzip'}
    r = requests.get(
        f'http://data.bioontology.org/ontologies/{ontology}/'
        'download?apikey=8b5b7825-538d-40e0-9e9e-5ab9274a9aeb'
        '&download_format=csv',
        headers=custom_header,
        stream=True)
    # r.raw.decode_content = True
    try:
        f = gzip.GzipFile(fileobj=r.raw)
    except Exception:
        f = r.raw
    reader = csv.DictReader(line.decode('UTF-8') for line in f)
    reader.fieldnames = list(
        [n.lower().replace(' ', '_') for n in reader.fieldnames])
    for row in reader:
        row['synonyms'] = [st.strip('"') for st in row['synonyms'].split('|')]
        row['semantic_types'] = [st.strip('"')
                                 for st in row['semantic_types'].split('|')]
        row['parents'] = [st.strip('"') for st in row['parents'].split('|')]
        x = dict()
        for idx, key in enumerate(row.keys()):
            x['ontology'] = ontology
            if 0 <= idx < 8:
                if (row[key] == ''):
                    x[key] = None
                else:
                    x[key] = row[key]
                if (row[key] == ['']):
                    x[key] = []
        yield (x)


def get_all_ontology_short_ids():
    import yaml
    yaml_string = requests.get(
        'https://raw.githubusercontent.com/OBOFoundry/'
        'OBOFoundry.github.io/master/_config.yml'
    )
    val = yaml.load(yaml_string.content)
    x = []
    for onto in val['ontologies']:
        x.append(onto['id'].upper())
    return (x)


async def create_onto_table():
    await database.connect()
    # Create a table.
    await database.execute(query='DROP table ontologies CASCADE;')
    await database.execute(query='DROP table parents CASCADE;')
    await database.execute(query='DROP table synonyms CASCADE;')
    await database.execute(query='DROP table semantic_types CASCADE;')

    query = """
    CREATE TABLE ontologies (id SERIAL PRIMARY KEY,
        ontology varchar,
        class_id varchar,
        preferred_label varchar,
        definitions varchar,
        obsolete varchar,
        cui varchar)
    """
    await database.execute(query=query)
    query = """CREATE index ontologies_ontology_class on ontologies(ontology, class_id)"""
    await database.execute(query=query)
    query = """
    CREATE TABLE parents (id SERIAL PRIMARY KEY,
        ontology_id INTEGER references ontologies (id),
        parent varchar
    )"""
    await database.execute(query=query)
    query = """
    CREATE TABLE synonyms (id SERIAL PRIMARY KEY,
        ontology_id INTEGER references ontologies (id),
        synonym varchar
    )"""
    await database.execute(query=query)
    query = """
    CREATE TABLE semantic_types (id SERIAL PRIMARY KEY,
        ontology_id INTEGER references ontologies (id),
        semantic_type varchar
    )"""
    await database.execute(query=query)
    await database.disconnect()


async def main(vals):
    await database.connect()
    # Create a table.

# WITH data(firstname, lastname, adddetails, value) AS (
#    VALUES                              -- provide data here
#       ('fai55', 'shaggk', 'ss', 'ss2') -- see below
#     , ('fai56', 'XXaggk', 'xx', 'xx2') -- works for multiple input rows
#        --  more?
#    )
# , ins1 AS (
#    INSERT INTO sample (firstname, lastname)
#    SELECT firstname, lastname          -- DISTINCT? see below
#    FROM   data
#    -- ON     CONFLICT DO NOTHING       -- UNIQUE constraint? see below
#    RETURNING firstname, lastname, id AS sample_id
#    )
# , ins2 AS (
#    INSERT INTO sample1 (sample_id, adddetails)
#    SELECT ins1.sample_id, d.adddetails
#    FROM   data d
#    JOIN   ins1 USING (firstname, lastname)
#    RETURNING sample_id, user_id
#    )
# INSERT INTO sample2 (user_id, value)
# SELECT ins2.user_id, d.value
# FROM   data d
# JOIN   ins1 USING (firstname, lastname)
# JOIN   ins2 USING (sample_id);

    # Insert some data.
    query = """
    WITH data (ontology, class_id, preferred_label,
         synonyms, definitions, obsolete, cui, semantic_types, parents) as (
         VALUES (:ontology, :class_id, :preferred_label, CAST( :synonyms AS varchar[]),
         :definitions, :obsolete, :cui, CAST( :semantic_types AS varchar[]), 
         CAST( :parents as varchar[]))
    )
    , ins1 as (
        INSERT INTO ontologies (ontology, class_id, preferred_label,
         definitions, obsolete, cui)
         select ontology, class_id, preferred_label, definitions, obsolete, cui from data
         returning ontologies.id as ontology_id, class_id, ontology
    )
    , ins2 as (
        INSERT INTO parents (ontology_id, parent)
         select ontology_id, UNNEST(data.parents) 
        from ins1 join data USING(class_id,ontology))
    , ins3 as (
        INSERT INTO synonyms (ontology_id, synonym)
         select ontology_id, UNNEST(synonyms) 
        from ins1 join data USING(class_id,ontology))
    INSERT INTO semantic_types (ontology_id, semantic_type)
         select ontology_id, UNNEST(semantic_types) 
        from ins1 join data USING(class_id,ontology)
    """
    try:
        await database.execute_many(query=query, values=vals)
    except Exception as e:
        print(e)
    await database.disconnect()


if __name__ == '__main__':
    create_db(database_url)
    exit(0)
    asyncio.get_event_loop().run_until_complete(create_onto_table())
    for onto in sorted(get_all_ontology_short_ids()):
        print(onto)
        vals = []
        with open(onto + '.json', 'w') as outfile:
            try:
                vals = ontology_csv(onto)
                asyncio.get_event_loop().run_until_complete(main(vals))
            except KeyboardInterrupt:
                exit(0)
            except Exception as e:
                os.unlink(onto + '.json')
                print(f'error with {onto}')
                print(e)
                continue
        
