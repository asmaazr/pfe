from flask import Flask, render_template, request,session ,redirect,url_for
import requests
import re
import json
import pandas as pd
import pycountry
from senti_anal import *
from aspect_model import *
from tweet import *
import numpy as np
import plotly
import plotly.graph_objs as go
from airlines import airline_name
from sqlalchemy  import create_engine
import mysql.connector
from mysql.connector import Error
import plotly.express as px
from testw import *
from tweetEmbed import *
from flask import Markup
from localisation import *

app = Flask(__name__)




@app.route('/index', methods=('GET', 'POST'))
def index():
    # create sqlalchemy engine
    engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}"
                        .format(user="root",
                                pw="mercurycreatures12345",
                                db="projet_dyal_pfe"))
    
    #ar = request.form.getlist('airline')
    ar = request.args.get('airline')
    # Insert whole DataFrame into MySQL
        
    local = request.args.get('local')
    lang= request.args.get('lang')
    count =request.args.get('count')
    date_s= request.args.get('date_s')
    date_e= request.args.get('date_e')
    if lang is not None and lang != 'eu':
        lang = lang.capitalize()
        lang = pycountry.languages.get(name=lang)
        lang = lang.alpha_2
    else :
        lang = 'en'
    if local is not None and local != '':
        local = local.capitalize()
        place = api.geo_search(query=local, granularity="country")
        place_id = place[0].id
    else :
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
        df['sentiment']=tw
        df['aspect']= asp
        df.to_sql('details', con = engine, if_exists = 'replace')
        return redirect(url_for('data'))

    
    return render_template('index.html' ,data = airline_name)





@app.route('/data')
def data():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='projet_dyal_pfe',
                                            user='root',
                                            password='mercurycreatures12345')

        ##     Labels   ##
        sql_select_Query = "SELECT distinct airline from details order by airline"
        cursor = connection.cursor()
        cursor.execute(sql_select_Query)
        records = cursor.fetchall()
        count = cursor.rowcount
        wiki = []
        blabla = []
        par = []
        p= "positive"
        n ="negative"
        nt="neutral"
        for row in records:
            wiki_details={}
            print(row[0])
            blabla.insert(0, row[0])
            blabla.append(p)
            blabla.append(n)
            blabla.append(nt)
            wiki_details['airline_name']=row[0]
            wiki_details['summary']=wikipd(row[0])
            wiki_details['image'] = get_wiki_image(row[0])
            wiki.append(wiki_details)
            print(wiki)
            for sm in range(3) :
                par.insert(0, row[0])
        print(blabla)  
        ##    parents ##
        for sm in range(count) :
            par.insert(0, "")
        print(par)
        ##    values ##
        val = [10, 2, 6, 6, 4, 4,4,5,6]
        sql_select_Tweets= "SELECT airline,count(airline) from details group by airline order by airline"
        cursor1 = connection.cursor()
        cursor1.execute(sql_select_Tweets)
        records1 = cursor1.fetchall()
        for row in records1:
            val.insert(0, row[1])
        print(val)
        cursor1.close()
        sql_select_id_tweet = "SELECT id_tweet from details limit 25"
        cursor2 = connection.cursor()
        cursor2.execute(sql_select_id_tweet)
        records2 = cursor2.fetchall()
        
        data = []
        for tweet_id in records2 :
            tw = embedTw(tweet_id[0])
            data.append(Markup(tw))
        


    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
  
    return render_template('kiki.html',dt= blabla,ff = par,values = val,wik =wiki,code = data )
@app.route('/mapl')
def mapl():
    try:
        connection = mysql.connector.connect(host='localhost',
                                            database='projet_dyal_pfe',
                                            user='root',
                                            password='mercurycreatures12345')
        cursor = connection.cursor()
        sql_select_location = "SELECT DISTINCT location FROM details WHERE location IS NOT NULL"
        cursor3 = connection.cursor()  
        cursor3.execute(sql_select_location) 
        map = cursor3.fetchall()
        list_countries = [item for t in map for item in t]
        countries = []
        for c in list_countries:
            countries.append(get_loc(c))
        cleaned_count = [x for x in countries if x is not None]
        geo = pd.DataFrame(cleaned_count)
    except Error as e:
        print("Error reading data from MySQL table", e)
    finally:
        if (connection.is_connected()):
            connection.close()
            cursor.close()
            print("MySQL connection is closed")
    return  geo.to_csv(index=False) 





    


if __name__ == "__main__":
    app.run()
