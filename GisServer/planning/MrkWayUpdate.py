__author__ = 'dima'

import psycopg2
import sys
import psycopg2.extras


def connect (host, dbname, user, pswd):
    conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, pswd,)
    # print "Connecting to database\n ->%s" % (conn_string)
    try:
        db = psycopg2.connect(conn_string)
    except psycopg2.Error as e:
        # print "I am unable to connect to the database"
        # print e.pgerror
        # sys.exit()
        raise
    return db

def MrkWayUpdate2(point_list):
    db2 = connect('localhost','gis_perm','gis_user','123')
    cursor = db2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #point_list[0][0] x point [0]
    #point_list[0][1] y point [0]
    #point_list[1][0] x point [1]
    #point_list[1][1] y point [1]
    i = 0
    str1 = 'LINESTRING( '
    for point in point_list:
        str1 = str1 + repr(point[0]) + ' ' + repr(point[1]) + ','


    str1 = str1[0: -1]
    str1 = str1 + ')'
    # print("update planet_osm_line set way = ST_GeomFromText('%s',4326) where name = 'MrkWay';"%(str1,))
    try:
        cursor.execute("update planet_osm_line set way = ST_GeomFromText(%s,4326) where name = 'MrkWay';",(str1,))
    except:
        print("Wrong query")
        return  None

    db2.commit()
    return 0

def DeleteWay():
    db2 = connect('localhost','gis_perm','gis_user','123')
    cursor = db2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    try:
        cursor.execute("update planet_osm_line set way = ST_GeomFromText('LINESTRING(39.74739 -105,39.74738 -105)',4326) where name = 'MrkWay';")
    except:
        print("Wrong query")
        return  None
    db2.commit();
