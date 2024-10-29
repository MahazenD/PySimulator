'''
***********************************************************************

NOTES FOR STUDEENTS
-------------------
Change this file appropriately
    1. update the endpoint URL
    2. update the API Key or update your environment variable
    3. (If required) change the logic

***********************************************************************
'''

import time
import json
import requests
import os

class EdgeAnalyzer:
    def __init__(self):
        self.endPoint = 'http://172.21.188.162:80/image'
        self.apiKey = '8b47093c924d4e93b2e28adbb9e5eca0'
        
    def analyzeImage(self, filePath) -> int:
        start_time = time.time()
        url = self.endPoint
        headers = {
            'Prediction-Key': self.apiKey,
            'Content-Type': 'application/octet-stream'
        }
        with open(filePath, 'rb') as file:
            response = requests.post(url, headers=headers, data=file)

        rowNo = filePath[-6:-4]
        if response.status_code == 200:
            data = json.loads(response.text)

            #find any Bad cookie with prediction rate more than 0.8
            filtered_predictions = [
                prediction for prediction in data["predictions"]
                if prediction["probability"] > 0.8 and prediction["tagName"] == "Bad"
            ]
            badCount = len(filtered_predictions)
            print(f"ROW: {rowNo}   |   BAD: {badCount}  |  TIME: {(time.time() - start_time):.2f}s")
            time.sleep(1.5)
            return badCount
        else:
            print(f"* ROW: {rowNo}   |  FAILED: {response.status_code}  |  TIME: {(time.time() - start_time):.2f}s")
            return 0