import requests
import json
from .models import CarDealer, DealerReview
from requests.auth import HTTPBasicAuth

# Watson NLU API configuration values
watson_nlu_api_base_url = "https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com/instances/bc906088-fbeb-40cd-abd5-3738474659aa/v1/analyze"
watson_nlu_api_key = "4aBlw6qGio3BCXSIjb6ReuOYTAsAQQBbd-pWUtfsVS7W"
watson_nlu_api_version = '2021-08-01'

def get_request(url, **kwargs):
    print(kwargs)
    print("GET from {} ".format(url))

    try:
        response = requests.get(url, params=kwargs, headers={'Content-Type': 'application/json'},
                                    auth=HTTPBasicAuth('apikey', watson_nlu_api_key))    
    except:
        # If any error occurs
        print("Network exception occurred")
    else:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data

# Create a `post_request` to make HTTP POST requests
# e.g., response = requests.post(url, params=kwargs, json=payload)
def post_request(url, json_payload, **kwargs):
    try:
        response = requests.post(url, json=json_payload, headers={'Content-Type': 'application/json'},
                                 params=kwargs)
    except:
        print("Network exception occurred on POST request")
    else:
        status_code = response.status_code
        print("With status {} ".format(status_code))
        json_data = json.loads(response.text)
        return json_data


# Create a get_dealers_from_cf method to get dealers from a cloud function
# def get_dealers_from_cf(url, **kwargs):
# - Call get_request() with specified arguments
# - Parse JSON results into a CarDealer object list

def get_dealers_from_cf(url, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url, params=kwargs)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer["doc"]
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])

            results.append(dealer_obj)

    return results

def get_dealer_by_id(url, dealerId, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        # Get its content in `doc` object
        dealer_doc = dealers[0]
        # Create a CarDealer object with values in `doc` object
        dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                               id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                               short_name=dealer_doc["short_name"],
                               st=dealer_doc["st"], zip=dealer_doc["zip"])

    return dealer_obj

def get_dealers_by_state(url, state, **kwargs):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,state=state)
    if json_result:
        # Get the row list in JSON as dealers
        dealers = json_result["result"]
        # For each dealer object
        for dealer in dealers:
            # Get its content in `doc` object
            dealer_doc = dealer
            # Create a CarDealer object with values in `doc` object
            dealer_obj = CarDealer(address=dealer_doc["address"], city=dealer_doc["city"], full_name=dealer_doc["full_name"],
                                   id=dealer_doc["id"], lat=dealer_doc["lat"], long=dealer_doc["long"],
                                   short_name=dealer_doc["short_name"],
                                   st=dealer_doc["st"], zip=dealer_doc["zip"])
            results.append(dealer_obj)

    return results


def get_dealer_reviews_from_cf(url,dealerId):
    results = []
    # Call get_request with a URL parameter
    json_result = get_request(url,dealerId=dealerId)
    if json_result:
        # Get the row list in JSON as dealers
        reviews = json_result["result"]
        # For each dealer object
        for review in reviews:
            sentiment = ""
            review_obj = DealerReview(dealership=review["dealership"],name=review["name"],
                                      purchase=review["purchase"],review=review["review"],
                                      purchase_date=review["purchase_date"],car_make=review["car_make"],
                                      car_model=review["car_model"],car_year=review["car_year"],
                                      sentiment=sentiment)
            review_obj.sentiment = analyze_review_sentiments(review_obj.review)
            results.append(review_obj)
    return results

def analyze_review_sentiments(text):
    features = {"sentiment" : {}}    
    params = dict()
    params["text"] = text
    params["version"] = watson_nlu_api_version
    params["features"] = features
    params["return_analyzed_text"] = True

    response = get_request(watson_nlu_api_base_url, params=params, headers={'Content-Type': 'application/json'}, auth=HTTPBasicAuth('apikey', watson_nlu_api_key))
    if "error" in response:
        return "neutral"
    else:
        text_sentiment = response["sentiment"]["document"]["label"]
        return text_sentiment
