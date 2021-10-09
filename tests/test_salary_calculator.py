import pytest

from calculator import config
from calculator.core.salary_calculator import SalaryDataFrame


def test_initialization_fails_with_no_url():
    with pytest.raises(ValueError):
        SalaryDataFrame(None)


def test_initialization_fails_with_malformed_url():
    with pytest.raises(ValueError):
        SalaryDataFrame("i-am-not-a-url")


def test_initialization_fails_with_unexpected_source_data():
    with pytest.raises(Exception):
        SalaryDataFrame("https://google.com")


# The following would be considered integration tests rather than unit tests, but the results are certainly valuable.
# We alternatively could pickle the results of a successful load and initialize the SalaryDataFrame with that instead.
# However, I think this is more practical (as opposed to pure), since we actually do have a hard dependency on the
# external data.
def test_initialization_successful_with_expected_source_data():
    SalaryDataFrame(config.SALARY_DATA_URL)


def test_calculating_top_n_salaries():
    number_of_salaries = 10
    results, highest_paid_players = SalaryDataFrame(config.SALARY_DATA_URL).calculate_top_n_salaries(number_of_salaries)

    assert results["number_of_salaries"] == number_of_salaries
    assert results["qualifying_offer"] > 0
    assert results["meta"]["prefiltered_row_count"] >= results["meta"]["postfiltered_row_count"]
    assert len(highest_paid_players) == number_of_salaries


def test_getting_all_salaries():
    assert len(SalaryDataFrame(config.SALARY_DATA_URL).get_all_salaries()) > 0
