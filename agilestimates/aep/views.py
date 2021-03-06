from django.shortcuts import render
import traceback

import session_manager
import crypt_utils
from django.db import connection as conn
from trello_scanner import scan as scan_trello
from aep.models import User, Profile, Customer, Project, Sprint, ProjectUser, Card
from utils.profile import build_profile, get_profile_list, get_profile, remove_profile, update_profile, create_profile
from datetime import date
import chart_generator
import json

def pending_scans(request):
    sprints = Sprint.objects.filter(date_scanned=None, end_date=date.today())
    projects = map(lambda s: {'sprint': s.description, 'project': s.project}, sprints)
    return render(request, 'pending_scans.html', {'sprintproj': projects, 'length': len(projects)})

def get_cards(request):
    sprint_id = request.GET['sprint_id']
    cards = Card.objects.filter(sprint__id=sprint_id)
    return render(request, 'card_list.html', {'cards': cards})

def get_project_sprints(request):
    project_name = request.GET['project_name']
    sprints = Sprint.objects.filter(project__name=project_name)
    return render(request, 'sprint_list.html', {'sprints': sprints})

def my_projects(request):
    user_name = session_manager.get_session_username(request)
    user_projects = ProjectUser.objects.filter(user__username=user_name)
    projects = map(lambda user_project: Project.objects.get(id=user_project.project_id), user_projects)
    return render(request, 'my_projects.html', {'projects': projects})

def generate_chart(request):
    project_id = request.GET['project']
    chart = request.GET['chart']
    if chart == 'points_per_sprint':
        sprints = Sprint.objects.filter(project__id=project_id)
        labels = map(lambda sprint: str(sprint.description), sprints)
        points = {'data': map(lambda sprint: sprint.points_delivered, sprints), 'title': 'Points Delivered'}
        chart = chart_generator.generate(labels, [points])
    elif chart == 'tests_per_sprint':
        sprints = Sprint.objects.filter(project__id=project_id)
        labels = map(lambda sprint: str(sprint.description), sprints)
        tests = {'data': map(lambda sprint: sprint.number_of_tests, sprints), 'title': 'Tests Created'}
        chart = chart_generator.generate(labels, [tests])
    elif chart == 'delivered_per_estimated_per_persprint':
        sprints = Sprint.objects.filter(project__id=project_id)
        labels = map(lambda sprint: str(sprint.description), sprints)
        points_estimated = {'data': map(lambda sprint: sprint.points_estimated, sprints), 'title': 'Points Estimated'}
        points_delivered = {'data': map(lambda sprint: sprint.points_delivered, sprints), 'title': 'Points Delivered'}
        chart = chart_generator.generate(labels, [points_estimated, points_delivered])
    elif chart == 'tests_per_estimated_per_persprint':
        sprints = Sprint.objects.filter(project__id=project_id)
        labels = map(lambda sprint: str(sprint.description), sprints)
        points_estimated = {'data': map(lambda sprint: sprint.number_of_tests, sprints), 'title': 'Tests Created'}
        points_delivered = {'data': map(lambda sprint: sprint.points_delivered, sprints), 'title': 'Points Delivered'}
        chart = chart_generator.generate(labels, [points_estimated, points_delivered])
    elif chart == 'us_per_sprint':
        sprints = Sprint.objects.filter(project__id=project_id)
        labels = map(lambda sprint: str(sprint.description), sprints)
        card_list = []
        sprint_list = []
        for sprint in sprints:
            card_list.append(Card.objects.filter(sprint__id=sprint.id).count())
            sprint_list.append(sprint.description)
        cards = {'data': card_list, 'title': 'Total Cards'}
        labels = sprint_list
        chart = chart_generator.generate(labels, [cards])

    jsonString = json.dumps(chart, ensure_ascii=False)
    return render(request, 'chart.html', {'chart': jsonString})

def admin_charts(request):
    projects = Project.objects.all()
    return render(request, 'admin_charts.html', {'projects': projects, 'profile': 'admin'})

def user_charts(request):
    projects = Project.objects.all()
    return render(request, 'admin_charts.html', {'projects': projects, 'profile': 'team'})

def logout(request):
    return session_manager.delete_session(request, render(request, 'logout.html'))

def get_customer_list():
    return map(lambda c: (c.id, c.name, c.country, c.operation_area), Customer.objects.all())

def get_user_list():
    users = map(lambda u: (u.id, u.name, u.username, u.password, u.email, u.profile.name), User.objects.all())
    return users

def get_user_list_from_project(project_id):
    return map(lambda u: (u.id, u.name, u.username), Project.objects.get(id=project_id).users.all())

