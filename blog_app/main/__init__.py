from flask import Blueprint
main = Blueprint("main", __name__, template_folder="templates")
import main_task
