# built-in imports
# standard library imports
import pickle

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Jobs


def get_data_list() -> list[Jobs]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
   url: str = "https://onu1.s2.chalmers.se/datasets/AI_ML_jobs.json"
    response = requests.get(url, timeout=30)


def calculate_statistics(dataset: list[Jobs]) -> dict[int | str, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    # TODO
    pass


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
