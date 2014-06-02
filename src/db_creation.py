# -*- coding: utf-8 -*-
# <nbformat>3.0</nbformat>

# <codecell>

import csv
import numpy
import datetime
import pandas as pd
import subprocess
import psycopg2 as pg
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
   
db = 'cwbdb'    

def create_db(dbname, hostname='localhost', pg_admin_db='postgres'):
    #create a new postgresql database with postgis extension
    conn = pg.connect(host=hostname, database=pg_admin_db)
    checkdb_exist_sql = '''select count(datname) from pg_database where datname='%s';''' % dbname
    cur = conn.cursor()
    cur.execute(checkdb_exist_sql)
    result = cur.fetchone()
    if result[0] == 0:
        # http://initd.org/psycopg/docs/extensions.html?highlight=isolation_level_autocommit
        # before create new database, you need to set isolation level autocommit
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute('CREATE DATABASE %s;' % dbname)
        cur.close()
        conn = pg.connect(host=hostname, database=dbname)
        cur = conn.cursor()
        cur.execute('CREATE EXTENSION postgis;')
        cur.execute('CREATE EXTENSION postgis_topology;')
        conn.commit()
    else:
        print("The database %s already exists!" % dbname)
    cur.close()
def query_db(dbname, sql, hostname='localhost'):
    conn = pg.connect(host=hostname, database=dbname)
    cur = conn.cursor()
    cur.execute(sql)
    result = cur.fetchall()
    cur.close()
    return(result)
# create new table
def create_table(db, sql, hostname='localhost'):
    try:
        conn = pg.connect(host=hostname, database=db)
        cur = conn.cursor()
        conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cur.execute(sql)
        conn.close()
    except:
        print("Create table error!")
        raise
def insert_table(db, insert_sql, hostname='localhost'):
    try:
        conn = pg.connect(host=hostname, database=db)
        cur = conn.cursor()
        cur.execute(insert_sql)
        conn.commit()
        conn.close() 
    except:
        print("Insert data into table error!")
        raise

def split_rdate(db, new_table, orig_tab, hostname='localhost'):
    split_sql = '''
    CREATE TABLE %s AS (
    SELECT
        stn_code,
        substring(cast(rdate as text) from 1 for 4)::integer yr,
        substring(cast(rdate as text) from 5 for 2)::integer mm,
        substring(cast(rdate as text) from 7 for 2)::integer dd,
        substring(cast(rdate as text) from 9 for 2)::integer-1 hr,
        ps01, tx01, rh01, wd01, wd02, pp01, ss01 
    FROM %s); ''' % ( new_table, orig_tab )
    conn = pg.connect(host=hostname, database=db)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute(split_sql)
    conn.close()
    

# <codecell>

# create postgresql database with postgis extension
create_db(dbname=db)

# <codecell>

# create format
create_format_sql = '''
DROP TABLE IF EXISTS format_cwb;
DROP SEQUENCE IF EXISTS format_cwb_seq;
CREATE SEQUENCE format_cwb_seq;
CREATE TABLE format_cwb (
    id int DEFAULT nextval('format_cwb_seq') PRIMARY KEY,
    format character varying, -- format type, ex: Format_CWB_H_1
    pd_start date, -- start period of format, ex: 1951-01-01
    pd_end date, -- end period of format, ex:2008-12-31
    item_code character varying, -- item (observation) code 
    item_detail character varying, -- detail information of item
    pos_start int, -- start position 
    pos_end int -- end position
); '''

# create basic information of each meteorological station
create_meteo_sql = '''
DROP TABLE IF EXISTS station_cwb;
CREATE TABLE station_cwb (
    stn_code character(6) PRIMARY KEY, -- 測站代碼
    station character(24), -- 測站名稱
    elevation float, -- 海拔高度(m)
    x float, -- TWD97 經度
    y float -- TWD97 緯度
);'''


# <codecell>

#create_table(db, create_meteo_sql)
create_table(db,create_format_sql)

# <codecell>

try:
    format_file = open('info/format_cwb.csv', 'r')
    sql_insert = 'INSERT INTO format_cwb (format, pd_start, pd_end, item_code, item_detail, pos_start, pos_end) VALUES ('
    conn = pg.connect(host='localhost', database=db)
    cur = conn.cursor()
    for row in format_file.readlines():
        insert = sql_insert+str(row)+');'
        cur.execute(insert)
    conn.commit()
    conn.close()
except:
    raise

# <codecell>

# insert station information into station_cwb table
conn = pg.connect(host='localhost', database=db)
cur = conn.cursor()
rfile = open('info/stn_info.csv', 'r')
csv_reader = csv.reader(rfile)
s1 = 'INSERT INTO station_cwb (stn_code, station, elevation, x, y) VALUES ('
for row in csv_reader:
    insert = s1+'\''+row[0]+'\',\''+row[1]+'\','+row[2]+','+row[4]+','+row[6]+');'
    cur.execute(insert)
