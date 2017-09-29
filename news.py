#!/usr/bin/env python

import psycopg2

DBNAME = 'news'

def db_handler(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    p = c.fetchall()
    db.close()
    return p

def get_pop_articles():
    """Return a sorted list of articles that
    have been accessed the most. The most popular articles at the top.
"""
    query = """
    SELECT articles.title, popular_articles.num
    FROM articles JOIN popular_articles
    ON articles.slug = popular_articles.slug
    ORDER BY popular_articles.num desc
    LIMIT 3;
    """
    results = db_handler(query)
    print "\nMost Popular 3 Articles of all time:"

    for i in results:
        print "- %s - %d Views" % (i[0], i[1])


def get_pop_authors():
    """
    Return a sorted list with the most popular author at the top.
    """
    query = """
    SELECT authors.name, pop_authors.sum
    FROM authors JOIN pop_authors
    ON authors.id = pop_authors.author;
    """
    results = db_handler(query)
    print "\nMost Popular Article Authors of all time:"

    for i in results:
        print "- %s - %d Views" % (i[0], i[1])

def get_err_percentages():
    """
    Return the days which more than 1% of the requests lead to errors.
"""
    query = """
    SELECT to_char(date, 'FMMonth FMDD, YYYY'), error_percentage AS precentage
    FROM percentage_of_errors
    WHERE percentage_of_errors.error_percentage >= 1;
    """
    results = db_handler(query)
    print "\nDays with more than 1% of errors:"

    for i in results:
        print "- %s - %.2f%%" % (i[0], i[1])

if __name__ == "__main__":
    get_pop_articles()
    get_pop_authors()
    get_err_percentages()

