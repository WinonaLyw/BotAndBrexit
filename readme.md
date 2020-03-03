# Bot and #Brexit
### Analysis of bot influnce with tweets having #Brexit hashtags
***(original data set is not included in the repository)***

## Data Source
1. 1,267,607 tweets tagged with #brexit from 1st Jan to 31st Mar, 2018
1. 73,194 tweeter accounts with botness score calculated by [Botometer](https://botometer.iuni.iu.edu)

## Dataset Information Retrieve

1. Select 26,327 tweets on 29th March, 2018, envolving 11,887 accounts, see [select_tweets.py](select_tweets.py) for details.
<br/>Why 29th March, 2018?:
    2. Highest daily tweets on the selected date;
    2. Top 10 increase of number of daily tweets comparing to the previous one;
    2. Top 10 decrease of number of daily tweets for the next day;
    2. No special Brexit events found in news on that particular day.
1. For the 11,887 accounts envolved:
	2. 7,797(10.65% overall) of them have botness score no less than 0.5 quantile(0.25)
	2. 4,567(6.24% overall) no less than 0.75 quantile(0.33)
	2. 2,881(3.9% overall) no less than 0.85 quantile(0.37)



## Workflow
### PREPROCESSING
1. [Add more columns into tweets table](extend_tweets.py)
1. [Select tweets sample](select_tweets.py)
1. [Select accounts sample accordingly](select_accounts.py)
1. [Add more columns into sample accounts table](extend_accounts.py)

### ACCOUNT SELECTION (BOT VS HUMAN)
final sample accounts, 2,886 bots

### NETWORK DATA ANALYSIS


### FURTHER WORK
repeat the workflow with different sample selected...