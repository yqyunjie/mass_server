import os
from flask import Blueprint
from flask_apscheduler import APScheduler

from mass_flask_scheduling.tasks import schedule_analyses

scheduling_blueprint = Blueprint('mass_flask_scheduling', __name__, template_folder='templates', static_folder='static')
scheduler = APScheduler()


@scheduling_blueprint.record_once
def on_load(state):
    if 'MASS_TESTING' in state.app.config and state.app.config['MASS_TESTING'] is True:
        print('Not starting scheduler when MASS_TESTING=True')
        return
    elif not state.app.debug or os.environ.get('WERKZEUG_RUN_MAIN') == 'true':
        scheduler.init_app(state.app)
        scheduler.add_job('schedule_analyses', schedule_analyses, trigger='interval', seconds=state.app.config['SCHEDULE_ANALYSES_INTERVAL'])
        scheduler.start()
