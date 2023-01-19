import pandas as pd
import numpy as np


def get_url_map(sport: str):
    if sport == 'golf':
        # Some taken from espn and some from the pga tour
        url_map = {'general_stats': 'https://www.espn.com/golf/stats/player/_/season/{y}',
                   'official_money': "https://www.pgatour.com/stats/stat.109.y{y}.html",
                   'consecutive_cuts': "https://www.pgatour.com/stats/stat.122.y{y}.html",
                   'longest_drive': 'https://www.pgatour.com/stats/stat.159.y{y}.html',
                   'avg_drive': 'https://www.pgatour.com/stats/stat.101.y{y}.html',
                   'pct_over_300_yards': 'https://www.pgatour.com/stats/stat.454.y{y}.html',
                   'avg_clubhead_speed': 'https://www.pgatour.com/stats/stat.02401.y{y}.html',
                   'avg_ball_speed': 'https://www.pgatour.com/stats/stat.02402.y{y}.html',
                   'gir_pct': 'https://www.pgatour.com/stats/stat.103.{y}.html',
                   'sand_saves_pct': 'https://www.pgatour.com/stats/stat.111.{y}.html',
                   'bogey_pct': 'https://www.pgatour.com/stats/stat.02414.y{y}.html'}

    elif sport == 'basketball': 
        url_map = {'regular_season_individual': 'https://www.espn.com/nba/stats/player/_/season/{y}/seasontype/2',
                   'regular_season_team': 'https://www.espn.com/nba/stats/team/_/season/{y}/seasontype/2',
                   'post_season_individual': 'https://www.espn.com/nba/stats/player/_/season/{y}/seasontype/3',
                   'post_season_team': 'https://www.espn.com/nba/stats/team/_/season/{y}/seasontype/3'}

    elif sport == 'baseball': 
        url_map = {'regular_season_batting': 'https://www.espn.com/mlb/stats/player/_/season/{y}/seasontype/2',
                   'regular_season_pitching': 'https://www.espn.com/mlb/stats/player/_/view/pitching/season/{y}/seasontype/2',
                   'regular_season_fielding': 'https://www.espn.com/mlb/stats/player/_/view/fielding/season/{y}/seasontype/2',
                   'post_season_batting': 'https://www.espn.com/mlb/stats/player/_/season/{y}/seasontype/3',
                   'post_season_pitching': 'https://www.espn.com/mlb/stats/player/_/view/pitching/season/{y}/seasontype/3',
                   'post_season_fielding': 'https://www.espn.com/mlb/stats/player/_/view/fielding/season/{y}/seasontype/3'}
    
    elif sport == 'ice_hockey':
        url_map = {'regular_season_skating': 'https://www.espn.com/nhl/stats/player/_/season/{y}/seasontype/2',
                   'regular_season_goaltending': 'https://www.espn.com/nhl/stats/player/_/view/goaltending/season/2022/seasontype/2',
                   'post_season_skating': 'https://www.espn.com/nhl/stats/player/_/season/{y}/seasontype/3',
                   'post_season_goaltending': 'https://www.espn.com/nhl/stats/player/_/view/goaltending/season/2022/seasontype/3'}
    
    elif sport == 'nfl':
        # Add defense, sciring and special teams 
        url_map = {'regular_season_offense_passing': 'https://www.espn.com/nfl/stats/player/_/stat/passing/season/{y}/seasontype/2',
                   'regular_season_offense_rushing': 'https://www.espn.com/nfl/stats/player/_/stat/rushing/season/{y}/seasontype/2',
                   'regular_season_offense_receiving': 'https://www.espn.com/nfl/stats/player/_/stat/receiving/season/{y}/seasontype/2',
                   'post_season_offense_passing': 'https://www.espn.com/nfl/stats/player/_/stat/passing/season/{y}/seasontype/3',
                   'post_season_offense_rushing': 'https://www.espn.com/nfl/stats/player/_/stat/rushing/season/{y}/seasontype/3',
                   'post_season_offense_receiving': 'https://www.espn.com/nfl/stats/player/_/stat/receiving/season/{y}/seasontype/3'}
    else: 
        return "Please enter a valid sport. Choose from: ['golf', 'basketball', 'baseball', 'ice_hockey', 'nfl']"
    
    return url_map


def sport_scraper(sport: str, stat: str, start_year: int, cutoff_year: int):
    datasets = []

    # Just so we know we have data for sports where the 2023 season has not started yet
    
    years = [y for y in range(start_year, cutoff_year+1, 1)]
    url_map = get_url_map(sport=sport)
    for y in years:
        url = url_map.get(stat)
        tables = pd.read_html(url.format(y=y))

        # For tables from the pga tour website, the first table is useless
        tables = tables if 'www.pgatour.com' not in url else [tables[-1]]
        
        temp = pd.concat([t for t in tables], axis=1)
        temp['Year'] = y
        datasets.append(temp)
    
    return pd.concat(datasets, axis=0)


def main():
    # TODO: if else statements to ensure start year and end year are valid. Maybe a helper function called check_years(start, end)
    start_year = 2010
    cutoff_year = 2022
    
    dataset_num = 0
    files_successfully_saved = 0
    
    sport = 'nfl'
    sport_dict = get_url_map(sport=sport)
    for key in sport_dict.keys():
        path = f'../datasets/{sport}/{key}.csv'
        try: 
            print(f'Collecting Dataset {dataset_num+1}, Sport: {sport}, Statistic: {key}')
            temp = sport_scraper(sport=sport, stat=key, start_year=start_year, cutoff_year=cutoff_year)
            temp.to_csv(path, index=False)
            files_successfully_saved += 1
        except ImportError: 
            print(f'Unable to download Dataset directed to {path}')
        
        dataset_num += 1
        print(f'Files Saved: {files_successfully_saved}\n')
        
        
if __name__ == '__main__': 
    main()