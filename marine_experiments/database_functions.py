"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection


def get_db_connection(dbname,
                      password="postgres") -> connection:
    """Returns a DB connection."""

    return connect(dbname=dbname,
                   host="localhost",
                   port=5432,
                   password=password,
                   cursor_factory=RealDictCursor)


def get_subject(conn: connection):
    with conn.cursor() as cur:
        query = '''select s.subject_id,s.subject_name,sp.species_name,TO_CHAR(s.date_of_birth,'yyyy-MM-dd') as date_of_birth
        from subject s join species sp using (species_id)
        order by date_of_birth desc;'''
        cur.execute(query)
        return cur.fetchall()


def get_experiment(conn: connection):
    with conn.cursor() as cur:
        query = '''select e.experiment_id,e.subject_id,sp.species_name as species
,e.experiment_date,et.type_name as experiment_type,
ROUND((e.score / 133) * 100, 2) || '%' as score
from experiment e 
join subject s using(subject_id)
join experiment_type et using(experiment_type_id)
join species sp using(species_id)
order by e.experiment_date desc;'''
        cur.execute(query)
        return cur.fetchall()


# conn = get_db_connection("marine_experiments")
# print(get_subject(conn))
