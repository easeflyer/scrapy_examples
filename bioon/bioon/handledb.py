# -*- coding:utf-8 -*-

'''
Function:handle database's any operation
Author:Wan Shitao
Email:wst.521@163.com
Date:2014.8.20
Reference:funcs.py
'''
from twisted.enterprise import adbapi

try:  # py3
    import pymysql

    CURSORCLASS = pymysql.cursors.DictCursor
    pymysql.install_as_MySQLdb()
except:  # py2
    import MySQLdb

    CURSORCLASS = MySQLdb.cursors.DictCursor


def get_db(**kwargs):
    '''connect database,return link resource'''
    try:
        db = pymysql.connect(**kwargs)
    except:
        try:
            db = MySQLdb.connect(**kwargs)
            return db
        except Exception as e:
            print("Link DB error:", e)
    else:
        return db


def create_table(data, primary, table, **kwargs):
    ''' Create table for storing resume data. '''
    sql = 'create table if not exists `%s`(%s) DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci'
    ps = ["`%s` text" % x for x in data] + ([primary, ] if primary else [])
    paras = ','.join(ps)
    SQL = sql % (table, paras)
    exec_sql(SQL, **kwargs)


def exec_sql(sql, data='', **kwargs):
    '''execute insert sql and other operation'''
    conn = get_db(**kwargs)
    cur = conn.cursor()
    if data == '':
        cur.execute(sql)
    else:
        cur.execute(sql, data)
    result = cur.fetchall()
    conn.commit()
    cur.close()
    conn.close()
    return result


def insert_data(data_, table, **kwargs):
    '''insert data into database'''
    insertSQL = "insert into `" + table + "`(%s) values (%s)"
    keys = list(data_.keys())
    fields = ','.join(['`%s`' % k for k in keys])
    qm = ','.join(['%s'] * len(keys))
    sql = insertSQL % (fields, qm)
    data = [data_[k] for k in keys]
    exec_sql(sql, data, **kwargs)


def adb_connect_db(db_type, **kwargs):
    '''
    db_type-->"MySQLdb"
    '''
    dbpool = adbapi.ConnectionPool(db_type, **kwargs)
    return dbpool


def adb_insert_data(item, table, db_type, **kwargs):
    keys = list(item.keys())
    fields = ','.join(keys)
    qm = ','.join(['%s'] * len(keys))
    insert_sql = "insert into `" + table + "`(%s) values (%s)"
    sql = insert_sql % (fields, qm)
    data = [item[k] for k in keys]
    dbpool = adb_connect_db(db_type, **kwargs)
    d = dbpool.runOperation(sql, data)
    d.addCallback(insSuccess)
    d.addErrback(insFailed, item)
    dbpool.close()


def insSuccess(data):
    print("data inserted", data)


def insFailed(exp, data):
    print("insert failed", data, "error:", exp.getErrorMessage())
