# Log Analysis

The program is using the following views:

```sql
CREATE VIEW popular_articles AS
SELECT substring(path, 10) AS slug, count(*) AS num
FROM log
WHERE status = '200 OK'
GROUP BY path
ORDER BY num DESC;

CREATE VIEW authors_views AS
SELECT articles.author,
       articles.slug,
       popular_articles.num
FROM articles
JOIN popular_articles ON articles.slug = popular_articles.slug;

CREATE VIEW pop_authors AS
SELECT authors_views.author,
       sum(authors_views.num) AS sum
FROM authors_views
GROUP BY authors_views.author
ORDER BY (sum(authors_views.num)) DESC;

CREATE VIEW requests_per_day AS
SELECT date_trunc('day', time) as date, count(*) AS requests
FROM log
GROUP BY 1;

CREATE VIEW not_found_per_day AS
SELECT not_found_list.date,
       count(*) AS num
FROM ( SELECT date_trunc('day', time) as date,
     status
FROM log
WHERE status = '404 NOT FOUND') as not_found_list
GROUP BY not_found_list.date;

CREATE VIEW percentage_of_errors AS
SELECT requests_per_day.date,
       not_found_per_day.num::double precision / requests_per_day.requests::double precision * 100::double precision AS error_percentage
FROM requests_per_day
JOIN not_found_per_day ON requests_per_day.date = not_found_per_day.date;
```


# Execution

To get the results run the python program `news.py`

`python news.py`