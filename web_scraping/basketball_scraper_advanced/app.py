# Script to scrape basketball statistics
# Noah Rubin: 2023

from helpers import scrape_bball_stats


def main():
    start = 2002
    end = 2023
    driver_path = '/Users/noahrubin/Desktop/chromedriver'
    data = scrape_bball_stats(start, end, driver_path=driver_path)
    data.to_csv('../datasets/basketball/basketball_data.csv', index=False)
    print("Finished!")

if __name__ == '__main__':
    main()
