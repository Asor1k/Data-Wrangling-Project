import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import matplotlib.patches as patches
import pandas as pd
import geopandas as gpd
from highlight_text import fig_text

greenhouse_file = 'greenhouse-emissions.csv'
renewable_energy_share_file = 'renewable-share-energy.csv'

# Reading the files
greenhouse_emissions_data = pd.read_csv(greenhouse_file)
renewable_energy_share_data = pd.read_csv(renewable_energy_share_file)


def show_renewable_energy_for_year(year, renewable_energy_share_data):
    # Filtering the data on the year to display on the map
    renewable_energy_amount = renewable_energy_share_data[renewable_energy_share_data['Year'] == year]['Renewables (% equivalent primary energy)']
    renewable_energy_countries = renewable_energy_share_data[renewable_energy_share_data['Year'] == year]['Entity']

    re_df = pd.DataFrame({'Country': renewable_energy_countries, 'Renewables': renewable_energy_amount})

    # Displaying the map
    world = gpd.read_file("./map/ne_110m_admin_0_countries.shp")
    europe = world[world['CONTINENT'] == 'Europe']

    data = europe.merge(re_df, how='left', left_on='NAME', right_on='Country')

    fig, ax = plt.subplots(1, 1, figsize=(8, 8))
    
    # define colors
    cmap = cm.Greens
    min_rate, max_rate = 0, 100
    norm = mcolors.Normalize(vmin=min_rate, vmax=max_rate)

    # create the plot
    data.plot(column='Renewables', cmap=cmap, norm=norm, ax=ax)

    # custom axis
    ax.set_xlim(-15, 35)
    ax.set_ylim(32, 72)
    ax.axis('off')

    # add a title
    fig.text(0.2, 0.75, 'Has a doctor ever told you\nthat you had a cancer?',
         fontsize=22, fontweight='bold', fontfamily='serif')


    data_projected = data.to_crs(epsg=3035)
    data_projected['centroid'] = data_projected.geometry.centroid
    data['centroid'] = data_projected['centroid'].to_crs(data.crs)
    
    adjustments = {
        'France': (9, 3),
        'Italy': (-2.4, 2),
        'Lithuania': (0, -0.6),
        'Finland': (0, -2.5),
        'Romania': (0, -0.5),
        'Bulgaria': (0, -0.6),
        'Greece': (-1.2, -0.8),
        'Croatia': (0, -1),
        'Cyprus': (0, -1),
        'Ireland': (0, -1),
        'Malta': (0, -1),
        'Slovenia': (0, -1),
        'Slovakia': (-0.7, -0.8),
        'Estonia': (0, -0.7),
        'Latvia': (0, -0.5),
        'Belgium': (0, -0.7),
        'Austria': (0, -1),
        'Spain': (0, -1),
        'Portugal': (-0.5, -1),
        'Luxembourg': (0, -1),
        'Germany': (-0.2, 0),
        'Hungary': (-0.3, -1),
        'Czechia': (0, -1),
        'Poland': (0, -1),
        'Sweden': (-1.5, -1),
        'Denmark': (0, -1),
        'Netherlands': (0, 0),
        'United Kingdom': (0, -1),
        'Switzerland': (0, -0.5),
    }


    for country in data['Country']:
        if country != country:
            continue
        print(country)
        # get centroid
        centroid = data.loc[data['NAME'] == country, 'centroid'].values[0]
        x, y = centroid.coords[0]

        # get corrections
        x += adjustments[country][0]
        y += adjustments[country][1]

        # get rate and annotate
        rate = round(data.loc[data['NAME'] == country, 'Renewables'].values[0], 2)
        ax.annotate(f'{country} {rate}%', (x, y), textcoords="offset points", xytext=(5, 5),
                    ha='center', fontsize=5, fontfamily='DejaVu Sans', color='black')

    # display the plot
    plt.tight_layout()
    plt.show()



show_renewable_energy_for_year(2020, renewable_energy_share_data)
