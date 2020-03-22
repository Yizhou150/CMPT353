import numpy as np
import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier

def classify(str):
    if str in ['college', 'kindergarten', 'language_school', 'library', 'music_school', 'prep_school', 'school', 'science', 'university']:
        return 'edu'
    if str in ['arts_centre',' bar', 'casino', 'cinema', 'clock', 'fountain', 'gambling', 'leisure', 'marketplace', 'nightclub', 'pub', 'spa', 'stripclub', 'theatre']:
        return 'ent'
    if str in ['sanitary_dump_stations', 'trash', 'vacuum_cleaner', 'waste_disposal', 'waste_transfer_station']:
        return 'ind'
    return None

def draw_marker(p, group):
    if p['class'] == 'edu':
        col = 'red'
    if p['class'] == 'ent':
        col = 'green'
    if p['class'] == 'ind':
        col = 'blue'
    group.add_child(
        folium.CircleMarker(
            [p['lat'], p['lon']],
            radius=0.2,
            color=col,
            fill_opacity=0.1
        )
    )

def main():
    in_directory = 'amenities-vancouver.json.gz'
    data = pd.read_json(in_directory, lines=True)

    # pd.set_option('max_columns', 400)
    # pd.set_option('max_row',400)
    # data.groupby('amenity').count()

    # filter the needed data
    data['class'] = data['amenity'].apply(classify)
    new_data = data[data['class'].notna()]

    # draw map
    v_latitude = 49.14
    v_longitude = -123.05
    van_map_c = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')

    # add marker to map
    c_group = folium.map.FeatureGroup()
    new_data.apply(draw_marker, axis=1, group=c_group)
    fig = van_map_c.add_child(c_group)
    fig.save("output_attraction/urban_area.html")

    # try models
    X = new_data[['lat', 'lon']]
    y = new_data['class']
    X_train, X_valid, y_train, y_valid = train_test_split(X, y)

    bayes_model = GaussianNB()
    bayes_model.fit(X_train, y_train)
    print(bayes_model.score(X_valid, y_valid))

    knn_model = KNeighborsClassifier(n_neighbors=7)
    knn_model.fit(X_train, y_train)
    print(knn_model.score(X_valid, y_valid))

    rf_model = RandomForestClassifier(n_estimators=200, max_depth=35, min_samples_leaf=1)
    rf_model.fit(X_train, y_train)
    print(rf_model.score(X_valid, y_valid))
    print('Successfully Create HTML Files in folder output_attraction!')
if __name__ == '__main__':
    main()