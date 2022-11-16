#Python Script to get data from twitter api for recent tweets

#Importing requests library to make http api calls to twitter (to do the curl command)
import requests 

#Importing json library so that the response back from twitter will be json format      
import json    

#Importing various methods from azure-storage-blob library       
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient, __version__ 

from datetime import datetime

#To get the current date and time
datetime = datetime.now().strftime("%Y_%m_%d_%I:%M:%S")

#To set our environment variables in our terminal we need to run the following line:
#export bearer token
bearer_token = '<bearer_token>'

#Connection string
conn_string = "<Azure connection string of storage account>"

#Using the requests library we hit the twitter api, on its latest version 2, for the recent tweets
search_url = "https://api.twitter.com/2/tweets/search/recent"

#Optional parameters to get the details from the tweets such as mentioned below:
#start_time, end_time, since_id, until_id, max_results, next_token, expansions, tweet.fields, media.fields, poll.fields, user.fields
query_params = {'query': '(from:twitterdev -is:retweet) OR #twitterdev', 'tweet.fields': 'author_id, public_metrics'}

#Bearer method to get bearer token authorization
def bearer_oauth(r):
    """Method required for bearer token authorization. While making an API call bearer token is required as an header information."""
  
    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2RecentSearchPython"
    return r

#Method to connect the endpoint from twitter api and getting the response status and json format of the data
def connect_to_endpoint(url, params):

    #Calling to twitter api using the bearer token
    response = requests.get(url, auth = bearer_oauth, params = params)
    print(response.status_code)
    
    if response.status_code != 200:
        raise Exception(response.status_code, response.text)
    
    return response.json()

def main():
    
    #Getting the json data from the connect to endpoint method
    json_response = connect_to_endpoint(search_url, query_params)

    #Connecting the Azure container using the connection string
    container_client = ContainerClient.from_connection_string(conn_string, container_name = "<Azure container name>")

    #Uploading the json data with datetime stamp to the container, inside the files folder
    container_client.upload_blob(f"files/twitter_{datetime}.json", data = json.dumps(json_response))

    #Printing the json dump on the console
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()