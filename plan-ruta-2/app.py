import importlib
from .modelos import db
from flask_restful import Api
from .vistas import vistaCrearPlanRuta

planRuta2 = importlib.import_module("plan-ruta-2")
app = planRuta2.create_app('default')
app_context = app.app_context()
app_context.push()

db.init_app(app)
db.create_all()

api = Api(app)
api.add_resource(vistaCrearPlanRuta, '/plan-ruta-2')