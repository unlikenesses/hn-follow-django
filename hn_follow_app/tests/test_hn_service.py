import pytest, json
from hn_follow_app.models import HnUser, HnSubmission
from hn_follow_app.hn_service import HnService


@pytest.mark.django_db
def test_it_gets_all_submitted_in_order():
    # Set up users
    username1 = "user 1"
    submissions1 = [7, 13]
    HnUser(
        username=username1,
        submissions=json.dumps(submissions1),
    ).save()
    username2 = "user 2"
    submissions2 = [1, 18, 19]
    HnUser(
        username=username2,
        submissions=json.dumps(submissions2),
    ).save()
    username3 = "user 3"
    submissions3 = [4, 103]
    HnUser(
        username=username3,
        submissions=json.dumps(submissions3),
    ).save()
    merged = submissions1 + submissions2 + submissions3
    # Call method
    hn_service = HnService()
    submitted = hn_service.getAllSubmitted([username1, username2, username3])
    assert len(submitted) == len(merged)
    assert submitted == sorted(merged, reverse=True)


@pytest.mark.django_db
def test_it_gets_an_hn_user_from_the_db():
    # Set up user
    username = "test_username"
    hn_user = HnUser(
        username=username,
    )
    hn_user.save()
    # Call method
    hn_service = HnService()
    user_from_db = hn_service.getHnUserDetailsFromDb(username)
    assert user_from_db == hn_user
