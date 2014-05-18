from django.http import HttpResponse
import views

def create_session(response, conn, cursor, username):
	cursor.execute("insert into aep_session (username, login_date) values('{0}', now()) returning id".format(username))
	session_id = cursor.fetchone()[0]
	conn.commit()

	print 'session id {0} created'.format(session_id)

	response.set_cookie("aep_session", session_id)
	response.set_cookie("aep_username", username)
	return response


def get_session_id(request):
	session_id = None
	try:
		session_id = request.COOKIES['aep_session']
	except:
		session_id = 0

	return session_id


def get_session_username(request):
	session_username = None
	try:
		session_username = request.COOKIES['aep_username']
	except:
		session_username = 'xxxxxxx'
	return session_username


def is_there_a_valid_session(request, profile):
	session_id = get_session_id(request)
	session_username = get_session_username(request)
	conn, cursor = views.connect()
	cursor.execute("select count(1) from aep_session s, aep_user u, aep_profile p where s.username = u.username and u.id_profile = p.id"+
		" and s.username = '{0}' and s.id = {1} and p.name = '{2}'".format(session_username, session_id, profile))
	session_count = cursor.fetchone()[0]
	if session_count > 0:
		return True
	return False


def delete_session(request, response):
	conn, cursor = views.connect()

	session_id = get_session_id(request)

	print 'removing session id {0}'.format(session_id)
	cursor.execute("delete from aep_session where id = {0}".format(session_id))
	conn.commit()

	response.delete_cookie('aep_session')
	response.delete_cookie('aep_username')
	return response
