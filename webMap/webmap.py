import folium 
import pandas

data = pandas.read_excel("iit_data.xlsx")

iit_ranking = list(data["IIT Ranking"])
college_name = list(data["IIT College"])
nirf_score = list(data["NIRF Score"])
lat = list(data["Latitude"])
lon = list(data["Longitude"])
pic = list(data["Image"])

fg = folium.FeatureGroup('map')
fg.add_child(folium.GeoJson(data = (open("india_states.json","r",encoding = "utf-8-sig").read())))
for rank, name, score, lati, longi, ima in zip(iit_ranking, college_name, nirf_score, lat, lon, pic):
    fg.add_child(folium.Marker(location=[lati, longi], 
                               popup="<b>College Name : </b>" + str(name) +
                                     "<br> <b> Rank among IIT in India : </b>" + str(rank) +
                                     "<br> <img src='" + ima + "' height='145' width='300'>", 
                               icon=folium.Icon(color="red")))

map = folium.Map(location = [20.000,75.000],zoom_start = 4)

map.add_child(fg)
map.save("India.html")