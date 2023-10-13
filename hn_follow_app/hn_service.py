import json
from datetime import datetime
from .models import HnUser, HnSubmission
from .hn_client import HnClient


class HnService:
    def __init__(self):
        self._client = HnClient()

    def getAllSubmitted(self, usernames):
        submitted = []
        for username in usernames:
            user = self.getHnUserDetailsFromDb(username)
            submitted += json.loads(user.submissions)

        return sorted(submitted, reverse=True)

    def getHnUserDetailsFromDb(self, username):
        user = HnUser.objects.get(username=username)
        return user

    def getSubmissions(self, submissionIds):
        submissions = []
        for submissionId in submissionIds:
            try:
                submission = self.getSubmissionFromDb(submissionId)
            except HnSubmission.DoesNotExist:
                submissionFromApi = self._client.getSubmissionFromAPI(submissionId)
                # Save it in the db:
                submission = HnSubmission(
                    id=submissionId,
                    text=submissionFromApi.get("text"),
                    time=datetime.utcfromtimestamp(submissionFromApi["time"]).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    type=submissionFromApi["type"],
                    by=submissionFromApi["by"],
                )
                submission.save()
            submissions.append(submission)

        return submissions

    def getSubmissionFromDb(self, submissionId):
        submission = HnSubmission.objects.get(id=submissionId)
        return submission

    def addHnUserToUser(self, form_data, user):
        # check to see if the HN user is already in the database, if so add this user to it
        try:
            hn_user = HnUser.objects.get(username=form_data["username"])
            hn_user.user.add(user)
            hn_user.save()
        except HnUser.DoesNotExist:
            # try to get the HN user from the HN API
            user_from_api = self._client.getHnUserDetailsFromAPI(form_data["username"])
            if user_from_api is None:
                raise Exception("User not found")
            # add the user
            submissions = json.dumps(user_from_api["submitted"])
            hn_user = HnUser(
                username=form_data["username"],
                about=user_from_api.get("about"),
                karma=user_from_api["karma"],
                submissions=submissions,
                notes=form_data["notes"],
            )
            hn_user.save()
            hn_user.user.add(user)
