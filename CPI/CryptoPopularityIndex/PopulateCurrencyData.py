import CoinmarketcapApiRetriever
import boto3
import json, os, datetime, logging


# Retrieve the data (This starts the process of calling Coinmarketcap and Google APIs)
currencyList = CoinmarketcapApiRetriever.retrieveCurrencies()

# Defining a dictionary to help process the currency list into JSON
for currency in currencyList:
    def obj_dict(obj):
        return obj.__dict__

# Creating JSON based on the list of currencies
for currency in currencyList:
    def obj_dict(obj):
        return obj.__dict__
json_string = json.dumps(currencyList, default=obj_dict)
json_list = json.loads(json_string)

# Write the json output to a file. This is for debugging/logging
with open('data.json', 'w') as outfile:
    json.dump(json_list, outfile, indent=4)

# Open connection to AWS S3 bucket
# I almost checked my AWS keys into Github. Good thing I'm smarter than the average bear.
s3 = boto3.resource('s3',
                    aws_access_key_id=os.environ['S3_KEY'],
                    aws_secret_access_key=os.environ['S3_SECRET'])
s3_client = boto3.client('s3',
                         aws_access_key_id= os.environ['S3_KEY'],
                         aws_secret_access_key= os.environ['S3_SECRET'])

# Upload the file to S3. Making it public so anyone can use it.
s3_client.upload_file('data.json', 'cryptopopindex', 'latestData.json', ExtraArgs={'ContentType': "application/json", 'ACL':'public-read'})
logging.info("Uploaded .json info to AWS S3 bucket.")

# Ugly print statement because my logging statements aren't showing up in Heroku logs  :(
print("Finished retrieving trends at: ", datetime.datetime.now())
