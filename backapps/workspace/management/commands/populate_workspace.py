from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from backapps.workspace.models import Workspace
import libs.chart.generate_data as gen
import dateutil.parser

class Command(BaseCommand):
    args = u"""<workspace_name username number_of_users number_of_tasks 
start_date end_date>"""
    help = u'Populate the workspace with fake generated data'
    def handle(self, * args, ** options):
        self.stdout.write(u'Analyze arguments')
        (ws_name, username, users_nb, tasks_nb, start, end) = args

        ws = Workspace.objects.get(name=ws_name)
        user = User.objects.get(username=username)
        users_nb = int(users_nb)
        tasks_nb = int(tasks_nb)
        start = dateutil.parser.parse(start)
        end = dateutil.parser.parse(end)

        self.stdout.write(u'Clean database')
        gen.clean_records(ws)
        gen.clean_tasks(ws)
        gen.clean_users(ws, user)
        self.stdout.write(u'Generate users')
        gen.generate_users(ws, users_nb)
        self.stdout.write(u'Generate tasks')
        gen.generate_tasks(ws, user, tasks_nb)
        self.stdout.write(u'Generate records')
        gen.generate_records(ws, start, end)
        self.stdout.write(u'done')
