import urllib2
from bs4 import BeautifulSoup
import pdb
import requests
import re

def find_in_page_text(page, class_=None, text_=None):
    return page.find(class_, text=text_)

def find_in_page_id(page, class_=None, id_=None):
    return page.find(class_, id = id_)

def go_to_page(url, page, class_=None, text_=None):
    link = page.find(class_, text=text_)
    new_url = url + str(link.get('href'))
    return new_url, BeautifulSoup(urllib2.urlopen(new_url), 'html.parser')

def main():
    ""
    nba_url = 'https://www.basketball-reference.com'
    nba_page = urllib2.urlopen(nba_url)
    nba_site = BeautifulSoup(nba_page, 'html.parser')
    nav_bar = nba_site.find('div', attrs={'id': 'nav'})
    league = nav_bar.find('li', attrs = {'id': 'header_leagues'})
    league_url = nba_url + str(league.find('a').get('href'))
    
    league_page = urllib2.urlopen(league_url)
    league_page= BeautifulSoup(league_page, 'html.parser')
    NBA = find_in_page_text(league_page, 'span', "Seasons")
    NBA_by_year = (NBA.parent.find_all('li'))

    url_by_season = []
    for i in NBA_by_year:
        url_by_season.append(nba_url + str(i.find('a').get('href')))
    print(url_by_season)

    last_year = NBA.parent.find('a', text ="2017-18")
    last_year_url = nba_url + str(last_year.get('href'))
    last_year_page = BeautifulSoup(urllib2.urlopen(last_year_url) , 'html.parser')
    season_url, season_page = go_to_page(nba_url, last_year_page, 'a', "Schedule and Results")
    print(season_url)
    html = requests.get(url_by_season[0]).content
   # last_year_page = BeautifulSoup(urllib2.urlopen(url_by_season[0]), 'lxml')
    last_year_page = BeautifulSoup(re.sub("<!--|-->","", html))
    teams_table = find_in_page_id(last_year_page, "div", "all_team-stats-base")
    teams_table = teams_table.get('tbody').get_all('tr')
    print(teams_table)

    #     l = []
    # for tr in table_rows:
    #     td = tr.find_all('td')
    #     row = [tr.text for tr in td]
    #     l.append(row)
    # pd.DataFrame(l, columns=["A", "B", ...])


if __name__ == '__main__':
    main()
