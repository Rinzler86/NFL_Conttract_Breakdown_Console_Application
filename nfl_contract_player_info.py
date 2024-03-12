import pandas as pd
import csv
import requests
from bs4 import BeautifulSoup
import re

# Global for Access and updating for use with multiple classes depending on the situation
player_contract_dict = {}


class NFL_Player_Stats:
    """Class with 2 methods, the first method gets data from input variable called in main and passes that data into a url request variable along with
       designated URL, URl is then converted to usable HTML data with web scraper module BeautifulSoup, Headers for CSV are set and all stats are gathered
       from SOUP variable(html data) tracker variables are used to track interations in for loops and written to proper Header sections in newly created
       CSV file, list is then cleared pandas module is used to display data cleanly in method print_dataframe"""

    def players_statistics(self, year):
        """collects data based on year variable passed, parses data, extracts necessary data and assigns it to CSV file to align with corresponding header"""
        global player_contract_dict

        # Constants
        # Enter any year from 1970 and above
        YEAR = f'{year}'
        URL = requests.get(f'https://www.nfl.com/stats/player-stats/category/passing/{YEAR}/post/all/passingyards/desc',
                           'html.parser', timeout=60)
        SOUP = BeautifulSoup(URL.text, features="html5lib")
        HEADER = ['Player', 'Pass Yds', 'Yds/Att', 'Att', 'Comp', 'Comp%', 'TD',
                  'INT', 'Rate', '1st', '1st%', '20+', '40+', 'Lng', 'Sck', 'Pay']
        PLAYER_STATS = SOUP.find_all('td')
        TRACKER = 0
        TRACKER_2 = 0

        # temporarily stores organized data from SOUP
        player_row = []

        # clears csv file to be rewritten
        with open('player_stats.csv', mode='w') as csv_file:
            writer = csv.DictWriter(csv_file, fieldnames=HEADER)

        # for loop runs through all data in PLAYER_STATS, nested if statement checks that iteration is below 15 and maps each data point
        # to the correct header section in the csv, if TRACKER is on 0 then the blank space is stripped from the name(error from data collection)
        # next if statement to see if year is less than 2020, if so it only loads stats gathered from nfl website, if greater than 2020
        # then the pay header is populated from another scraped website and errors are checked using exception handling, then the data is cleared
        # from player_row list and tracker is set back to 0
        for stat in PLAYER_STATS:
            if TRACKER < 15:
                if TRACKER == 0:
                    remove_space = stat.text.strip(" ")
                    for player in player_contract_dict.items():
                        if remove_space in player:
                            if int(year) < 2020:
                                player_row.append("N/A")
                            else:
                                player_row.append(int(player[1]))

                    player_row.append(remove_space)
                    TRACKER += 1
                else:
                    player_row.append(stat.text)
                    TRACKER += 1
            else:
                with open('player_stats.csv', mode='a') as csv_file:
                    writer = csv.DictWriter(csv_file, fieldnames=HEADER)
                    if TRACKER_2 == 0:
                        writer.writeheader()
                        try:
                            writer.writerow({'Pay': player_row[0], 'Player': player_row[1], 'Pass Yds': player_row[2],
                                             'Yds/Att': player_row[3], 'Att': player_row[4], 'Comp': player_row[5],
                                             'Comp%': player_row[6],
                                             'TD': player_row[7], 'INT': player_row[8], 'Rate': player_row[9],
                                             '1st': player_row[10],
                                             '1st%': player_row[11], '20+': player_row[12], '40+': player_row[13],
                                             'Lng': player_row[14],
                                             'Sck': player_row[15]})
                            TRACKER_2 += 1
                        except IndexError:
                            writer.writerow({'Player': player_row[0], 'Pass Yds': player_row[1],
                                             'Yds/Att': player_row[2], 'Att': player_row[3], 'Comp': player_row[4],
                                             'Comp%': player_row[5],
                                             'TD': player_row[6], 'INT': player_row[7], 'Rate': player_row[8],
                                             '1st': player_row[9],
                                             '1st%': player_row[10], '20+': player_row[11], '40+': player_row[12],
                                             'Lng': player_row[13], 'Sck': player_row[14], 'Pay': 0})
                            TRACKER_2 += 1
                    else:
                        try:
                            writer.writerow({'Pay': player_row[0], 'Player': player_row[1], 'Pass Yds': player_row[2],
                                             'Yds/Att': player_row[3], 'Att': player_row[4], 'Comp': player_row[5],
                                             'Comp%': player_row[6],
                                             'TD': player_row[7], 'INT': player_row[8], 'Rate': player_row[9],
                                             '1st': player_row[10],
                                             '1st%': player_row[11], '20+': player_row[12], '40+': player_row[13],
                                             'Lng': player_row[14],
                                             'Sck': player_row[15]})
                        except:
                            writer.writerow({'Player': player_row[0], 'Pass Yds': player_row[1],
                                             'Yds/Att': player_row[2], 'Att': player_row[3], 'Comp': player_row[4],
                                             'Comp%': player_row[5],
                                             'TD': player_row[6], 'INT': player_row[7], 'Rate': player_row[8],
                                             '1st': player_row[9],
                                             '1st%': player_row[10], '20+': player_row[11], '40+': player_row[12],
                                             'Lng': player_row[13], 'Sck': player_row[14], 'Pay': 0})

                player_row.clear()
                TRACKER = 0

    def print_dataframe(self):
        """prints CSV cleanly in console"""
        df = pd.read_csv('player_stats.csv')
        df.to_csv("to_test.csv", index=False, header=True)

        print(df)


