__author__ = 'dima'

import psycopg2
import sys
import psycopg2.extras
import json
import time
from planning.main import *



#SELECT ST_AsText(ST_Transform(way,4326)) FROM  planet_osm_polygon where osm_id=311957108;



def connect (host, dbname, user, pswd):
    conn_string = "host=%s dbname=%s user=%s password=%s" % (host, dbname, user, pswd,)
    db = psycopg2.connect(conn_string)
    return db

def PrintPolygon(cursor, osm_id):
    quary_string = "SELECT ST_AsText(ST_Transform(way,4326)) FROM  planet_osm_polygon where osm_id=%s;"  % (osm_id,)
    cursor.execute(quary_string)
    #print quary_string
    for value in cursor:
        data = value
        #print value ['st_astext']
    # to string
    str = json.dumps(data)
    print (str)
    # from string
    print (json.loads(str))
    json.dump(data, open('test.js', 'w'))

def GetCurentLoc1(cursor):
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_point where name='Robot_location';"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonString.js', 'w') as f :
        for value in cursor:
            #son_string = 'var geojsonFeature = {"type": "Feature","geometry":' + value ['st_asgeojson'] + '};'
            GeoJsonString = value ['st_asgeojson']
        #json.dump(json_string, open('JsonString.js', 'w'))
        #var geojsonFeature = {"type": "Feature", "geometry": {"type": "Point","coordinates": [ 56.22343,58.05407]}};
        json_parse = json.loads(GeoJsonString)
        json_parse['coordinates'].reverse()# if polygon, reverse() for each element
        GeoJsonString = json.dumps(json_parse)
        GeoJsonString = '{"type": "Feature","geometry":' + GeoJsonString+ '}'
        return GeoJsonString

def GetCurentLoc(cursor):
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_point where name='Robot_location';"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonString.js', 'w') as f :
        for value in cursor:
            #son_string = 'var geojsonFeature = {"type": "Feature","geometry":' + value ['st_asgeojson'] + '};'
            GeoJsonString = value ['st_asgeojson']
        #json.dump(json_string, open('JsonString.js', 'w'))
        #var geojsonFeature = {"type": "Feature", "geometry": {"type": "Point","coordinates": [ 56.22343,58.05407]}};
        json_parse = json.loads(GeoJsonString)
        json_parse['coordinates'].reverse()# if polygon, reverse() for each element
        GeoJsonString = json.dumps(json_parse)
        GeoJsonString = 'var geojsonFeature = {"type": "Feature","geometry":' + GeoJsonString+ '};'

        geodata = {"type": "Feature","geometry":{"type": "Point", "coordinates": [56.22361, 58.05473]}}
        from json import dumps
        GeoJsonString = dumps(geodata)

        f.write(GeoJsonString)

    #SELECT ST_AsText(ST_Transform(way,4326)) FROM  planet_osm_point;
    #58.05407,56.22343 CORP. A LOCATION
    #insert into planet_osm_point(name,way) values ('Robot_location',ST_SetSRID(ST_MakePoint(58.05407,56.22343),4326));
    #SELECT osm_id, ST_AsText(ST_Transform(way,4326)) FROM  planet_osm_point where name='Robot_location';

def GetWay1(cursor):
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_line where name='MrkWay';"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonString.js', 'a') as f :
        for value in cursor:
            GeoJsonString = value ['st_asgeojson']
        json_parse = json.loads(GeoJsonString)
        for str in json_parse['coordinates']:
            str.reverse()# if polygon, reverse() for each element

        GeoJsonString = json.dumps(json_parse)
        GeoJsonString = '{"type": "Feature","geometry":' + GeoJsonString+ '}'
        # ForPlanning()
        return GeoJsonString


def GetWay(cursor):
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_line where name='MrkWay';"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonString.js', 'a') as f :
        for value in cursor:
            GeoJsonString = value ['st_asgeojson']
        json_parse = json.loads(GeoJsonString)
        for str in json_parse['coordinates']:
            str.reverse()# if polygon, reverse() for each element

        GeoJsonString = json.dumps(json_parse)
        GeoJsonString = '\nvar myLines = {"type": "Feature","geometry":' + GeoJsonString+ '};'
        f.write(GeoJsonString)

def GetJsonPol(cursor):
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_polygon;"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonStringPol.js', 'w') as f :
        for value in cursor:
            GeoJsonString = value ['st_asgeojson'] + '\n'
            f.write(GeoJsonString)
        #GeoJsonString = '\nvar myLines = {"type": "Feature","geometry":' + GeoJsonString+ '};'
        #f.write(GeoJsonString)

def SetCurrentLocation(cursor, db):#update current location in db from cl.json file
    with open('cl.json', 'r') as f :
        for value in f:
            json_str = json.loads(value)

        cursor.execute("update planet_osm_point set way = ST_SetSRID(ST_MakePoint(%s,%s),4326) where name = 'Robot_location';",(json_str['coordinates'][0],json_str['coordinates'][1],))
    db.commit()
    return 0

def SetCurLocJsonFile(x,y):
    with open('cl.json', 'w') as f:
        #JsonStr = '{"type": "Point", "coordinates": [%s, %s]}' %(x,y)
        JsonStr = {"type": "Point", "coordinates": [x, y]}
        s = json.dumps(JsonStr)
        f.write(s)
    return 0

