import folium
import csv
from pandas import read_csv
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from datetime import datetime
import numpy as np
#Aquestes llibraries han destar isntal·lades per poder fer funcionar correctament el codi

Lat = []
Temp = []
Pres = []
Lon = []
Time = []
Vel = []
Alt = []

RSSI = []
Course = []
Course_float = []
RSSI_float = []

#Plot Variables
coordinatesList = []
Temperatures = []
Pressure = []
Alture = []
Course_Plot = []
Velocity_Plot = []
Time_plot =[]

#Make maps
m = folium.Map(location=[41.943396421698935, 1.6867802678968304], zoom_start=9)
#Centrem on volem que estigui el mapa situat

tooltip = "Test me!"

#Creació d'un marcador demo, permet veure com funciona
folium.Marker(
    [41.294856568994334, 2.495856897612685], popup="<i>Test Test Test!</i>",
    tooltip=tooltip,
    icon=folium.Icon(color="green", icon="info-sign"),
).add_to(m)

#Read CSV files
#The fill must contain just the values. It will crash if the headers are not removed
#Headers: TEMPERATURA,PRESSURE,ALTITUDE,LATITUDE,LONGITUDE,SPEED,COURSE,TIMERX
#Si es vol es pot modifica el codi per tal que es grafiquin altres valors

with open('Demo_Data.csv') as csvfile:  
    sonda = csv.reader(csvfile, delimiter = ',')
    print(sonda)
    i=0
    for row in sonda:
        #if (row[3]) > 0:
            Temp.append(row[0])
            Pres.append(row[1])
            Alt.append(row[2])
            Lat.append(row[3])
            Lon.append(row[4])
            Vel.append(row[5])
            Course.append(row[6])
            Time.append(row[7])
            print(i)
            print(Lat[i])
            #It can also be in a tuple
            points=list(zip(Lat,Lon))
            #No guardem els valors que tenen coordenades nul·les
            i=i+1
            
    i=0    
    for row in Lat:
        if int(float(Lat[i]))>0:
                coordinatesList.append( [float(Lat[i]) , float(Lon[i])] )
                Course_float.append(float(Course[i]))
                i=i+1
        else:
                i=i+1 #No fem Plot de valors de GPS nuls  
    
    i=0
    for row in Lat:
        if int(float(Lat[i]))>0:
                print("Position: ",i)
                folium.Marker([Lat[i], Lon[i]],
                popup='T(UHT): '+Time[i] + ' Cord: '+ Lat[i] + ','+ Lon[i] ,
                icon=folium.Icon(color="red"),
                tooltip='Velocitat: ' + Vel[i] + ' m/s' + ' | Altitut: ' + Alt[i] + ' m' + ' | Curs: ' + Course[i] + 'º' + 'Temp: ' +Temp[i] + 'Pres: ' + Pres[i]
                    ).add_to(m)
                folium.RegularPolygonMarker([Lat[i], Lon[i]], fill_color='blue', number_of_sides=3, radius=10, rotation=Course[i]).add_to(m)
                i=i+1
        else:
                i=i+1 #No fem Plot de valors de GPS nuls  

#Aquí estem creat una linia que uneix el punts, es pot treure si no acava de fer el pes	
folium.PolyLine(coordinatesList, color="red", weight=2.5, opacity=1).add_to(m)


#Gràfics de presió i temperatura

i=0
for column in Time:
        if int(Time[i][:1])>0: #a vegaes si el dispositiu no te GPS loock ens donarà hores nul·les.
                Time_plot.append(datetime.strptime(Time[i],'%H:%M:%S').time())
                Temperatures.append(float(Temp[i]))
                Pressure.append(float(Pres[i]))
                Alture.append(float(Alt[i]))
                Course_Plot.append(float(Course[i]))
                Velocity_Plot.append(float(Vel[i]))
        else:
                print(Time[i]) #Hora que dona el Error (buscar en en CSV)
        i=i+1

#Grafiquem els diferents valors que em extret del CSV
dataframe_temp = pd.DataFrame({'Time': Time_plot,'Temp': Temperatures})
dataframe_pres = pd.DataFrame({'Time': Time_plot,'Pres': Pressure})
dataframe_alt = pd.DataFrame({'Time': Time_plot,'Alt': Alture})
dataframe_course = pd.DataFrame({'Time': Time_plot,'Course': Course_Plot})
dataframe_vel = pd.DataFrame({'Time': Time_plot,'Vel': Velocity_Plot})

print(Time_plot[0])
print(dataframe_temp)


dataframe_temp.plot( 'Time' , 'Temp' )
plt.ylabel('Temperature º')
plt.grid()

dataframe_pres.plot( 'Time' , 'Pres' )
plt.ylabel('Pressure (Pa)')
plt.grid()

dataframe_alt.plot( 'Time' , 'Alt' )
plt.ylabel('Altitude (m)')
plt.grid()

dataframe_course.plot( 'Time' , 'Course' )
plt.ylabel('Course (º)')
plt.grid()

dataframe_vel.plot( 'Time' , 'Vel' )
plt.ylabel('Velocity (m/s)')
plt.grid()

plt.show()

# Un cop tanquem tots els plots aleshores es pot veure el mapa que es guarda en format html

        
print("Full Recorded Data: ") 
#print(Lat)
#print(Lon)
#print(points)
#print(coordinatesList)
#print(Course)

m.save("GoSTEM_SONDA.html")

print("Map exported into 'GoSTEM_SONDA.html'. Open it in your browser.")
pass
