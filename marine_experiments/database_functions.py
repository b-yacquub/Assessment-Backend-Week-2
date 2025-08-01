"""Functions that interact with the database."""

from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import connection
from psycopg2 import sql


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


def get_experiment(conn: connection, type: str = None, score_over: int = None):
    with conn.cursor() as cur:
        query = ('''SELECT
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
JOIN species sp USING(species_id)''')
        params = []

        if type:
            query += (f" where et.type_name = '{type}'")
            params.append(type)

        if score_over is not None:
            query += (
                f" AND e.score::numeric / et.max_score * 100 > {score_over}")
            params.append(score_over)

        query += (" ORDER BY e.experiment_date DESC")
        cur.execute(query)

        return cur.fetchall()


def delete(conn: connection, id):
    with conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute(
            "SELECT experiment_id, experiment_date FROM experiment WHERE experiment_id = %s",
            (id,)
        )
        experiment = cur.fetchone()

        if not experiment:
            return False

        cur.execute(
            "DELETE FROM experiment WHERE experiment_id = %s", (str(id)))
        conn.commit()

        experiment_date = experiment["experiment_date"].strftime("%Y-%m-%d")
        return experiment_date


conn = get_db_connection("marine_experiments")
print(delete(conn, 3))
