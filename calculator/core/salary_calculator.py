import logging

import numpy as np
import pandas as pd
import validators

logger = logging.getLogger(__name__)


class SalaryDataFrame:
    def __init__(self, salary_data_url):
        if not salary_data_url:
            raise ValueError("Parameter salary_data_url must be defined")

        if not validators.url(salary_data_url):
            raise ValueError(f"Parameter salary_data_url=[{salary_data_url}] is not a valid URL")

        logger.debug(f"Reading HTML-based salary data from url=[{salary_data_url}]")
        df: pd.DataFrame = pd.read_html(salary_data_url)[0]

        # Taken from : https://stackoverflow.com/a/39371897
        required_columns = {"Salary", "Player", "Year", "Level"}
        if not required_columns.issubset(df.columns):
            raise Exception(
                f"DataFrame created from HTML via URL [{salary_data_url}] does not contain all required columns [{required_columns}]"
            )

        self.prefiltered_row_count = len(df)

        # Taken from : https://stackoverflow.com/a/29314880
        #   1. Convert all empty string salaries to NaN
        #   2. Drop all rows where Salary is NaN
        logger.debug(f"Replacing empty strings and NaNs within 'Salary' column. Number of rows = [{len(df)}]")
        df["Salary"].replace("", np.nan, inplace=True)
        df["Salary"].dropna(inplace=True)

        logger.debug(f"Filtering illegal strings from 'Salary' column. Number of rows = [{len(df)}]")
        df = df[df["Salary"].str.contains("no salary data") == False]

        logger.debug(f"Normalizing 'Salary' column to convert currency into a number. Number of rows = [{len(df)}]")
        df["Salary"] = df["Salary"].apply(self._clean_currency).astype("int")

        self.postfiltered_row_count = len(df)
        self.df: pd.DataFrame = df

    def calculate_top_n_salaries(self, number_of_salaries):
        logger.debug(f"Calculating the qualifying offer for the top [${number_of_salaries}] salaries")

        logger.debug(f"Taking the top [{number_of_salaries}] salaries. Number of rows = [{len(self.df)}]")
        df = self.df.sort_values("Salary", ascending=False).head(number_of_salaries)

        logger.debug(f"Calculating the mean of the top [{number_of_salaries}] salaries. Number of rows = [{len(df)}]")
        qualifying_offer = int(df["Salary"].mean())

        top_player_salaries = df.to_dict(orient="records")

        # Return a tuple of dict, dict so that different services could include the entire DF if they choose
        return (
            {
                "number_of_salaries": number_of_salaries,
                "qualifying_offer": qualifying_offer,
                "meta": {
                    "prefiltered_row_count": self.prefiltered_row_count,
                    "postfiltered_row_count": self.postfiltered_row_count,
                },
            },
            top_player_salaries,
        )

    def get_all_salaries(self):
        return self.df.to_dict(orient="records")

    # Taken from : https://pbpython.com/currency-cleanup.html
    @staticmethod
    def _clean_currency(value):
        # We might encounter non-strings, so let's try to be safe
        if isinstance(value, str):
            return value.replace("$", "").replace(",", "")
        return value