conn.commit()
conn.close()

# <codecell>

sql = 'select stn_code from station_cwb_2 where stn_code like \'C%\''
stn_res = query_db(db, sql)

# <codecell>

# concatenate hourly data into single file
autostn_a1 = []
autostn_a2 = []
for i in stn_res:
    # type A1
    cp1 = '''cat CWB_A_%s_200[0-8]*.txt CWB_A_%s_20090[1-9].txt CWB_A_%s_200910.txt > ../../../data/type_a/CWB_A1_%s.txt'''% (i[0], i[0], i[0], i[0])
    cp2 = '''cat CWB_A_%s_20091[1-2].txt CWB_A_%s_201*.txt > ../../../data/type_a/CWB_A2_%s.txt''' % (i[0], i[0], i[0])
    autostn_a1.append(cp1)
    autostn_a2.append(cp2)
autostn_cat_f1 = open('script/autostn_list_cat.sh', 'w')
autostn_cat_f2 = open('script/autostn_list_cat2.sh', 'w')
for item in autostn_a1:
  autostn_cat_f1.write("%s\n" % item)
for item in autostn_a2:
  autostn_cat_f2.write("%s\n" % item)

# <codecell>

query_stn_code = '''
select stn_code from station_cwb where stn_code not like '4%';'''
stn = query_db(db, query_stn_code)
# create automatic recording meteorological station
for i in range(0, len(stn)):
    create_auto_stn_sql = '''
    DROP TABLE IF EXISTS stn_auto_%s;
--    CREATE TABLE stn_auto_%s(
--        stn_code character varying,
--        rdate numeric,
--        ps01 float,
--        tx01 float,
--        wd01 float,
--        wd02 float,
--        pp01 float,
--        ss01 float
--    );
    ''' % (stn[i][0], stn[i][0])
    create_table(db, create_auto_stn_sql)

# <codecell>

list_inputf_sql = '''SELECT stn_code from info_a_1_list;'''
input_stn = query_db(db, list_inputf_sql)
input_stn

# <codecell>

list_inputf_sql = '''SELECT stn_code from info_a_1_list;'''
input_stn = query_db(db, list_inputf_sql)
conn = pg.connect(host='localhost', database=db)
cur = conn.cursor()
for i in range(0,len(input_stn)):
    stn_name = input_stn[i][0].lower()
    out_stn_file = '/tmp/stn_auto_'+stn_name+'.csv'
    # find the column specs
    tab_width_sql = '''select pos_start,pos_end from format_cwb where format='Format_CWB_A_1';'''
    tab_width = query_db(db, tab_width_sql)
    tab_len = len(tab_width)
    # dirty hack of date and hour column
    #date_list = (tab_width[1][0]-1,tab_width[4][1])
    #hr_list = (tab_width[4][0]-1,tab_width[4][1])
    #ncolspec = [tab_width[0], (7,17)]#, hr_list]
    #for row in range(5,tab_len):
    #    ncolspec.append(tab_width[row])
    ncolspec = [(0, 6), (7, 17), (18, 24), (25, 31), (32, 38), (39, 45), (46, 52), (53, 59)]
    # open raw data and use read_fwf to read and parse date
    stn_data_file = open('concat_a/CWB_A_%s_1.txt' % stn_name.upper(), 'r')
    #pd.read_fwf(stn_data_file, colspecs=ncolspec, header=None, infer_datetime_format=True, parse_dates=[1], na_values='-9999')
    df = pd.read_fwf(stn_data_file, colspecs=ncolspec, header=None, na_values='-9999')

    df.to_csv(out_stn_file, index=False, convert_datetime64=False , header=False)
    copy_sql = '''COPY %s FROM '%s' WITH CSV DELIMITER ',';
    ''' % ( 'stn_auto_'+stn_name, out_stn_file )
    cur.execute(copy_sql)
    conn.commit()
    print(stn_name)
conn.close()

# <codecell>

ncolspec = [(0, 6), (7, 17), (18, 24), (25, 31), (32, 38), (39, 45), (46, 52), (53, 59)]
stn_a1_data = open('data/CWB_A1_all.txt', 'r')
a1_df = pd.read_fwf(stn_a1_data, colspecs=ncolspec, header=None, na_values='-9999')
a1_df.to_csv('data/CWB_A1_all_parsed.csv', index=False, header=False)

# <codecell>


# <codecell>


# <codecell>


# <markdowncell>

# ##重新整理測站表格，把時間欄位(rdate) 分割成年、月、日、時##
# 把原本的時間減一(ex: 24 => 24-1 = 23）

# <codecell>

split_rdate('cwbdb', 'stn_auto_r', 'stn_auto')

# <codecell>


# <codecell>


