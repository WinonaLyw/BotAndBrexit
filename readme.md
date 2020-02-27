# Bot and Brexit
### Analysis of bot influnce with tweets having #Brexit hashtags
(Data is not included in the repository due to confidential issue.)

## Data Source
1. 1,267,607 tweets tagged with #brexit from 1st Jan to 31st Mar, 2018
1. 73,194 tweeter accounts with botness score calculated by [Botometer](https://botometer.iuni.iu.edu)

## Sample selection

1. Select 26,327 tweets on 29th March, 2018, envolving 11,887 accounts, see [select_tweets.py](select_tweets.py) for details.
<br/>Why 29th March, 2018?:
    2. Highest daily tweets on the selected date;
    2. Top 10 increase of number of daily tweets comparing to the previous one;
    2. Top 10 decrease of number of daily tweets for the next day;
    2. No special Brexit events found in news on that particular day.
1. For the 11,887 accounts envolved:
	2. 7,797(10.65%) of them have botness score no less than 0.5 quantile(0.25)
	2. 4,567(6.24%) no less than 0.75 quantile(0.33)
	2. 1,906(2.61%) on less than 0.9 quantile(0.40)
