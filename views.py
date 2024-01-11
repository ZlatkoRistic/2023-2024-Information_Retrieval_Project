from flask import Blueprint, render_template, request, redirect, url_for
from main import fact_check

views = Blueprint(__name__, "views")


@views.route("/")
def home():
    return render_template("index.html")


@views.route("/submit", methods=["GET"])
def submit():
    args = request.args
    claim = args.get('claim')

    evidence_list = ["Geraldine Chaplin maintains a home in Granada, Spain.", "Earth is round", "Jennifer Aniston was married to Brad Pitt for five months."]
    evidence_string = '\n\n'.join(evidence_list)
    result = False
    # result = fact_check(claim, evidence_string)

    return render_template("evidence.html", claim=claim, result=result, evidence=["6678"])


@views.route("/show_document", methods=["GET"])
def show_document():
    args = request.args
    page = args.get('pagenr')

    page_name = str(page) + ".html"

    return render_template(page_name)

