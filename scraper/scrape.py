from urllib.request import urlopen
from IPython.display import display, HTML
from bs4 import BeautifulSoup, Comment
import pdb
import requests
import re
import pandas as pd

def find_in_page_text(page, class_=None, text_=None):
    return page.find(class_, text=text_)

def find_in_page_id(page, class_=None, id_=None):
    return page.find(class_, id = id_)

def go_to_page(url, page, class_=None, text_=None):
    link = page.find(class_, text=text_)
    new_url = url + str(link.get('href'))
    return new_url, BeautifulSoup(urlopen(new_url), 'html.parser')

def main():
    ""
    nba_url = 'https://www.basketball-reference.com'
    nba_page = urlopen(nba_url)
    nba_site = BeautifulSoup(nba_page, 'html.parser')
    nav_bar = nba_site.find('div', attrs={'id': 'nav'})
    league = nav_bar.find('li', attrs = {'id': 'header_leagues'})
    league_url = nba_url + str(league.find('a').get('href'))
    
    league_page = urlopen(league_url)
    league_page= BeautifulSoup(league_page, 'html.parser')
    NBA = find_in_page_text(league_page, 'span', "Seasons")
    NBA_by_year = (NBA.parent.find_all('li'))

    url_by_season = []
    for i in NBA_by_year:
        url_by_season.append(nba_url + str(i.find('a').get('href')))

    last_year = NBA.parent.find('a', text ="2017-18")
    last_year_url = nba_url + str(last_year.get('href'))
    last_year_page = BeautifulSoup(urlopen(last_year_url) , 'html.parser')
    season_url, season_page = go_to_page(nba_url, last_year_page, 'a', "Schedule and Results")
    # URL page we will scraping (see image above)
    year=2018
    url = "https://www.basketball-reference.com/leagues/NBA_{}_per_game.html".format(year)

# this is the HTML from the given URL
    html = urlopen(url)

    soup = BeautifulSoup(html)
    # use findALL() to get the column headers
    soup.findAll('tr', limit=2)

# use getText()to extract the text we need into a list
    headers = [th.getText() for th in soup.findAll('tr', limit=2)[0].findAll('th')]

# exclude the first column as we will not need the ranking order from Basketball Reference for the analysis
    headers = headers[1:]
    rows = soup.findAll('tr')[1:]
    player_stats = [[td.getText() for td in rows[i].findAll('td')] \
            for i in range(len(rows))]
    stats = pd.DataFrame(player_stats, columns = headers)
    stats.head(10)
    print(stats)
    #print(last_year_page.find("div", id="all_team-stats-base").find("div", class_="table_outer_container"))

    #for comment in last_year_page.find_all(string=lambda text:isinstance(text,Comment)):
    #    data = BeautifulSoup(comment,"html5lib")
    ##    for items in data.select("table.row_summable tr"):
    #        tds = [item.get_text(strip=True) for item in items.select("th,td")]
    #        print(tds)
    #comments = last_year_page.findAll(text=lambda text:isinstance(text, Comment))
    #for comment in comments:
    #    comment.extract()
    #pdb.set_trace()
    #teams_table = find_in_page_id(last_year_page, "table", "team-stats-base")
    #teams_table = teams_table.get('tbody').get_all('tr')
    #print(teams_table.prettify())

    #     l = []
    # for tr in table_rows:
    #     td = tr.find_all('td')
    #     row = [tr.text for tr in td]
    #     l.append(row)
    # pd.DataFrame(l, columns=["A", "B", ...])


if __name__ == '__main__':
    main()
