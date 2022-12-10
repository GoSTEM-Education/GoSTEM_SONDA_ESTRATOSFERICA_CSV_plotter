import folium
import csv

Lat = []
Lon = []
Time = []
Vel = []
Alt = []
RSSI = []
Course = []
Course_float = []
RSSI_float = []
coordinatesList = []
#Make maps
m = folium.Map(location=[40.368699226464095, -1.5692626328666004], zoom_start=13)

tooltip = "Test me!"

folium.Marker(
    [40.368699226464095, -1.5692626328666004], popup="<i>I'm Alive!</i>",
    tooltip=tooltip,
    icon=folium.Icon(color="red", icon="info-sign"),
).add_to(m)

#Read CSV files
#The fill must contain just the values. It will crash if the headers are not removed
#Headers: SAT,LATITUDE,LONGITUDE,ALTITUDE,SPEED,COURSE,RSSI,SNR,DATERX,TIMERX
with open('loggtest_CALOMARDE_6.csv') as csvfile:  
    sonda = csv.reader(csvfile, delimiter = ',')

    
    for row in sonda:
        Lat.append(row[1])
        Lon.append(row[2])
        Alt.append(row[3])
        Vel.append(row[4])
        Course.append(row[5])
        RSSI.append(row[6])
        Time.append(row[9])
        #It can also be in a tuple
        points=list(zip(Lat,Lon))

    i=0    
    for row in Lat:
        coordinatesList.append( [float(Lat[i]) , float(Lon[i])] )
        Course_float.append(float(Course[i]))
        RSSI_float.append(float(RSSI[i]))
        i=i+1
        
    
    i=0
    for row in Lat:
        if RSSI_float[i] <= -110: 
            print("Position: ",i)
            folium.Marker([Lat[i], Lon[i]],
            popup='T(UHT): '+Time[i] +'  RSSI: ' + RSSI[i] + ' Cord: '+ Lat[i] + ','+ Lon[i] ,
            icon=folium.Icon(color="red"),
            tooltip='Velocitat: ' + Vel[i] + ' m/s' + ' | Altitut: ' + Alt[i] + ' m' + ' | Curs: ' + Course[i] + 'º' 
            ).add_to(m)

        elif -110 < RSSI_float[i] <= -60:
            print("Position: ",i)
            folium.Marker([Lat[i], Lon[i]],
            popup='T(UHT): '+Time[i] +'  RSSI: ' + RSSI[i] + ' Cord: '+ Lat[i] + ','+ Lon[i] ,
            icon=folium.Icon(color="orange"),
            tooltip='Velocitat: ' + Vel[i] + ' m/s' + ' | Altitut: ' + Alt[i] + ' m' + ' | Curs: ' + Course[i] + 'º' 
            ).add_to(m)
        
        else:
            print("Position: ",i)
            folium.Marker([Lat[i], Lon[i]],
            popup='T(UHT): '+Time[i] +'  RSSI: ' + RSSI[i] + ' Cord: '+ Lat[i] + ','+ Lon[i] ,
            icon=folium.Icon(color="green"),
            tooltip='Velocitat: ' + Vel[i] + ' m/s' + ' | Altitut: ' + Alt[i] + ' m' + ' | Curs: ' + Course[i] + 'º' 
            ).add_to(m)
        
        if Course_float[i]!=0:
            folium.RegularPolygonMarker([Lat[i], Lon[i]], fill_color='blue', number_of_sides=3, radius=10, rotation=Course[i]).add_to(m)
            print(Course[i])
        i=i+1


	
folium.PolyLine(coordinatesList, color="red", weight=2.5, opacity=1).add_to(m)

        
print("Full Recorded Data: ") 
#print(Lat)
#print(Lon)
#print(points)
#print(coordinatesList)
print(Course)

m.save("GoSTEM_SONDA.html")

print("Map exported into 'GoSTEM_SONDA.html'. Open it in your browser.")
pass
