import sys
import logging
import db_config
import psycopg2


#rds settings
rds_host  = db_config.rds_host
name = db_config.username
password = db_config.password
db_name = db_config.db_name
port = db_config.port

logger = logging.getLogger()
logger.setLevel(logging.INFO)

try:
    conn = psycopg2.connect(database=db_name, user=name, host=rds_host, password=password, port=port)
except:
    print "I am unable to connect to the database"


def handler(event, context):
    """
    This function fetches content from the RDS instance
    """

    query_params = event.get("params")
    path_params = query_params.get("path") if query_params else None
    querystring_params = query_params.get("querystring") if query_params else None
    
    country = path_params.get("country") if path_params else None
    state = path_params.get("state") if path_params else None
    go_back = querystring_params.get("go_back") if querystring_params else None

    result = []

    with conn.cursor() as cur:
        if state and not country:
            return result
        elif not country and not state:
            return result
        elif country and not state:
            query = '''
                WITH aux AS(
                    SELECT 
                        state,
                        city,
                        round(latitude::numeric, 1) AS lat,
                        round(longitude::numeric, 1) AS lon,
                        count(*) AS njobs
                    FROM
                        job_posts
                    WHERE
                        country = (%s)
                    GROUP BY
                        round(latitude::numeric, 1),
                        round(longitude::numeric, 1),
                        city,
                        state
                    ORDER BY
                        njobs DESC
                ),

                cities AS(
                    SELECT DISTINCT ON (lat, lon)
                        lat,
                        lon,
                        city
                    FROM
                        aux
                    ORDER BY
                        lat,
                        lon,
                        njobs DESC
                )

                SELECT
                    state,
                    cities.city,
                    avg(aux.lat),
                    avg(aux.lon),
                    sum(njobs)
                FROM 
                    aux JOIN cities 
                    ON
                        aux.lat = cities.lat 
                        AND 
                        aux.lon = cities.lon
                GROUP BY
                    cities.city,
                    state
                ORDER BY sum DESC'''

            cur.execute(query, (country, ))
        elif country and state:
            query = '''
                WITH aux AS(
                    SELECT 
                        state,
                        city,
                        round(latitude::numeric, 1) AS lat,
                        round(longitude::numeric, 1) AS lon,
                        count(*) AS njobs
                    FROM
                        job_posts
                    WHERE
                        country = (%s)
                    AND 
                        state = (%s)
                    GROUP BY
                        round(latitude::numeric, 1),
                        round(longitude::numeric, 1),
                        city,
                        state
                    ORDER BY
                        njobs DESC
                ),

                cities AS(
                    SELECT DISTINCT ON (lat, lon)
                        lat,
                        lon,
                        city
                    FROM
                        aux
                    ORDER BY
                        lat,
                        lon,
                        njobs DESC
                )

                SELECT
                    state,
                    cities.city,
                    avg(aux.lat),
                    avg(aux.lon),
                    sum(njobs)
                FROM 
                    aux JOIN cities 
                    ON
                        aux.lat = cities.lat 
                        AND 
                        aux.lon = cities.lon
                GROUP BY
                    cities.city,
                    state
                ORDER BY sum DESC'''

            cur.execute(query, (country, state))
            
            
        rows = cur.fetchall()
        for row in rows:
            result.append({
                "location": row[1],
                "count": int(row[4]),
                "lat": float(row[2]),
                "lon": float(row[3])
            })
    
    return result
