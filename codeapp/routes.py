# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
from codeapp.models import Jobs
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int | str, int] = calculate_statistics(dataset)

    sorted_jobs = sorted(counter.items(), key=lambda y: y[1], reverse=True)

    # render the page
    return render_template("home.html", counter=sorted_jobs)


@bp.get("/image")
def image() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int | str, int] = calculate_statistics(dataset)

    sorted_jobs = sorted(counter.items(), key=lambda y: y[1], reverse=True)

    # creating the plot
    fig = Figure()

    vert = [x[0] for x in sorted_jobs][:15]
    horz = [x[1] for x in sorted_jobs][:15]

    vert.reverse()
    horz.reverse()

    fig.gca().barh(
        vert,
        horz,
        color="gray",
        alpha=0.5,
        zorder=2,
    )

    fig.gca().grid(ls=":", zorder=1)
    fig.gca().set_xlabel("Number of jobs")
    fig.gca().set_ylabel("Skills")
    fig.tight_layout()

    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/data")  # data route
def data() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # Shorten job descriptions to 100 characters.
    for job in dataset:
        job.job_description = job.job_description[:100] + "..."

    return render_template("data.html", data=dataset[:15])


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # render the page
    return jsonify(dataset)


@bp.get("/json-stats")
def get_json_stats() -> Response:
    # gets dataset
    dataset: list[Jobs] = get_data_list()

    # get the statistics that is supposed to be shown
    counter: dict[int | str, int] = calculate_statistics(dataset)

    # render the page
    return jsonify(counter)
