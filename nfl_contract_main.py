from nfl_contract_player_info import NFL_Player_Stats, NFL_Player_Pay, Pay_Per_Play
import datetime

current_year = datetime.datetime.now().year

def main():
    """main function"""
    # Statictical Data Available from 1970 to Present
    # Contract Data Avilable from 2020 to Present, If 2019 or below is entered only statistics will be shown
    print("Enter year to get pay per play information for quarterbacks in NFL")
    print("Years 2020 and above will show pay per play information, 2019 and below is statistics only")
    def user_input_year():
        year_ = input('Enter Year: ')
        if int(year_) < 1970 or int(year_) > (current_year - 1):
             print("Year entered is not between 1970 and Current Year, please try again")
             return user_input_year()
        else:
            return year_

    year = str(user_input_year())
    print(year)

    print('\n')

    # Nfl player pay class instance created and method player_contracts called
    contract = NFL_Player_Pay()
    contract.player_contracts(year=year)

    # player stats class instance created and player_statistics method called
    stats = NFL_Player_Stats()
    stats.players_statistics(year=year)

    # pay_per_pay class instance created
    pay_per_play = Pay_Per_Play()

    # if statement to decide, based on the year entered by user, as to which data should be displayed (stats only or stats with pay eval)
    if int(year) < 2020:
        stats.print_dataframe()
    else:
        pay_per_play.gather()


# Main Function Call
main()

