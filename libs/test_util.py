from selenium.webdriver.support.ui import Select
from workspace.models import Workspace, getDashboardNameFromEmail
from profile.models import Profile
from task.models import Task

#
# Helpers for WebTest (django_webtest)
#
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
    form = webtest_app.get('/login/').forms[0] #form 1 is the language one
    form['username'] = username
    form['password'] = password
    return form.submit()

def dashboard_create_task(webtest_app, name, owner, parent=None):
    form = webtest_app.get('/task/new/').form
    form['name'] = name
    form['owner'] = owner.user.id
    if parent:
        form['parent'] = parent.id
    response = form.submit()
    task = Task.objects.get(workspace=owner.workspace, name=name, owner=owner)
    return (response, task)

#
# Helpers for LiveServerTestCase (Selenium)
#
def selenium_signup(live_server, url, email, password, name=None):
    live_server.selenium.get('%s%s' % (live_server.live_server_url, url))
    live_server.selenium.find_element_by_name("email").send_keys(email)
    if name:
        live_server.selenium.find_element_by_name("first_name").send_keys(name)
    field = live_server.selenium.find_element_by_name("username")
    field.clear()
    field.send_keys(email)
    live_server.selenium.find_element_by_name("password1").send_keys(password)
    live_server.selenium.find_element_by_name("password2").send_keys(password)
    response = live_server.selenium.find_element_by_name("signup").click()
    try:
        workspace = Workspace.objects.get(name=getDashboardNameFromEmail(email))
        user = Profile.objects.get(workspace=workspace, user__username=email)
    except:
        workspace = None
        user = None
    return (response, workspace, user)

def selenium_dashboard_signup(live_server, email, password, name=None):
    return selenium_signup(live_server, '/signup/', email, password, name)

def selenium_client_signup(live_server, email, password, name=None):
    return selenium_signup(live_server, '/clientapp/register/', email, password, name)

def selenium_login(live_server, url, username, password):
    live_server.selenium.get('%s%s' % (live_server.live_server_url, url))
    live_server.selenium.find_element_by_name("username").send_keys(username)
    live_server.selenium.find_element_by_name("password").send_keys(password)
    response = live_server.selenium.find_element_by_name("login").click()
    try:
        user = Profile.objects.get(workspace=workspace, user__username=username)
        workspace = user.workspace
    except:
        workspace = None
        user = None
    return (response, workspace, user)

def selenium_dashboard_login(live_server, email, password):
    return selenium_login(live_server, '/login/', email, password)

def selenium_client_login(live_server, email, password):
    return selenium_login(live_server, '/clientapp/login/', email, password)

def selenium_dashboard_create_task(live_server, name, owner, parent=None):
    live_server.selenium.get('%s%s' % (live_server.live_server_url, '/task/new/'))
    live_server.selenium.find_element_by_name("name").send_keys(name)
    Select(live_server.selenium.find_element_by_name("owner")
                                        ).select_by_value((owner.user.id,))
    if parent:
        Select(live_server.selenium.find_element_by_name("parent")
                                        ).select_by_value((parent.id,))
    response = live_server.selenium.find_element_by_id("creation").click()
    task = Task.objects.get(workspace=owner.workspace, name=name, owner=owner)
    return (response, task)
