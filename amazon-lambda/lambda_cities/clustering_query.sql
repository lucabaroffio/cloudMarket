WITH aux AS(
SELECT state, city, round(latitude::numeric, 1) AS lat, round(longitude::numeric, 1) AS lon, count(*) AS njobs FROM job_posts WHERE country ='US' AND state = 'CA' GROUP BY round(latitude::numeric, 1), round(longitude::numeric, 1), city, state ORDER BY njobs DESC),

cities AS(
SELECT DISTINCT ON (lat, lon) lat, lon, city FROM aux ORDER BY lat, lon, njobs DESC)

SELECT state, cities.city, avg(aux.lat), avg(aux.lon), sum(njobs) FROM aux JOIN cities ON aux.lat = cities.lat AND aux.lon = cities.lon GROUP BY cities.city, state ORDER BY sum DESC