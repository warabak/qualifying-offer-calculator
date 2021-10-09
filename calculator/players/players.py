import logging

from flask import request, render_template

from calculator.players import api_bp
from calculator.utils import get_salary_dataframe

logger = logging.getLogger(__name__)


@api_bp.route("/calculator", methods=["GET", "POST"])
def calculator():
    default_number_of_highest_salaries = 125

    if request.method == "POST":
        number_of_salaries = int(request.form.get("numberOfSalaries", default_number_of_highest_salaries))
    else:
        number_of_salaries = int(request.args.get("number_of_salaries", default_number_of_highest_salaries))

    if number_of_salaries < 1:
        number_of_salaries = default_number_of_highest_salaries

    salary_dataframe = get_salary_dataframe()

    summary, _ = salary_dataframe.calculate_top_n_salaries(number_of_salaries)
    all_salaries = salary_dataframe.get_all_salaries()

    return render_template("calculator.html", summary=summary, all_salaries=all_salaries)
