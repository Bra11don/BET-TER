import math

#opening the files with goals data
def goals1(file_name):
    goals = []
    with open(file_name) as file:
        for line in file:
            goals.append(float(line))
        return goals

#opening the respective files from the function above
home_gf = goals1("home_gf.txt")  #home_gf - goals scored by a team at home stadium
home_ga = goals1("home_ga.txt")  #home_ga - goals conceded by (scored against) a team at home stadium
away_gf = goals1("away_gf.txt")  #away_gf - goals scored by a team at away stadium
away_ga = goals1("away_ga.txt")  #away_ga - goals conceded by (scored against) a team at away stadium

# ask the user to enter team indices
def name_get():
    name1 = int(input("Enter home team index: "))
    name2 = int(input("Enter away team index: "))
    return name1,name2
homename,awayname = name_get()  #homename is the name of the home team, awayname is the name of the away team

#opening the file with team names and placing the names in a list
teams = []
with open("teams.txt") as file:
    for line in file:
        teams.append(line)

print("the home team selected is",teams[homename])  #printing the respective home team from the selected indice
print("the away team selected is",teams[awayname])  #printing the respective away team from the selected indice


#average of goals (total goals/number of teams)
def tot_average(goals1):
    avg = sum(goals1)/len(goals1)
    return avg

tot_home_avg_gf = sum(home_gf) / len(home_gf)  #the average number of goals scored by the home team
tot_home_avg_ga = sum(home_ga) / len(home_ga)  #the average number of goals conceded by the home team
tot_away_avg_gf = sum(away_gf) / len(away_gf)  #the average number of goals scored by the away team
tot_away_avg_ga = sum(away_ga) / len(away_ga)  #the average number of goals conceded by the away team


#average goals for a team per matches played
matches_played = 7 #for this project we'll use 7 games because at the time of writing the code each team had played 7games at home and away
def avg_goals(goals1,name):
    aver1 = goals1[name]/matches_played
    return aver1

home_aver_gf = avg_goals(home_gf,homename)  #the average_gf for the home team
home_aver_ga = avg_goals(home_ga,homename)  #the average_ga for the home team
away_aver_gf = avg_goals(away_gf,awayname)  #the average_gf for the Away team
away_aver_ga = avg_goals(away_ga,awayname)  #the average_ga for the away team


#league average which is the average of all individual team averages (sum of individual team averages/total number of teams)
def total_av(goals1):
    ave = []
    for goal in goals1:
        ave.append(goal / matches_played)
    total_avg = sum(ave)/len(ave)
    return total_avg

total_avg_home_gf = total_av(home_gf) #league average of home goals for
total_avg_home_ga = total_av(home_ga) #league average  of home goals for
total_avg_away_gf = total_av(away_gf) #league average  of away goals against
total_avg_away_ga = total_av(away_ga) #league average  of Away goals against


#team individual strengths (individual averages/ sum of all averages)
def teaminds(goals1,name):
        home_strength = avg_goals(goals1,name) / total_av(goals1)
        return home_strength

home_att_strength = teaminds(home_gf,homename)  #home team attacking strength (team_gf/ league average_gf)
home_def_strength = teaminds(home_ga,homename)  #home team defending strength (team_gf/ league total_gf)
away_att_strength = teaminds(away_gf,awayname)  #away team attacking strength (team_ga/ league total_ga)
away_def_strength = teaminds(away_ga,awayname)  #away team defending strength (team_ga/ league total_ga)


#probability of number of goals.. this is where Poisson distribution formula comes in
def goal_prob(n,xG):  #n is the number of goals, xG is the expected goals
    while n < 5:
        step_1 = xG ** n
        step_2 = math.exp(-xG)
        step_3 = step_2 * step_1
        step_4 = math.factorial(n)
        step_5 = step_3/step_4
        return step_5

outcomes = []
for n1 in range(0,5):
    for n2 in range(0,5):
        # home expected goals = hometeam attacking strength at home stadium * hometeam defending strength at away stadium * home team average goals for at home
        home_xG = teaminds(home_gf, homename) * teaminds(away_ga, homename) * avg_goals(home_gf, homename)
        # away expected goals = awayteam attacking strength at away stadium * awayteam defending strength at home stadium * away team average goals for at away stadium
        away_xG = teaminds(away_gf, awayname) * teaminds(home_ga, awayname) * avg_goals(away_gf, awayname)
        #home team goal probability
        home_goals_prob = goal_prob(n1,home_xG)  #probability of home team to score n goals

        #away team goal probability
        away_goals_prob = goal_prob(n2,away_xG) #probability of away team to score n goals

        #PREDICTING MATCH OUTCOMES
        #function to make sure all outcomes are accounted for and only the highest outcome is printed
        prob_goals = home_goals_prob * away_goals_prob
        print("The probability of the game ending "+ str(n1) + "-" + str(n2)+" is " + str(round(prob_goals,3)) )
        outcomes.append(round(prob_goals, 3))
#print(outcomes)

probability = float(input("Enter the probability of the outcome you would like to bet on: "))
while probability not in outcomes:
    print('Please make sure you have entered the correct probability.')
    probability = float(input("Enter the probability of the outcome you would like to bet on: "))
    continue

#match odds
odds = 1/probability #the odds for a selected outcome
print("The odds from chosen outcome are", odds)

#total payout to be won
#AMOUNT TO STAKE (bet on)
amount = int(input("How much would you like to stake? (in USD): "))
total_payout = amount * odds #total amount that a player wins after placing a certain bet
print("The total amount you'll win is",round(total_payout), "usd")


