# Python 2.7.12

import psycopg2

DBNAME = 'news'


def get_pop_articles():
    """Return a sorted list of articles that
    have been accessed the most. The most popular articles at the top.
"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
    SELECT articles.title, popular_articles.num
    FROM articles JOIN popular_articles
    ON articles.slug = popular_articles.slug
    ORDER BY popular_articles.num desc
    LIMIT 4;
    """)
    p = c.fetchall()
    db.close()
    return p[1:]


def get_pop_authors():
    """
    Return a sorted list with the most popular author at the top.
    """
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
    SELECT authors.name, pop_authors.sum
    FROM authors JOIN pop_authors
    ON authors.id = pop_authors.author;
    """)
    p = c.fetchall()
    db.close()
    return p


def get_percentage():
    """
    Return the days which more than 1% of the requests lead to errors.
"""
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute("""
    SELECT date, error_percentage AS precentage
    FROM percentage_of_errors
    WHERE percentage_of_errors.error_percentage >= 1;
    """)
    p = c.fetchall()
    db.close()
    return p

print get_percentage()


print "\nMost Popular 3 Articles of all time:"

for i in get_pop_articles():
    print "- %s - %d Views" % (i[0], i[1])

print "\nMost Popular Article Authors of all time:"

for i in get_pop_authors():
    print "- %s - %d Views" % (i[0], i[1])

print "\nDays with more than 1% of errors:"

for i in get_percentage():
    print "- %s - %.2f%%" % (i[0].strftime("%B %d, %Y"), i[1])