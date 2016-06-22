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

    result = {}

    query_params = event.get("params")
    path_params = query_params.get("path") if query_params else None
    querystring_params = query_params.get("querystring") if query_params else None
    
    country = path_params.get("country") if path_params else None
    go_back = querystring_params.get("go_back") if querystring_params else None

    with conn.cursor() as cur:
        if country and any([country == c for c in ('US', 'BR', 'CA', 'AU')]):
            cur.execute("SELECT state, count(*) FROM job_posts WHERE country = %s GROUP BY state", (country, ))
        elif not country:
            cur.execute("SELECT country, count(*) FROM job_posts GROUP BY country")
        rows = cur.fetchall()
        for row in rows:
            if row[0] not in result:
                result[row[0]] = {}
            
            result[row[0]]["job_num"] = row[1]

    return result
