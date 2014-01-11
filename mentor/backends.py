import ldap
from djangocas.backends import CASBackend
from mentor.users.models import User 
from django.conf import settings
from django.core.exceptions import PermissionDenied

class PSUBackend(CASBackend):
	def get_or_init_user(self, username):
		try:
			user = User.objects.get(username=username)
		except User.DoesNotExist:
			# user will have an "unusable" password
			user = User.objects.create_user(username, '')
			user.save()


		if settings.DEBUG:
			pass
		else:
			# get the user's first and lastname
			ld = ldap.initialize(settings.LDAP_URL)
			ld.simple_bind_s()
			results = ld.search_s(settings.LDAP_BASE_DN, ldap.SCOPE_SUBTREE, "uid=" + username)
			record = results[0][1]
			cn = record['cn']
			parts = cn[0].split(" ")
			user.first_name = parts[0]
			user.last_name = " ".join(parts[1:])
			mail = record['mail'][0]
			user.email = mail
			user.save()

		return user