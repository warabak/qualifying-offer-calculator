import logging

from calculator import config
from calculator.core.salary_calculator import SalaryDataFrame

logger = logging.getLogger(__name__)

# We have several options when dealing with calculating the original DataFrame :
# ---------------------------------------------------------------------------------------------------------------------
#   1. Query the URL and parse, clean, and prepare the data for each Flask request.
#   2. Compute the initial DataFrame on start-up, and store it in a proper local cache
#      where we can expire and refresh it arbitrarily.
#   3. Compute the initial DataFrame and serialize it to some external system.
#      This would be absolutely necessary if we had more than a single server.
#      Another system altogether would be responsible for generating the underlying data in the real world anyway and
#      our app here would just be querying what it needs, probably from a database.
#   4. Implement a memoizer at the function level, where the DataFrame can be lazily loaded.
#   5. Compute the initial DataFrame and permanently store and encapsulate it here.
#      We would not use this approach in anything but a demonstration, given that the
#      underlying data is subject to change.
# ---------------------------------------------------------------------------------------------------------------------
# For the purposes of this exercise, we'll use option #5
cache = {}


def get_salary_dataframe() -> SalaryDataFrame:
    if "df" not in cache:
        logger.debug(
            "Generating the initial DataFrame. This will only happen once throughout the entire life of the server"
        )
        cache["df"] = SalaryDataFrame(config.SALARY_DATA_URL)

    return cache["df"]


def format_currency(value):
    return "${:,}".format(value)
