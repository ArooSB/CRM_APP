from flask import Blueprint

api = Blueprint('api', __name__)

from .customers import *
from .workers import *
from .sales_leads import *
from .interactions import *
from .support_tickets import *
from .analytics import *
