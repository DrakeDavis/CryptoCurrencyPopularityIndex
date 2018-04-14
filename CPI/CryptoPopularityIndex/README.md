The Cryptocurrency Popularity Index

<b>What is this?</b>

This program uses Google Trends to see which cryptocurriences are becoming more popular. 

<b>How does it work?</b>

First, the program retrieves the top 100 cryptocurrenceis as defined by marketcap from an API proivided by Coinmarketcap: 
https://api.coinmarketcap.com/v1/ticker/

Secondly, each retrived cryptocurrency is then populated with data from Google Trends (https://trends.google.com/trends/)
This is accomplished from the excellent python library 'pytrends.'

Lastly, the aggregated data is stored in .json format and uploaded to an Amazon webservices S3 bucket - where it can be accessed by anyone:
https://s3.us-east-2.amazonaws.com/cryptopopindex/latestData.json

This Python job is schuedled to run once an hour through my Heroku server. 

<b>Where can I see it in action?</b>

I have created a web interface for this data that can be viewed at http://drake.technology/CCPI
