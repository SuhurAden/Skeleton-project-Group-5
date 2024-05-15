# built-in imports
# standard library imports
import ast
import collections
import pickle

import requests

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import Jobs


def get_data_list() -> list[Jobs]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving each object to a Redis list.
    """

    ##### check if dataset already exists, and if so, return the existing dataset  #####
    # db.delete("dataset_list")  # uncomment if you want to force deletion

    if db.exists("dataset_list") > 0:  # checks if the `dataset` key already exists
        current_app.logger.info("Dataset already downloaded.")
        dataset_stored: list[Jobs] = []  # empty list to be returned
        raw_dataset: list[bytes] = db.lrange("dataset_list", 0, -1)  # get list from DB
        for item in raw_dataset:
            dataset_stored.append(pickle.loads(item))  # load item from DB
        return dataset_stored

    ################# dataset has not been downloaded, downloading now #################
    current_app.logger.info("Downloading dataset.")
    url = "https://onu1.s2.chalmers.se/datasets/AI_ML_jobs.json"
    response = requests.get(url, timeout=30)

    ########################## saving dataset to the database ##########################
    dataset_base: list[Jobs] = []  # list to store the items
    # for each item in the dataset..
    for item in response.json():

        new_job = Jobs(
            title=item["Title"],
            company=item["Company"],
            location=item["Location"],
            position_type=item["Type of Positions"],
            job_description=item["Job Description"],
            salary=item["Salary"],
            identified_skills=item["Identified_Skills"],
        )

        db.rpush("dataset_list", pickle.dumps(new_job))
        dataset_base.append(new_job)  # append to the list

    return dataset_base


def calculate_statistics(dataset: list[Jobs]) -> dict[int | str, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """

    counter: dict[int | str, int] = collections.defaultdict(int)

    for item in dataset:
        for skill in ast.literal_eval(item.identified_skills):
            counter[skill] += 1

    # for item in dataset:
    # for skill in item.identified_skills:
    # counter[skill] += 1

    return counter


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
