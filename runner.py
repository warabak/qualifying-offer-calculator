import json
import logging

import click
from dotenv import load_dotenv

from calculator import config
from calculator.core.salary_calculator import SalaryDataFrame


@click.command()
@click.option(
    "--number_of_salaries",
    default=125,
    help="The number of highest salaries to use when calculating the qualifying offer",
)
@click.option(
    "--show_top_salaries",
    default=False,
    is_flag=True,
    help="Optionally show the top players salaries",
)
@click.option(
    "--verbose", default=False, is_flag=True, help="Run the program in verbose mode"
)
def execute(number_of_salaries, show_top_salaries, verbose):
    load_dotenv()

    log_level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(level=log_level)

    results, top_player_salaries = SalaryDataFrame(
        config.SALARY_DATA_URL
    ).calculate_top_n_salaries(number_of_salaries)

    if show_top_salaries:
        click.echo(
            json.dumps(
                {**results, "top_player_salaries": top_player_salaries}, indent=4
            )
        )
    else:
        click.echo(json.dumps(results, indent=4))


if __name__ == "__main__":
    execute()
