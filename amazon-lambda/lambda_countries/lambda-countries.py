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

    item_count = 0

    result = {}

    with conn.cursor() as cur:
        cur.execute("SELECT country, count(*) FROM job_posts GROUP BY country")
        rows = cur.fetchall()
        for row in rows:
            result[row[0]] = row[1]

    print result
    return result