def get_user_list_not_in_project(project_id):
    users_not_in = User.objects.exclude(id__in=map(lambda a: a[0], get_user_list_from_project(project_id)))
    return map(lambda u: (u.id, u.name, u.username, u.profile.name), users_not_in)

def get_user(id):
    return map(lambda u: (u.id, u.name, u.username, u.password, u.email, u.profile.name), [User.objects.get(id=id)])

def get_project(id):
    return map(lambda p: (p.id, p.name, p.trello_board, p.customer.name), [Project.objects.get(id=id)])

def get_project_list():
    return map(lambda p: (p.id, p.name, p.customer.name), Project.objects.all())

def user(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'users.html', {'users': get_user_list(), 'profiles': get_profile_list()})
    return render(request, 'login.html')

def project(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'projects.html', {'projects': get_project_list(), 'users': get_user_list(), 'customers': get_customer_list()})
    return render(request, 'login.html')

def build_user(user):
    return User(id=user[0], name=user[1], username=user[2], password=user[3], email=user[4], profile=build_profile(user[5]))

def build_customer(customer_id):
    c = get_customer(customer_id)[0]
    return Customer(id=c[0], name=c[1], country=c[2], operation_area=c[3])

def save_project_users(proj, user_list):
    for u in user_list:
        project_user = ProjectUser(project=proj, user=build_user(get_user(u)[0]))
        project_user.save()    

def save_project(request):
    name = request.POST['name']
    trello_board = request.POST['trello_board']
    customer_id = request.POST['customer']

    proj = Project(name=name, customer=build_customer(customer_id), trello_board=trello_board)
    proj.save()
    save_project_users(proj, request.POST.getlist('users[]'))

    return project(request)

def save_sprint(request):
    project = request.POST['project']
    description = request.POST['description']
    start_date = request.POST['start_date']
    end_date = request.POST['end_date']
    estimated_points = request.POST['estimated_points']
    
    cursor = conn.cursor()
    cursor.execute("insert into aep_sprint (project_id, description, start_date, end_date, points_estimated) "+
                   "values({0},'{1}','{2}','{3}',{4})".format(project, description, start_date, end_date, estimated_points))
    conn.commit()
    return sprint(request)

def delete_project(request, id):
    ProjectUser.objects.filter(project__id=id).delete()
    Project.objects.filter(id=id).delete()
    return project(request)

def edit_user(request, id):
    return render(request, 'edit_user.html', {'user': get_user(id), 'profiles': get_profile_list()})

def edit_project(request, id):
    print 'hdasudhsaudhasuhduashduashduashduahdusadhasudhasudhsua {0}'.format(get_project(id)[0][1])
    return render(request, 'edit_project.html',{'users_registered': get_user_list_from_project(id),
                                                'users_not_registered': get_user_list_not_in_project(id),
                                                'cust': get_project(id)[0][3],
                                                'project': get_project(id),
                                                'customers': get_customer_list()})

def save_edit_project(request):
    id = request.POST['id']
    name = request.POST['name']
    customer = request.POST['customer']
    cursor = conn.cursor()
    cursor.execute("update aep_project set name = '{0}', customer_id = {1}  where id = {2}".format(name, customer, id))
    ProjectUser.objects.filter(project__id=id).delete()
    for user in request.POST.getlist('users[]'):
        cursor.execute("insert into aep_user_project (user_id, project_id) values({0},{1})".format(user, id))
    conn.commit()
    return project(request)

def save_user(request):
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    password = crypt_utils.encrypt(password)
    email = request.POST['email']
    profile = request.POST['profile']
    cursor = conn.cursor()
    cursor.execute("insert into aep_user (name, username, password, email, profile_id) "+
                   "values('{0}','{1}','{2}', '{3}', {4})".format(name, username, password, email, profile))
    conn.commit()
    return user(request)

def save_edit_user(request):
    id = request.POST['id']
    name = request.POST['name']
    username = request.POST['username']
    email = request.POST['email']
    profile = request.POST['profile']
    cursor = conn.cursor()
    cursor.execute("update aep_user set name = '{0}', username = '{1}',  email = '{2}', profile_id = {3} where id = {4}".
                            format(name, username, email, profile, id))
    conn.commit()
    return user(request)

def delete_user(request, id):
    User.objects.filter(id=id).delete()
    return user(request)

def customer(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'customers.html', {'customers': get_customer_list()})
    return render(request, 'login.html')

def sprint(request):
    if session_manager.is_there_a_valid_session(request, 'Team'):
        return render(request, 'sprints.html', {'projects': get_project_list()})
    return render(request, 'login.html')

