from flask import Blueprint
user = Blueprint("user", __name__, template_folder="templates")
import user_task
