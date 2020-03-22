import folium
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.cluster import KMeans

def time_extract(t):
    a = t[0:10] +'-'+t[11:19]
    return a


data = pd.read_json('amenities-vancouver.json.gz', lines=True)
data['timestamp'] = data['timestamp'].apply(time_extract)
data['date'] = pd.to_datetime(data['timestamp'],format = '%Y-%m-%d-%H:%M:%S')
data['day'] = data['date'].map(lambda x: x.strftime('%Y-%m-%d'))

bike = data[(data['amenity'] == 'bicycle_parking')|(data['amenity'] == 'bicycle_rental')]
car = data[(data['amenity'] == 'car_sharing')|(data['amenity'] == 'parking')]
bus = data[data['amenity'] == 'bus_station']

parks = pd.read_csv('parks.csv')
parks = parks[['Name','GoogleMapDest']]
parks[['lat','lon']]= parks['GoogleMapDest'].str.split(',',expand = True)
parks = parks.assign(amenity='park')
parks = parks[['Name','amenity','lat','lon']]
parks.rename(columns={'Name':'name'},inplace=True)

arts_centre = data[data['amenity'] == 'arts_centre']
cinema = data[data['amenity'] == 'cinema']
college = data[data['amenity'] == 'college']
theatre = data[data['amenity'] == 'theatre']

data_good_place = data[(data['amenity']=='arts_centre')|(data['amenity']=='cinema')|(data['amenity']=='college')|(data['amenity']=='theatre')]
data_good_place = data_good_place[['name','amenity','lat','lon']]
data_good_place = pd.concat([data_good_place,parks])

transportation = data[(data['amenity']=='arts_centre')|(data['amenity']=='cinema')|(data['amenity']=='college')|(data['amenity']=='theatre')]

def draw_point_DBSCAN(df,eps,min_sap):
    X = df[['lat','lon']]
    y = DBSCAN(eps=eps, min_samples=min_sap).fit(X)
    df = df.copy()
    df['class'] = y.labels_
    van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
    ys =['#6699CC','#FF9900','#FF6666','#6600FF','#990000',
         '#057748','#7c4b00','#FF0066','#99CC00','#996633',
         '#116633','#19CAAD','#D1BA74','#A0EEE1','#BEEDC7',
         '#226633','#14ABCD','#85B444','#A25E11','#BC2227',
         '#61111C','#F22220','#F55556','#64444F','#977770',
         '#557AB8','#3c4430','#2F0036','#19CBAD','#933333',
         '#69CA33','#39CB8D','#C9BC84','#B8AAA1','#A65674',
         '#316243','#1361BD','#631444','#CDEE23','#DE2227',]
    entertain = folium.map.FeatureGroup()
    for i in range(max(df['class'])):
        df[df['class'] == i].apply(draw_marker, axis=1, m=entertain, color = ys[i])
    return van_map.add_child(entertain)

def draw_point_KMeans(df):
    model = KMeans(n_clusters=30)
    X = df[['lat','lon']]
    y = model.fit_predict(X)
    df = df.copy()
    df['class'] = y
    van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
    ys =['#6699CC','#FF9900','#FF6666','#6600FF','#990000',
         '#057748','#7c4b00','#FF0066','#99CC00','#996633',
         '#116633','#19CAAD','#D1BA74','#A0EEE1','#BEEDC7',
         '#226633','#14ABCD','#85B444','#A25E11','#BC2227',
         '#61111C','#F22220','#F55556','#64444F','#977770',
         '#557AB8','#3c4430','#2F0036','#19CBAD','#933333',
         '#69CA33','#39CB8D','#C9BC84','#B8AAA1','#A65674',
         '#316243','#1361BD','#631444','#CDEE23','#DE2227',]
    entertain = folium.map.FeatureGroup()
    for i in range(max(df['class'])):
        df[df['class'] == i].apply(draw_marker, axis=1, m=entertain, color = ys[i])
    return van_map.add_child(entertain)

def draw_marker(p, m, color):
    m.add_child(
        folium.CircleMarker(
            [p['lat'], p['lon']],
            radius=1,
            color=color,
        )
    )


fig = draw_point_DBSCAN(data, 0.0005, 20)
fig.save('output_tour/Total data with DBSCAN.html')

fig = draw_point_DBSCAN(data_good_place, 0.005, 5)
fig.save('output_tour/Manual Filter and DBSCAN.html')

van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
entertain = folium.map.FeatureGroup()
bike[bike['amenity'] == 'bicycle_parking'].apply(draw_marker, axis=1, m=entertain, color = '#6699CC')
bike[bike['amenity'] == 'bicycle_rental'].apply(draw_marker, axis=1, m=entertain, color = '#FF9900')
fig = van_map.add_child(entertain)
fig.save('output_tour/bike.html')


van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
entertain = folium.map.FeatureGroup()
car[car['amenity'] == 'car_sharing'].apply(draw_marker, axis=1, m=entertain, color = '#FF9900')
car[car['amenity'] == 'parking'].apply(draw_marker, axis=1, m=entertain, color = '#6699CC')
fig = van_map.add_child(entertain)
fig.save('output_tour/car.html')


van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
entertain = folium.map.FeatureGroup()
bus.apply(draw_marker, axis=1, m=entertain, color = '#6600FF')
fig = van_map.add_child(entertain)
fig.save('output_tour/bus.html')
    
print('Successfully Create HTML Files in folder output_tour!')