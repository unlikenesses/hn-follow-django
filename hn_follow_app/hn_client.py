import requests


class HnClient:
    def __init__(self):
        self.base_url = "https://hacker-news.firebaseio.com/v0"

    def getHnUserDetailsFromAPI(self, username):
        response = requests.get(self.base_url + "/user/" + username + ".json")
        return response.json()

    def getSubmissionFromAPI(self, submissionId):
        response = requests.get(self.base_url + "/item/" + str(submissionId) + ".json")
        return response.json()