class NFL_Player_Pay:
    """gathers data via webscraping from sporttrac website for player salary, for loop then removes dollar signs and commas so data can be converted to
       a int, name and pay are then entered into dictionary(name is key and pay is value) name text is matched from data in statistics list and mapped
       appropriately"""

    def player_contracts(self, year):
        global player_contract_dict
        YEAR = f'{year}'
        URL = requests.get(f'https://www.spotrac.com/nfl/rankings/{YEAR}/average/quarterback/', timeout=60)
        SOUP = BeautifulSoup(URL.text, features="html5lib")

        player_name = SOUP.find_all(class_='team-name')

        index_ = 0
        player_pay = SOUP.find_all(class_='info')
        for pay in player_pay:
            remove_dollar_sign = str(pay.text.strip("$"))
            remove_commas = re.sub(',', '', remove_dollar_sign)
            convert_to_int = int(remove_commas)
            player_contract_dict[f"{player_name[index_].text}"] = convert_to_int

            index_ += 1


class Pay_Per_Play:
    """displays pay per play statistics, math is used to determine what is displayed"""

    def gather(self):
        with open('player_stats.csv', mode='r') as file:
            f = file.readlines()
            counter = 0
            for i in f:
                if len(i) > 2:
                    # elimates the header from being displayed
                    if "Player,Pass Yds,Yds/Att,Att,Comp,Comp%,TD,INT,Rate,1st,1st%,20+,40+,Lng,Sck,Pay" in i:
                        pass
                    else:
                        temp_list = i.split(",")
                        # print(temp_list)
                        player_name = temp_list[0]
                        player_pay = round(int(temp_list[15].split("\n")[0]), 2)
                        pay_per_yard = round(player_pay / int(temp_list[1]), 2)
                        pay_per_attempt = round(player_pay / int(temp_list[3]), 2)
                        pay_per_completion = round(player_pay / int(temp_list[4]), 2)
                        pay_per_TD = round(player_pay / int(temp_list[6]), 2)
                        print(f"{player_name.upper()} Pay Per Play Chart:\n"
                              f"Total Pay: ${player_pay:,}\nPer Yard: ${pay_per_yard:,}   Total Passing Yards: {temp_list[1]}\n"
                              f"Per Pass Attempt: ${pay_per_attempt:,}   Total Pass Attempts: {temp_list[3]}\n"
                              f"Per Pass Completed: ${pay_per_completion:,}   Total Pass Completions: {temp_list[4]}\n"
                              f"Per TD: ${pay_per_TD:,}   Totals Passing TDs: {temp_list[6]}\n")

