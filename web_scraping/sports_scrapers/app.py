import pandas as pd
import numpy as np


def get_url_map(sport='golf'):
    if sport == 'golf':
        url_map = {'official_money': "https://www.pgatour.com/stats/stat.109.y{y}.html",
                   'consecutive_cuts': "https://www.pgatour.com/stats/stat.122.y{y}.html",
                   'longest_drive': 'https://www.pgatour.com/stats/stat.159.y{y}.html',
                   'avg_drive': 'https://www.pgatour.com/stats/stat.101.y{y}.html',
                   'pct_over_300_yards': 'https://www.pgatour.com/stats/stat.454.y{y}.html',
                   'avg_clubhead_speed': 'https://www.pgatour.com/stats/stat.02401.y{y}.html',
                   'avg_ball_speed': 'https://www.pgatour.com/stats/stat.02402.y{y}.html',
                   'gir_pct': 'https://www.pgatour.com/stats/stat.103.{y}.html',
                   'sand_saves_pct': 'https://www.pgatour.com/stats/stat.111.{y}.html',
                   'bogey_pct': 'https://www.pgatour.com/stats/stat.02414.y{y}.html'}
        return url_map
    else: 
        return


def golf_scraper(stats: str):
    datasets = []
    years = np.arange(2010, 2023+1, 1)
    url_map = get_url_map(sport='golf')
    for y in years:
        url = url_map.get(stats).format(y=y)
        temp = pd.read_html(url)[-1]
        temp['Year'] = y
        datasets.append(temp)
    
    return pd.concat(datasets, axis=0)


def main():
    sport = 'golf'  # must be name of folder too
    sport_dict = get_url_map(sport=sport)
    datasets_created = 0
    for key in sport_dict.keys():
        print(f'Collecting Dataset {datasets_created+1}, Sport: {sport}, Statistic: {key}')
        temp = golf_scraper(stats=key)
        temp.to_csv(f'../datasets/{sport}/{key}.csv', index=False)
        datasets_created += 1
        print(f'Files Saved: {datasets_created}')
        
     
if __name__ == '__main__': 
    main()