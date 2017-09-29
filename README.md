# Log Analysis

The purpose of the project is to print out reports on the terminal based on the newspaper database provided.

The code produces three reports:
..* Most popular three articles of all time
..* Most popular Article Authors of all time
..* Days with more than 1% of errors

The project makes use of the Linux based virtual machine VirtualBox/Vagrant environment which has all the components needed already installed (Python, PostgreSQL, and the psycopg2 library).

The news database is a SQL file containing newspaper articles, author's information and web server logs to the site.
This database contains three tables:
..* The `authors` table includes information about the authors of articles
..* The `articles` table includes the articles themselves.
..* The `log` table includes one entry for each time a user has accessed the site.

You can download the `newsdata.sql` file from [this link](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it into the `vagrant` directory which is shared with you virtual machine.

To build the reporting tool, you'll need to load the site's data into your local database.
To do this, `cd` into the `vagrant` directory and use the command `psql -d news -f newsdata.sql`
Explanation of the command executed:
..* `psql`: the PostgreSQL command line program
..* `-d news`: connect to the database named news which has been set up for you.
..* `-f newsdate.sql`: run the SQL statements in the file `newsdata.sql`

Running this command will connect to your installed database server and execute the SQL commands on the downloaded file, creating tables and populating them with data.

##Views:

You should create the following views into your local database before running the python file.

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

## Execution

To get all the reports run the python program `news.py`

`python news.py`

Also you would be able to import you code into another Python program or interactive Python session.
For example from a Python session you could do something like this:

```python
>>>import news as n
>>> n.get_err_percentages()

Days with more than 1% of errors:
- July 17, 2016 - 2.26%
>>>quit()
```