def TestCurLoc(cursor,db):
    while True: 
        SetCurLocJsonFile(58.0563, 56.2232)
        SetCurrentLocation(cursor, db)
        GetCurentLoc(cursor)
        GetWay(cursor)
        time.sleep(3)
        SetCurLocJsonFile(58.05475,56.2225)
        SetCurrentLocation(cursor, db)
        GetCurentLoc(cursor)
        GetWay(cursor)
        time.sleep(3)
        SetCurLocJsonFile(58.05477,56.22309)
        SetCurrentLocation(cursor, db)
        GetCurentLoc(cursor)
        GetWay(cursor)
        time.sleep(3)
        SetCurLocJsonFile(58.05475,56.2234)
        SetCurrentLocation(cursor, db)
        GetCurentLoc(cursor)
        GetWay(cursor)
        time.sleep(3)
        SetCurLocJsonFile(58.05473,56.22361)
        SetCurrentLocation(cursor, db)
        GetCurentLoc(cursor)
        GetWay(cursor)
        time.sleep(3)


def MrkWayUpdate(cursor, db):
    arg_line = []
    f2 = open('MrkWay.txt', 'r')
    for line in f2:
       #arg_line = line.split(' ')
       arg_line.extend(line.split(' '))
    i = 0
    str1 = 'LINESTRING( '
    for a in arg_line:
        if i < len(arg_line):
            str1 = str1 + arg_line[i] + '  ' + arg_line[i+1] + ','
        i = i+2
    str1 = str1[0: -1]
    str1 = str1 + ')'
    cursor.execute("update planet_osm_line set way = ST_GeomFromText(%s,4326) where name = 'MrkWay';",(str1,))
    print (str1)
    f2.close()
    db.commit()
    return 0

def MrkWayUpdateJSON(json_data, num):
    """
	[1] - КОНЕЧНАЯ ТОЧКА НЕ ЛЕЖИТ НА КАРТЕ
	[2] - путь до заданной точки не может быть проложен
	[3] - путь до заданнойточки не может быть проложен

	Возвращает:
	None - когда точки не лежат на карте
		(удалить путь)
	[] - когда путь между точками не может быть проложен (точки не связаны)
		(удалить путь)
	[_] - когда путь лежит на одном полигоне (нарисовать одну точку)
	[_ .. _] - все нормально, строим путь
	"""
    db = connect('localhost','gis_perm','gis_user','123')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #json_data = '{"type": "Feature","geometry":{"type": "LineString", "coordinates": [[56.22304, 58.05366], [56.2225, 58.05368], [56.2225, 58.05475], [56.2188, 58.0542], [56.2234, 58.05475], [56.22361, 58.05473], [56.2235, 58.0544]]}}'
    json_obj = json.loads(json_data)
    json_obj = json.loads(json_obj)
    str1 = 'LINESTRING( '
    for point in json_obj['geometry']['coordinates']:#x = point[0], y = point[1]
        str1 = str1 + repr(point[1]) + ' ' + repr(point[0]) + ','
    str1 = str1[0: -1]
    str1 = str1 + ')'

    cursor.execute("update planet_osm_line set way = ST_GeomFromText(%s,4326) where name = 'MrkWay';",(str1,))
    print("update planet_osm_line set way = ST_GeomFromText('%s',4326) where name = 'MrkWay';" % (str1))
    db.commit()
    if(num == 2):
        exc = ForPlanning()
    else:
        exc = "Маршрут построен"
    return exc

def ForPlanning():
    count = 0
    db = connect('localhost','gis_perm','gis_user','123')
    cursor = db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    quary_string = "SELECT ST_AsGeoJSON(ST_AsText(ST_Transform(way,4326))) FROM  planet_osm_line where name='MrkWay';"
    cursor.execute(quary_string)
    #print quary_string
    with open('JsonString.js', 'a') as f :
        for value in cursor:
            GeoJsonString = value ['st_asgeojson']
        json_parse = json.loads(GeoJsonString)
        for str in json_parse['coordinates']:
            count = count + 1
        x = json_parse['coordinates'][0]
        y = json_parse['coordinates'][count-1]

    return compute_path(x, y)


        #GeoJsonString = json.dumps(json_parse)
        #GeoJsonString = '\nvar myLines = {"type": "Feature","geometry":' + GeoJsonString+ '};'
        #f.write(GeoJsonString)


def main():
    db2 = connect('localhost','gis_perm','gis_user','123')
    cursor = db2.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    #ForPlanning()
    SetCurLocJsonFile(58.0563, 56.2232)
    SetCurrentLocation(cursor, db2)
    GetCurentLoc(cursor)
    GetWay(cursor)
    #PrintPolygon(cursor, 311957108)
    arg_line = 1
    #SetCurrentLocation(cursor, db2)
    #GetCurentLoc(cursor)
    ###MrkWayUpdate(cursor, db2)
    ###GetWay(cursor)
    ###TestCurLoc(cursor,db2)
    #MrkWayUpdateJSON()

    #GetJsonPol(cursor)
    #---------------------------------------------------------------------
    #f2 = []
    #f2.append('58.05378')
    #f2.append('56.22206')
    #CurrentLocation(cursor, db2, f2)
    #MrkWayUpdate(cursor, db2)
    #Cikle (cursor, db2)

if __name__ == "__main__":
    main()