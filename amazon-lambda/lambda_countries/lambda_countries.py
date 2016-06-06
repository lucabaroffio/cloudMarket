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
            if row[0] not in result:
                result[row[0]] = {}
            
            result[row[0]]["job_num"] = row[1]

        query = """WITH temp AS
(SELECT country, company, count(*) FROM job_posts WHERE company IS NOT NULL AND company != '' GROUP BY country, company ORDER BY count DESC),

temp2 AS
(SELECT *, ROW_NUMBER() OVER(PARTITION BY country ORDER BY count DESC) as rank FROM temp)

SELECT country, company, count, rank FROM temp2 WHERE rank <= 3"""
        
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[0] not in result:
                result[row[0]] = {}

            result[row[0]]["company%s" % row[3]] = row[1]
            result[row[0]]["numjobs%s" % row[3]] = row[2]

        query = """WITH temp AS
(SELECT country, jobtitle, count(*) FROM job_posts WHERE jobtitle IS NOT NULL AND jobtitle != '' GROUP BY country, jobtitle ORDER BY count DESC),

temp2 AS
(SELECT *, ROW_NUMBER() OVER(PARTITION BY country ORDER BY count DESC) as rank FROM temp)

SELECT country, jobtitle, count, rank FROM temp2 WHERE rank <= 3"""
        
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            if row[0] not in result:
                result[row[0]] = {}

            result[row[0]]["jobtitle%s" % row[3]] = row[1]
            result[row[0]]["numjobstitle%s" % row[3]] = row[2]

    return result
