from apps.workspace.models import Workspace, getDashboardNameFromEmail
from apps.profile.models import Profile
from apps.task.models import Task

def signup(webtest_app, url, email, password, name=None):
    form = webtest_app.get(url).forms[0] #form 1 is the language one
    form['username'] = email
    form['email'] = email
    form['password1'] = password
    form['password2'] = password
    if name:
        form['first_name'] = name
    response = form.submit()
    try:
        workspace = Workspace.objects.get(name=getDashboardNameFromEmail(email))
        user = Profile.objects.get(workspace=workspace, user__username=email)
    except:
        workspace = None
        user = None
    return (response, workspace, user)

def dashboard_signup(webtest_app, email, password, name=None):
    return signup(webtest_app, '/signup/', email, password, name)

def client_signup(webtest_app, email, password, name=None):
    return signup(webtest_app, '/clientapp/register/', email, password, name)

def dashboard_login(webtest_app, username, password):
    form = webtest_app.get('/dashboard/login/').forms[0] #form 1 is the language one
    form['username'] = username
    form['password'] = password
    return form.submit()

def dashboard_create_task(webtest_app, name, owner, parent=None):
    form = webtest_app.get('/dashboard/task/new/').form
    form['name'] = name
    form['owner'] = owner.user.id
    if parent:
        form['parent'] = parent.id
    response = form.submit()
    task = Task.objects.get(workspace=owner.workspace, name=name, owner=owner)
    return (response, task)
