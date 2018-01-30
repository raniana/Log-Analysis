#! /user/bin/env python3
import psycopg2
import datetime


def connect(database_name="news"):

    """ this function used to connect to the database returning
        a database and a cursor"""

    try:
        db = psycopg2.connect(database=database_name)
        cursor = db.cursor()
        return db, cursor
    except:
        print("couldn't connect to database")


def get_popular_articles():

    """ get the most 3 popular articles !!"""

    db, cursor = connect()
    cursor.execute("select title, count(*) as views from log join articles "
                   "on log.path = concat('/article/', articles.slug) "
                   "group by title "
                   "order by views desc limit 3;")
    pop_articles = cursor.fetchall()
    for row in pop_articles:
        print('\n* "{}" __ {} Views.'.format(row[0], row[1]))

    db.close()


def get_top_authors():

    """ get the most popular article authors of all time"""
    db, cursor = connect()
    cursor.execute("select authors.name, count(*) as num "
                   "from (select log.path, articles.title, "
                   "articles.author as sub_id from articles join log "
                   "on log.path = concat('/article/', articles.slug)) as subq "
                   "join authors on authors.id = subq.sub_id "
                   "group by authors.name order by num desc;")
    pop_authors = cursor.fetchall()
    for row in pop_authors:
        print('\n* {} __ {} Views.'.format(row[0], row[1]))
    db.close()


def get_day_of_one_percent_or_more_errors():

    """Which day got more than 1% errors of all requests ??"""
    db, cursor = connect()
    cursor.execute("""select f_subq.day, f_subq.errors, s_subq.total
                   from (select date_trunc('day', subq.time)::date "day",
                   count(*)::float as errors
                   from(select time from log where status!= '200 OK')as subq
                   group by day) as f_subq
                   join (select date_trunc('day', log.time)::date "day",
                   count(*)::float as total from log group by day) as s_subq
                   on f_subq.day = s_subq.day
                   where (f_subq.errors/ s_subq.total >= 0.01);""")

    result = cursor.fetchall()
    for row in result:
        print('\n{} __ {}% errors'.format(row[0], round(row[1]/row[2]*100, 2)))
    db.close()

if __name__ == '__main__':

    print("\nWhat are the most popular three articles of all time?" + '\n')
    get_popular_articles()
    print("\nWho are the most popular article authors of all time ??" + '\n')
    get_top_authors()
    print("\nWhich day got more than 1% errors of all requests ??" + '\n')
    get_day_of_one_percent_or_more_errors()
