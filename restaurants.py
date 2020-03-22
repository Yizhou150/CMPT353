import pandas as pd
import folium
from folium import plugins
from folium.plugins import HeatMap
import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns


def check_chain(name, list_r, list_f, list_p, list_c):
    tempr = list_r[list_r['restaurantLabel'].str.contains(str(name))]
    tempf = list_f[list_f['fast_foodLabel'].str.contains(str(name))]
    tempp = list_p[list_p['pizzeriaLabel'].str.contains(str(name))]
    tempc = list_c[list_c['cafeLabel'].str.contains(str(name))]
    if not tempr.empty:
        return tempr['restaurantLabel'].iloc[0]
    if not tempf.empty:
        return tempf['fast_foodLabel'].iloc[0]
    if not tempp.empty:
        return tempp['pizzeriaLabel'].iloc[0]
    if not tempc.empty:
        return tempc['cafeLabel'].iloc[0]
    return "NotChain"


def get_num(name, df):
    return df['num'].loc[name]


def draw_marker(p, foods, col):
    foods.add_child(
        folium.CircleMarker(
            [p['lat'], p['lon']],
            radius=0.2,
            color=col,
            fill_opacity=0.1
        )
    )


def draw_cluster(p, foods):
    folium.Marker(
        location=[p['lat'], p['lon']],
        icon=None
        # popup=p['label']
    ).add_to(foods)


def main():
    # read the data
    in_directory = 'amenities-vancouver.json.gz'
    data = pd.read_json(in_directory, lines=True)
    restaurants = data[
        (data['amenity'] == 'restaurant') | (data['amenity'] == 'fast_food') | (data['amenity'] == 'cafe')]
    res = pd.read_json('restaurant.json')
    fas = pd.read_json('fast_food.json')
    piz = pd.read_json('pizzeria.json')
    caf = pd.read_json('cafe.json')

    # process and split the data
    Unknown = restaurants[restaurants['name'].isnull()]
    restaurants = restaurants[~restaurants['name'].isnull()]
    restaurants['chain'] = restaurants['name'].apply(check_chain, list_r=res, list_f=fas, list_p=piz, list_c=caf)

    chains1 = restaurants[restaurants['chain'] != 'NotChain']  # 960
    Notchains1 = restaurants[restaurants['chain'] == 'NotChain']

    Notchains1 = Notchains1.assign(num=1)
    nc_group = Notchains1.groupby('name').count()
    Notchains1['num'] = Notchains1['name'].apply(get_num, df=nc_group)

    chains2 = Notchains1[Notchains1['num'] > 1]  # 711

    nchains = Notchains1[Notchains1['num'] == 1]
    chains = pd.concat([chains1[['amenity', 'lat', 'lon', 'name']], chains2[['amenity', 'lat', 'lon', 'name']]], axis=0)

    # analyze the data

    # draw distribution
    v_latitude = 49.14
    v_longitude = -123.05
    van_map_chains1 = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')
    van_map_chains2 = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')
    van_map_nchains = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')

    chain1_group = folium.map.FeatureGroup()
    chains1.apply(draw_marker, axis=1, foods=chain1_group, col='red')
    fig = van_map_chains1.add_child(chain1_group)
    fig.save("output_restaurant/chains_in_wikidata.html")

    chain2_group = folium.map.FeatureGroup()
    chains2.apply(draw_marker, axis=1, foods=chain2_group, col='green')
    fig = van_map_chains2.add_child(chain2_group)
    fig.save("output_restaurant/chains_notin_wikidata.html")

    nchain_group = folium.map.FeatureGroup()
    nchains.apply(draw_marker, axis=1, foods=nchain_group, col='blue')
    fig = van_map_nchains.add_child(nchain_group)
    fig.save("output_restaurant/nonchains.html")


    # draw cluster
    van_map_chains_cluster = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')
    van_map_nchains_cluster = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')

    chain_cluster = plugins.MarkerCluster().add_to(van_map_chains_cluster)
    nchain_cluster = plugins.MarkerCluster().add_to(van_map_nchains_cluster)

    chains.apply(draw_cluster, axis=1, foods=chain_cluster)
    fig = van_map_chains_cluster.add_child(chain_cluster)
    fig.save("output_restaurant/chains_cluster.html")

    nchains.apply(draw_cluster, axis=1, foods=nchain_cluster)
    fig = van_map_nchains_cluster.add_child(nchain_cluster)
    fig.save("output_restaurant/nonchains_cluster.html")

    # draw heat map
    van_map_chains_heat = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')
    van_map_nchains_heat = folium.Map(location=[v_latitude, v_longitude], zoom_start=10, tiles='OpenStreetMap')

    heatchain = chains[['lat', 'lon']].values.tolist()
    fig = HeatMap(heatchain).add_to(van_map_chains_heat)
    fig.save("output_restaurant/chains_heat.html")

    heatnchain = nchains[['lat', 'lon']].values.tolist()
    fig = HeatMap(heatnchain).add_to(van_map_nchains_heat)
    fig.save("output_restaurant/nonchains_heat.html")

    # stats analysis
    plt.figure(figsize=(12, 7))
    plt.subplot(2, 2, 1)
    plt.hist(chains['lon'])
    plt.title('distribution of chains along lonitude')
    plt.subplot(2, 2, 2)
    plt.hist(nchains['lon'])
    plt.title('distribution of non-chains along lonitude')
    plt.subplot(2, 2, 3)
    plt.hist(chains['lat'])
    plt.title('distribution of chains along latitude')
    plt.subplot(2, 2, 4)
    plt.hist(nchains['lat'])
    plt.title('distribution of chains along latitude')
    plt.plot()
    plt.savefig("output_restaurant/distribution_along_latitude_longitude.jpg")

    c_sample = chains.sample(n=500)
    n_sample = nchains.sample(n=500)

    lon_levene_p = stats.levene(c_sample['lon'], n_sample['lon']).pvalue
    lat_levene_p = stats.levene(c_sample['lat'], n_sample['lat']).pvalue
    print("--------------------statistic data------------------------")
    print("equal varible test:")
    print("longitude p value: ",lon_levene_p)
    print("latitude p value: ", lat_levene_p)

    print("stds: ")
    print("chains longitude std: ", chains['lon'].std(), ", non-chains longitude std: ", nchains['lon'].std())
    print("chains latitude std: ", chains['lat'].std(), ", non-chains latitude std: ", nchains['lat'].std())

    print("Mann-Whitney Utest:")
    print("longitude p value: ", stats.mannwhitneyu(c_sample['lon'], n_sample['lon'], alternative='two-sided').pvalue)
    print("latitude p value: ", stats.mannwhitneyu(c_sample['lat'], n_sample['lat'], alternative='two-sided').pvalue)

    print("means:")
    print("chains longitude mean: ", chains['lon'].mean(), ", non-chains longitude mean: ", nchains['lon'].mean())
    print("chains latitude mean: ", chains['lat'].mean(), ", non-chains latitude mean: ", nchains['lat'].mean())

    # density visualization
    sns.set(style='darkgrid', color_codes=True)
    fig = sns.jointplot(x="lon", y="lat", kind='kde', data=chains, color='red', ratio=6)
    fig.savefig('output_restaurant/chains_kde.png')

    sns.set(style='darkgrid', color_codes=True)
    fig = sns.jointplot(x="lon", y="lat", kind='kde', data=nchains, color='red', ratio=6)
    fig.savefig('output_restaurant/nonchains_kde.png')
    print('Successfully Create HTML Files in folder output_restaurant!')
if __name__ == '__main__':
    main()