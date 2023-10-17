import pytest
from hn_follow_app.models import HnUser, HnSubmission
from hn_follow_app.hn_service import HnService

@pytest.mark.django_db
def test_it_gets_an_hn_user_from_the_db():
    # Set up user
    username = 'test_username'
    hn_user = HnUser(
        username=username,
        about="",
        karma=123,
        submissions=[],
        notes="",
    )
    hn_user.save()
    # Call method
    hn_service = HnService()
    user_from_db = hn_service.getHnUserDetailsFromDb(username)
    assert user_from_db == hn_user