def scan(request):
    if session_manager.is_there_a_valid_session(request, 'Team'):
        return render(request, 'scan.html', {'projects': get_project_list()})
    return render(request, 'login.html')

def get_trello_id(project_id):
    return get_project(project_id)[0][2]

def get_sprint(project_id):
    sprint = Sprint.objects.filter(project__id=project_id, points_delivered=None)
    print sprint
    return sprint

def update_sprint(project_id, total_points_delivered, total_unit_tests):
    current_sprint = None
    try:
        sprint = Sprint.objects.filter(project__id=project_id, points_delivered=None)
        if len(sprint) == 0:
            return 'Sprint does not exist or already scanned'
        current_sprint = sprint[0]
        current_sprint.points_delivered=total_points_delivered
        current_sprint.number_of_tests=total_unit_tests
        current_sprint.date_scanned=date.today()
        current_sprint.save()
    except Exception as e:
        print e
    return ('Success', current_sprint)

def scan_process(request):
    try:
        project_id = request.GET['project_id']
        if len(get_sprint(project_id)) == 0:
            return render(request, 'log.html', {'cards': None, 'log': None, 'message': 'Sprint not found, please check if there is a sprint open', 'total_points_delivered': None, 'total_unit_tests': None})
        error, cards, log, total_unit_tests, total_points_delivered, card_list = scan_trello(get_trello_id(project_id))
        if error:
            return render(request, 'log.html', {'cards': None, 'log': log, 'message': 'Error', 'total_points_delivered': None, 'total_unit_tests': None})

        message, sprint = update_sprint(project_id, total_points_delivered, total_unit_tests)
        for card in card_list:
            card.sprint = sprint
            if card.end_date == '':
                card.end_date = date.today()
            card.save()
        log_final = []
        log_final.append('Customer: {0}'.format(sprint.project.customer.name))
        log_final.append('Sprint: {0}'.format(sprint.description))
        log_final.append('Period: from {0} to {1}'.format(sprint.start_date, sprint.end_date))
        log_final.append('')
        log_final.extend(log)

        return render(request, 'log.html', {'cards': cards, 'log': log_final, 'message': message, 'total_points_delivered': total_points_delivered, 'total_unit_tests': total_unit_tests})
    except:
        print traceback.format_exc()

def get_customer(id):
    return map(lambda c: (c.id, c.name, c.country, c.operation_area), [Customer.objects.get(id=id)])

def delete_customer(request, id):
    cursor = conn.cursor()
    cursor.execute("delete from aep_customer where id = {0}".format(id))
    conn.commit()
    return customer(request)

def edit_customer(request, id):
    return render(request, 'edit_customer.html', {'customers': get_customer(id)})

def save_edit_customer(request):
    id = request.POST['id']
    name = request.POST['name']
    country = request.POST['country']
    operation_area = request.POST['operation_area']
    cursor = conn.cursor()
    cursor.execute("update aep_customer set name = '{0}', country = '{1}', operation_area = '{2}' where id = {3}".
                            format(name, country, operation_area, id))
    conn.commit()
    return customer(request)

def profile(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'profiles.html', {'profiles': get_profile_list()})
    return render(request, 'login.html')

def save_profile(request):
    create_profile(request.POST['name'])
    return profile(request)

def delete_profile(request, id):
    remove_profile(id)
    return profile(request)

def save_edit_profile(request):
    update_profile(request.POST['id'], request.POST['name'])
    return profile(request)

def edit_profile(request, id):
    return render(request, 'edit_profile.html', {'profiles': get_profile(id)})

def save_customer(request):
    cust = Customer(name=request.POST['name'], country=request.POST['country'], operation_area=request.POST['operation_area'])
    cust.save()
    return customer(request)

def team(request):
    return render(request, 'team.html', {'userInfo':'cure'})

def admin(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'admin.html')
    return render(request, 'login.html')

def login(request):
    username = session_manager.get_session_username(request)

    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'admin.html', {'username': username})
    if session_manager.is_there_a_valid_session(request, 'Team'):
        return render(request, 'team.html', {'username': username})

    return render(request, 'login.html')

def get_user_information(username):
     return User.objects.filter(username=username)[0]

def login_process(request):
    username = request.POST['username']
    password = request.POST['password']
    user_info = get_user_information(username)
    
    if user_info.name is None or crypt_utils.decrypt(user_info.password) != password:
    	return render(request, 'login.html', {'error': 'username or password invalid'})
    
    if user_info.profile.name == 'Admin':
        response = render(request, 'admin.html', {'username': username})
    else:
        response = render(request, 'team.html', {'username': username})
    return session_manager.create_session(response, username)
