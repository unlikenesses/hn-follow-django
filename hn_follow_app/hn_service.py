import requests

class HnService:

    def __init__(self):
        self.base_url = 'https://hacker-news.firebaseio.com/v0'

    def getAllSubmitted(self, usernames):
        submitted = []
        for username in usernames:
            details = self.getHnUserDetails(username)
            submitted += details['submitted']

        # submitted = [self.getHnUserDetails(username)['submitted'] for username in usernames]

        return sorted(submitted, reverse=True)

    def getHnUserDetails(self, username):
        response = requests.get(self.base_url+'/user/'+username+'.json')
        return response.json()
    
    def getSubmissions(self, submissionIds):
        submissions = []
        for submissionId in submissionIds:
            submissions.append(self.getSubmission(submissionId))

        return submissions
    
    def getSubmission(self, submissionId):
        response = requests.get(self.base_url+'/item/'+str(submissionId)+'.json')
        return response.json()
