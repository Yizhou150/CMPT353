import folium
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from folium import plugins
from sklearn.cluster import KMeans


data = pd.read_json('amenities-vancouver.json.gz', lines=True)
bar = data[data['amenity']=='bar']
cafe = data[data['amenity']=='cafe']
car_sharing = data[data['amenity']=='car_sharing']
clinic = data[data['amenity']=='clinic']
doctors = data[data['amenity']=='doctors']
fast_food = data[data['amenity']=='fast_food']
pub = data[data['amenity']=='pub']
restaurant = data[data['amenity']=='restaurant']
bike = data[data['amenity'] == '']
bench = data[data['amenity'] == 'bench']
amenities = ['bar','cafe','car_sharing','clinic','doctors','fast_food','pub','restaurants']
data_all = data[(data['amenity']=='bar')|(data['amenity']=='cafe')|(data['amenity']=='car_sharing')|(data['amenity']=='clinic')|(data['amenity']=='doctors')|(data['amenity']=='fast_food')|(data['amenity']=='pub')|(data['amenity']=='restaurant')]

# Draw something
a = data_all.groupby('amenity').count().reset_index()
sns.set()
pic = sns.barplot(a['amenity'],a['lat'])
plt.xticks(rotation=0)
plt.title('Amenity Count',fontsize = 18)
plt.savefig('output_hotel/pic1', dpi = 300)

# Airbnb Data
airbnb_data = pd.read_csv('listings.csv.gz',parse_dates =['last_review'] )
airbnb_data = airbnb_data[airbnb_data['last_review']>'2019-1-1']
airbnb_data = airbnb_data[['id','latitude','longitude','price','minimum_nights','reviews_per_month']]
airbnb_data.rename(columns={'longitude':'lon'},inplace=True)
airbnb_data.rename(columns={'latitude':'lat'},inplace=True)
airbnb_data.rename(columns={'reviews_per_month':'reviews_rate'},inplace=True)
airbnb_data = airbnb_data[airbnb_data['minimum_nights']<=2]

def draw_marker(p, m, color):
    m.add_child(
        folium.CircleMarker(
            [p['lat'], p['lon']],
            radius=1,
            color=color
        )
    )

def draw_cluster(p, m):
    folium.Marker(
        location=[p['lat'], p['lon']],
        icon=None,
    ).add_to(m)

def draw_point_cluster_one_amenity(df):
    model = KMeans(n_clusters=7)
    X = df[['lat','lon']]
    y = model.fit_predict(X)
    df = df.copy()
    df['class'] = y
    van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
    ys =['#FF6666','#6600FF','#990000','#057748','#7c4b00','#FF0066','#99CC00']
    entertain = folium.map.FeatureGroup()
    for i in range(max(df['class'])):
        df[df['class'] == i].apply(draw_marker, axis=1, m=entertain, color = ys[i])
    return van_map.add_child(entertain)

def draw_point_cluster_all_amenity(df):
    van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
    ys =['#6699CC','#FF9900','#FF6666','#6600FF','#990000','#057748','#7c4b00','#FF0066','#99CC00']
    #ys = ['red', 'blue', 'green', 'purple', 'orange', 'darkred', 'lightred', 'beige']
    entertain = folium.map.FeatureGroup()
    for i in range(7):
        df[df['amenity'] == amenities[i]].apply(draw_marker, axis=1, m=entertain, color = ys[i])
    return van_map.add_child(entertain)

def draw_quntity_cluster(df):
    van_map = folium.Map(location=[49.14, -123.05], zoom_start=10)
    cluster = plugins.MarkerCluster().add_to(van_map)
    df.apply(draw_cluster, axis=1, m=cluster)
    return van_map.add_child(cluster)

fig = draw_point_cluster_one_amenity(airbnb_data)
fig.save('output_hotel/Airbnb_Data_Point.html')
fig = draw_quntity_cluster(airbnb_data)
fig.save('output_hotel/Airbnb_Data_Quntity.html')
fig = draw_point_cluster_all_amenity(data_all)
fig.save('output_hotel/Draw_All_Special_Amenities.html')
fig = draw_point_cluster_one_amenity(data[data['amenity'] == 'clinic'])
fig.save('output_hotel/amenity_clinic.html')

print('Successfully Create HTML Files in folder output_hotel!')