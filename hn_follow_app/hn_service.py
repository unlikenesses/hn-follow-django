import requests, json
from datetime import datetime
from .models import HnUser, HnSubmission

class HnService:

    def __init__(self):
        self.base_url = 'https://hacker-news.firebaseio.com/v0'

    def getAllSubmitted(self, usernames):
        submitted = []
        for username in usernames:
            user = self.getHnUserDetailsFromDb(username)
            submitted += json.loads(user.submissions)

        return sorted(submitted, reverse=True)
    
    def getHnUserDetailsFromDb(self, username):
        user = HnUser.objects.get(username=username)
        return user 

    def getHnUserDetailsFromAPI(self, username):
        response = requests.get(self.base_url+'/user/'+username+'.json')
        return response.json()
    
    def getSubmissions(self, submissionIds):
        submissions = []
        for submissionId in submissionIds:
            try:
                submission = self.getSubmissionFromDb(submissionId)
            except HnSubmission.DoesNotExist:
                submissionFromApi = self.getSubmissionFromAPI(submissionId)
                # Save it in the db:
                submission = HnSubmission(
                    id=submissionId,
                    text=submissionFromApi.get('text'),
                    time=datetime.utcfromtimestamp(submissionFromApi['time']).strftime('%Y-%m-%d %H:%M:%S'),
                    type=submissionFromApi['type'],
                    by=submissionFromApi['by'],
                )
                submission.save()
            submissions.append(submission)

        return submissions
    
    def getSubmissionFromDb(self, submissionId):
        submission = HnSubmission.objects.get(id=submissionId)
        return submission
    
    def getSubmissionFromAPI(self, submissionId):
        response = requests.get(self.base_url+'/item/'+str(submissionId)+'.json')
        return response.json()
