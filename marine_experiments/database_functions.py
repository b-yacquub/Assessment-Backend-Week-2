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
        query = '''SELECT
    e.experiment_id,
    e.subject_id,
    sp.species_name AS species,
    TO_CHAR(e.experiment_date,'yyyy-MM-dd')as experiment_date,
    et.type_name AS experiment_type,
    ROUND(
        (e.score / (et.max_score
        )) * 100, 2
    ) || '%' AS score
FROM
    experiment e
JOIN subject s USING(subject_id)
JOIN experiment_type et USING(experiment_type_id)
JOIN species sp USING(species_id)
ORDER BY e.experiment_date DESC;'''
        cur.execute(query)
        return cur.fetchall()


# conn = get_db_connection("marine_experiments")
# print(get_experiment(conn))
