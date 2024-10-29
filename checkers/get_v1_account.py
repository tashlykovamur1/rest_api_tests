from hamcrest import equal_to, has_items

from checkers.soft_assertions import SoftAssertions


class GetV1Account:
    @classmethod
    def check_received_user_info(cls, response, login: str):
        soft = SoftAssertions()
        soft.assert_that(response.body['resource']['login'], equal_to(login))
        soft.assert_that(response.body['resource']['rating']['enabled'], equal_to(True))
        soft.assert_that(response.body['resource']['roles'], has_items("Guest", "Player"))
        soft.assert_all()
