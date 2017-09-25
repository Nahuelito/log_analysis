# Log Analysis

The program is using the following views:

```sql
CREATE VIEW popular_articles AS
SELECT "substring"(log.path, 10) AS slug,
       count(*) AS num
FROM log
GROUP BY log.path
ORDER BY (count(*)) DESC
LIMIT 9;

CREATE VIEW pop_authors AS
SELECT authors_views.author,
       sum(authors_views.num) AS sum
FROM authors_views
GROUP BY authors_views.author
ORDER BY (sum(authors_views.num)) DESC;

CREATE VIEW date_log AS
SELECT log."time"::date AS date,
       log.status
FROM log;

CREATE VIEW requests_per_day AS
SELECT date_log.date,
       count(*) AS num
FROM date_log
GROUP BY date_log.date;

CREATE VIEW not_found_per_day AS
SELECT not_found_list.date,
       count(*) AS num
FROM ( SELECT date_log.date,
     date_log.status
FROM date_log
WHERE date_log.status = '404 NOT FOUND'::text) not_found_list
GROUP BY not_found_list.date;

CREATE VIEW percentage_of_errors AS
SELECT requests_per_day.date,
       not_found_per_day.num::double precision / requests_per_day.num::double precision * 100::double precision AS error_percentage
FROM requests_per_day
JOIN not_found_per_day ON requests_per_day.date = not_found_per_day.date;
```
# Execution

To get the results run the python program `news.py`

`python news.py`