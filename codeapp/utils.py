# built-in imports
# standard library imports
from datetime import date, datetime
import collections
import json
import math
import pickle
from dataclasses import dataclass

# external imports
from flask import current_app
from nbformat import from_dict
import requests
from typing import List

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
    # for each item in the dataset...
    for item in response.json():
        # check if the date can be parsed
        date_added: date | None = None
        try:
            date_added = datetime.strptime(item["date_added"], "%B %d, %Y").date()
        except Exception:
            pass

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
    counter: dict[str, int] = collections.defaultdict(lambda: 0)
    for item in dataset:
        counter[item.position_type] += 1

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
