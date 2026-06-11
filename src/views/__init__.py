from flask import Blueprint

main_bp = Blueprint('main', __name__)

from src.views import main, api # noqa: F401, E402
