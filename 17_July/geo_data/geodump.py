import sqlite3  
import json

conn = sqlite3.connect('opengeo.sqlite')
cur = conn.cursor()

fhand = open('where.js','a')
fhand.write('mydata = [\n')
count = 0
cur.execute('SELECT * FROM Locations')
for row in cur :
    data = row[1].decode()
    try : js =json.loads(data)
    except: continue

    if len(js['features']) == 0: continue

    try:
        # lat = js['features'][0]['geometry']["coordinates"][1]
        # lng = js['features'][0]['geometry']["coordinates"][0]
        # where = js['features'][0]['properties']['display-name']
        lat = js['features'][0]['geometry']['coordinates'][1]
        lng = js['features'][0]['geometry']['coordinates'][0]
        where = js['features'][0]['properties']['display_name']
        where = where.replace("'", "")
    except:
        print("Unexpected format")
        print(js)
    
    try:
        count += 1
        if count > 1 : 
            fhand.write(',\n')
        output = "["+str(lat)+","+str(lng)+", '" + where + "']"
        fhand.write(output)

    except: continue
fhand.write('\n];\n')

print(count, "records written to where.js")

    
