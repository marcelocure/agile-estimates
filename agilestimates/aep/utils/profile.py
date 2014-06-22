from django.db import connection as conn
from aep.models import Profile


def build_profile(profile_name):
    profile = filter(lambda p: p[1] == profile_name, get_profile_list())[0]
    return Profile(id=profile[0], name=profile[1])

def get_profile_list():
    return map(lambda p: (p.id, p.name), Profile.objects.all())

def get_profile(id):
    profile = Profile.objects.get(id=id)
    return [(profile.id, profile.name)]

def remove_profile(id):
	Profile.objects.filter(id=id).delete()

def update_profile(id, name):
	cursor = conn.cursor()
	cursor.execute("update aep_profile set name = '{0}' where id = {1}".format(name, id))
	conn.commit()

def create_profile(name):
	prof = Profile(name=name)
	prof.save()