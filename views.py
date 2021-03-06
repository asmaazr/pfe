from flask import Flask, render_template, request, session, redirect, url_for
import plotly.graph_objects as go
import requests
import re
import json
import pandas as pd
import pycountry
from models_process import *
from tweet import *
import numpy as np
import plotly
import plotly.graph_objs as go
from airlines import airline_name
from sqlalchemy import create_engine
import mysql.connector
from mysql.connector import Error
import plotly.express as px
from wiki import *
from tweetEmbed import *
from flask import Markup
from localisation import *
import connection_db

app = Flask(__name__)


@app.route('/index', methods=('GET', 'POST'))
def index():
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                           .format(user=connection_db.user,
                                   pw=connection_db.password,
                                   db=connection_db.database))

    #ar = request.form.getlist('airline')
    ar = request.args.get('airline')
    # Insert whole DataFrame into MySQL

    local = request.args.get('local')
    lang = request.args.get('lang')
    count = request.args.get('count')
    date_s = request.args.get('date_s')
    date_e = request.args.get('date_e')
    if lang is not None and lang != 'eu':
        lang = lang.capitalize()
        lang = pycountry.languages.get(name=lang)
        lang = lang.alpha_2
    else:
        lang = 'en'
    if local is not None and local != '':
        local = local.capitalize()
        place = api.geo_search(query=local, granularity="country")
        place_id = place[0].id
    else:
        place_id = ''

    if count is None or int(count) > 100:
        count = 100

    if ar is not None:
        ar = str(ar)
        ar = list(ar.split(","))
        ar = ' '.join(ar).split()
        print(ar)
        l = stream_tweets(ar)
        print(l)
        df = pd.DataFrame(l)
        sentiments = []
        for tweet in l:
            sentiments.append(tweet['tweet'])
        tw = predict_senti(sentiments)
        asp = predict_asp(sentiments)
        df['sentiment'] = tw
        df['aspect'] = asp
        df.to_sql('details', con=engine, if_exists='replace')
        return redirect(url_for('data'))

    return render_template('index.html', data=airline_name)


@app.route('/data')
def data():
    try:
        connection = mysql.connector.connect(host=connection_db.host,
                                             database=connection_db.database,
                                             user=connection_db.user,
                                             password=connection_db.password)

        ##     Labels   ##
        sql_select_Query = "SELECT distinct airline from details order by airline"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        count = cursor.rowcount
        wiki = []
        blabla = []
        par = []
        p = "positive"
        n = "negative"
        nt = "neutral"
        airlines = []
        for row in records:
            wiki_details = {}
            print(row[0])
            blabla.insert(0, row[0])
            blabla.append(p)
            blabla.append(n)
            blabla.append(nt)
            wiki_details['airline_name'] = row[0]
            airlines.insert(0, row[0])
            wiki_details['summary'] = wikipd(row[0])
            wiki_details['image'] = "https://"+get_data(row[0])
            wiki.append(wiki_details)
            print(wiki)
            for sm in range(3):
                par.insert(0, row[0])
        print(blabla)

        ##    parents ##
        for sm in range(count):
            par.insert(0, "")
        print(par)
        ##    values ##
        val = []
        sql_select_Tweets = "SELECT airline,count(airline) from details group by airline order by airline"
        cursor1 = connection.cursor()
        cursor1.execute(sql_select_Tweets)
        records1 = cursor1.fetchall()
        for row in records1:
            val.insert(0, row[1])
        for airline in airlines:
            sql_select_positive = "SELECT airline,count(sentiment) from details where sentiment='positive' and airline='%s'" % (
                airline)
            sql_select_negative = "SELECT airline,count(sentiment) from details where sentiment='negative' and airline='%s'" % (
                airline)
            sql_select_neutral = "SELECT airline,count(sentiment) from details where sentiment='neutral' and airline='%s'" % (
                airline)
            cursorpos = connection.cursor()
            cursorpos.execute(sql_select_positive)
            cursorpos1 = cursorpos.fetchall()

            cursorneg = connection.cursor()
            cursorneg.execute(sql_select_negative)
            cursorneg1 = cursorneg.fetchall()

            cursornet = connection.cursor()
            cursornet.execute(sql_select_neutral)
            cursornet = cursornet.fetchall()
            for row in cursorpos1:
                val.append(row[1])
            for row in cursorneg1:
                val.append(row[1])
            for row in cursornet:
                val.append(row[1])

        print(val)
        cursor1.close()
        sql_select_id_tweet = "SELECT id_tweet from details limit 25"
        cursor2 = connection.cursor()
        cursor2.execute(sql_select_id_tweet)
        records2 = cursor2.fetchall()
        aspects = ['Ground Service', 'Inflight Entertainement', 'Legroom',
                   'Value For Money', 'Food & Beverage', 'Cabin Staff Service']
        vis = []
        for airline in airlines:
            visual = []
            for aspect in aspects:
                sql_aspects = "SELECT count(aspect) from details where aspect='%s' and airline='%s' " % (
                    aspect, airline)
                cursor4 = connection.cursor()
                cursor4.execute(sql_aspects)
                records4 = cursor4.fetchall()
                visual.append(records4[0][0])
            vis.append(visual)
            print(vis)
        data = []
        for tweet_id in records2:
            tw = embedTw(tweet_id[0])
            data.append(Markup(tw))

        sql_count_tw = "SELECT COUNT(id_tweet) FROM details"
        cursor3 = connection.cursor()
        cursor3.execute(sql_count_tw)
        records3 = cursor3.fetchall()
        for rr in records3:
            nb_tw = rr[0]

        sql_select_best = "SELECT airline ,MAX(counted) FROM (SELECT airline ,COUNT(airline) AS counted  FROM details WHERE sentiment = 'positive' GROUP BY airline) AS counts;"
        cursor5 = connection.cursor()
        cursor5.execute(sql_select_best)
        records5 = cursor5.fetchall()
        for rr in records5:
            best = rr[0]

    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")

    return render_template('results.html', dt=blabla, ff=par, values=val, wik=wiki, code=data, air=airlines, vis=vis, aspects=aspects, nb_tw=nb_tw, best=best)


@app.route('/mapl')
def mapl():

    connection = mysql.connector.connect(host=connection_db.host,
                                         database=connection_db.database,
                                         user=connection_db.user,
                                         password=connection_db.password)
    cursor = connection.cursor()
    sql_select_location = "SELECT DISTINCT location FROM details WHERE location IS NOT NULL"
    curs3 = connection.cursor()
    curs3.execute(sql_select_location)
    map = curs3.fetchall()
    list_countries = [item for t in map for item in t]

    new_list = []
    etc = ''
    for l in list_countries:
        for c in l:
            if c.isalnum():
                etc += c
        new_list.append(etc)
        etc = ''

    countries = []
    for c in new_list:
        countries.append(get_loc(c))

    cleaned_count = [x for x in countries if x is not None]
    geo = pd.DataFrame(cleaned_count)
    print(geo)
    return geo.to_csv(index=False)


if __name__ == "__main__":
    app.run()
