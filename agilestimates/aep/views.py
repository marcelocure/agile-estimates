from django.shortcuts import render, render_to_response, RequestContext
import psycopg2
import session_manager
import crypt_utils
from django.db import connection as conn

def connect():
    return conn, conn.cursor()
 

def index(request):
    return render(request, 'index.html', {'userInfo':'cure'})


def admin(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render(request, 'admin.html')
    return render(request, 'login.html')


def login(request):
    return render(request, 'login.html')


def logout(request):
    response = render(request, 'logout.html')
    return session_manager.delete_session(request, response)


def get_customer_list():
    conn, cursor = connect()
    cursor.execute("select id, name, country, operation_area from aep_customer order by id")
    rows = cursor.fetchall()
    return {'customers': rows}


def get_user_list():
    conn, cursor = connect()
    cursor.execute("select u.id, u.name, u.username, u.password, u.email, p.name as profile from aep_user u, aep_profile p where p.id = u.id_profile order by u.id")
    rows = cursor.fetchall()
    return {'users': rows, 'profiles': get_profile_list()['profiles']}


def get_user_list_from_project(id_project):
    conn, cursor = connect()
    cursor.execute("select u.id, u.name, u.username from aep_user u, aep_user_project p where p.id_project = {0} and u.id = p.id_user order by u.id".format(id_project))
    rows = cursor.fetchall()
    return {'users_registered': rows}


def get_user_list_not_in_project(id_project):
    conn, cursor = connect()
    cursor.execute("select u.id, u.name, u.username from aep_user u where u.id not in (select p.id_user from aep_user_project p where p.id_project = {0}) order by u.id".format(id_project))
    rows = cursor.fetchall()
    return {'users_not_registered': rows}


def get_user(id):
    conn, cursor = connect()
    cursor.execute("select u.id, u.name, u.username, u.password, u.email, p.name as profile "+
        "from aep_user u, aep_profile p where p.id = u.id_profile and u.id = {0}".format(id))
    rows = cursor.fetchall()
    return {'users': rows, 'profiles': get_profile_list()['profiles']}


def get_project(id):
    conn, cursor = connect()
    cursor.execute("select p.id, p.name, c.name as customer "+
        "from aep_project p, aep_customer c where c.id = p.id_customer and p.id = {0}".format(id))
    rows = cursor.fetchall()
    return {'projects': rows, 'customers': get_customer_list()['customers']}


def get_project_list():
    conn, cursor = connect()
    cursor.execute("select p.id, p.name, c.name as customer from aep_project p, aep_customer c where c.id = p.id_customer order by p.id")
    rows = cursor.fetchall()
    return {'projects': rows, 'customers': get_customer_list()['customers']}


def user(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render_to_response('users.html', get_user_list(), context_instance=RequestContext(request))
    return render(request, 'login.html')


def project(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render_to_response('projects.html', get_project_list(), context_instance=RequestContext(request))
    return render(request, 'login.html')


def save_project(request):
    name = request.POST['name']
    customer = request.POST['customer']
    
    conn, cursor = connect()
    cursor.execute("insert into aep_project (name, id_customer) "+
                   "values('{0}',{1})".format(name, customer))
    conn.commit()

    return project(request)


def delete_project(request, id):
    conn, cursor = connect()
    cursor.execute("delete from aep_project where id = {0}".format(id))
    conn.commit()

    return project(request)


def edit_user(request, id):
    return render_to_response('edit_user.html', get_user(id), context_instance=RequestContext(request))


def edit_project(request, id):
    return render_to_response('edit_project.html',{'users_registered': get_user_list_from_project(id)['users_registered'], 'users_not_registered': get_user_list_not_in_project(id)['users_not_registered'], 'projects': get_project(id)['projects'], 'customers': get_project(id)['customers']}, context_instance=RequestContext(request))


def parse_post(post_data):
    s = str(post_data)
    if s.find("u'users[]':") == -1:
        return []
    pos = s.find("u'users[]':") + 13
    s = s[pos:]
    s = s[:s.find("]")]
    s =  s.replace("u","").replace(" ","").replace("'","")
    return s.split(",")


def save_edit_project(request):
    id = request.POST['id']
    name = request.POST['name']
    customer = request.POST['customer']
    print request.POST
    users = parse_post(request.POST)
    print users

    conn, cursor = connect()
    cursor.execute("update aep_project set name = '{0}', id_customer = {1}  where id = {2}".
                            format(name, customer, id))
    
    cursor.execute("delete from aep_user_project where id_project = {0}".format(id))
    for user in users:
        cursor.execute("insert into aep_user_project (id_user, id_project) values({0},{1})".format(user, id))

    conn.commit()

    return project(request)


def save_user(request):
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    password = crypt_utils.encrypt(password)
    email = request.POST['email']
    profile = request.POST['profile']

    conn, cursor = connect()
    cursor.execute("insert into aep_user (name, username, password, email, id_profile) "+
                   "values('{0}','{1}','{2}', '{3}', {4})".format(name, username, password, email, profile))
    conn.commit()

    return user(request)


def save_edit_user(request):
    id = request.POST['id']
    name = request.POST['name']
    username = request.POST['username']
    password = request.POST['password']
    email = request.POST['email']
    profile = request.POST['profile']
    conn, cursor = connect()
    cursor.execute("update aep_user set name = '{0}', username = '{1}', password = '{2}', email = '{3}', id_profile = {4} where id = {5}".
                            format(name, username, password, email, profile, id))
    conn.commit()

    return user(request)


def delete_user(request, id):
    conn, cursor = connect()
    cursor.execute("delete from aep_user where id = {0}".format(id))
    conn.commit()

    return user(request)


def customer(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render_to_response('customers.html', get_customer_list(), context_instance=RequestContext(request))
    return render(request, 'login.html')


def get_customer(id):
    conn, cursor = connect()
    cursor.execute("select id, name, country, operation_area from aep_customer where id = {0}".format(id))
    rows = cursor.fetchall()
    return {'customers': rows}


def delete_customer(request, id):
    conn, cursor = connect()
    cursor.execute("delete from aep_customer where id = {0}".format(id))
    conn.commit()

    return customer(request)


def edit_customer(request, id):
    return render_to_response('edit_customer.html', get_customer(id), context_instance=RequestContext(request))


def save_edit_customer(request):
    id = request.POST['id']
    name = request.POST['name']
    country = request.POST['country']
    operation_area = request.POST['operation_area']
    conn, cursor = connect()
    cursor.execute("update aep_customer set name = '{0}', country = '{1}', operation_area = '{2}' where id = {3}".
                            format(name, country, operation_area, id))
    conn.commit()

    return customer(request)


def get_profile_list():
    conn, cursor = connect()
    cursor.execute("select id, name from aep_profile order by id")
    rows = cursor.fetchall()
    return {'profiles': rows}


def get_profile(id):
    conn, cursor = connect()
    cursor.execute("select id, name from aep_profile where id = {0}".format(id))
    rows = cursor.fetchall()
    return {'profiles': rows}

def profile(request):
    if session_manager.is_there_a_valid_session(request, 'Admin'):
        return render_to_response('profiles.html', get_profile_list(), context_instance=RequestContext(request))
    return render(request, 'login.html')


def save_profile(request):
    name = request.POST['name']
    conn, cursor = connect()
    cursor.execute("insert into aep_profile (name) values('{0}')".format(name))
    conn.commit()

    return profile(request)


def delete_profile(request, id):
    conn, cursor = connect()
    cursor.execute("delete from aep_profile where id = {0}".format(id))
    conn.commit()

    return profile(request)


def save_edit_profile(request):
    id = request.POST['id']
    name = request.POST['name']
    conn, cursor = connect()
    cursor.execute("update aep_profile set name = '{0}' where id = {1}".format(name, id))
    conn.commit()

    return profile(request)


def edit_profile(request, id):
    return render_to_response('edit_profile.html', get_profile(id), context_instance=RequestContext(request))


def save_customer(request):
    name = request.POST['name']
    country = request.POST['country']
    operation_area = request.POST['operation_area']

    conn, cursor = connect()
    cursor.execute("insert into aep_customer (name, country, operation_area) "+
                   "values('{0}','{1}','{2}')".format(name, country, operation_area))
    conn.commit()

    return customer(request)
def get_encrypted_password(username):
    conn, cursor = connect()
    cursor.execute("select password from aep_user where username = '{0}'".format(username))
    return cursor.fetchone()[0]


def login_process(request):
    username = request.POST['username']
    password = request.POST['password']
    conn, cursor = connect()
    encrypted_password = get_encrypted_password(username)
    
    cursor.execute("select u.name, p.name from aep_user u, aep_profile p " +
                "where u.id_profile = p.id and u.username = '{0}'".format(username))
    name, profile = cursor.fetchone()
    print crypt_utils.decrypt(encrypted_password)
    print password
    
    if name is None or crypt_utils.decrypt(encrypted_password) != password:
    	return render(request, 'login.html', {'error': 'username or password invalid'})
    
    if profile == 'Admin':
        response = render(request, 'admin.html')
    else:
        response = render(request, 'index.html')

    return session_manager.create_session(response, conn, cursor, username)
