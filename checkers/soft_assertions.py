from hamcrest import assert_that
from hamcrest.core.string_description import StringDescription


class SoftAssertions:
    def __init__(self):
        self._exceptions = []

    def assert_that(self, actual, matcher=None, message=""):
        try:
            assert_that(actual_or_assertion=actual, matcher=matcher, reason=message)
        except AssertionError as error:
            self._exceptions.append(error)

    def _get_errors_text(self) -> StringDescription:
        description = StringDescription()
        description.append('One or more Assertions failed!\n')
        description.append(f'Total failures collected: {len(self._exceptions)}.\n')
        for error in self._exceptions:
            description.append(error)
            description.append('\n')
        return description

    def assert_all(self):
        if self._exceptions:
            description = self._get_errors_text()
            self._exceptions = []
            raise AssertionError(description)