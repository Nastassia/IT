from time import gmtime, strftime
import re
import ldap
import ldap.modlist


OU = 'ou=automatedtest,dc=wot,dc=io'

def ldap_init(server):
	l = None

	try:
		l = ldap.open(server)
	except ldap.LDAPError, (e):
		print "Error: %s" % (e)
		raise e

	return l

def ldap_connect(server, bind_dn, password):
	l = ldap_init(server)
	l.simple_bind_s(bind_dn, password)
	return l

def ldap_bind(server, bind_dn, password):
	l = None
	try:
		l = ldap_connect(server, bind_dn, password)
	except ldap.INVALID_CREDENTIALS:
		return 2
	except ldap.LDAPError, (e):
		print "Error: %s" % (e)
		return 3
	finally:
		if l: l.unbind_s()

	return 0

# TODO(agy) Checks only the first result returned -- should probably be smarter.
def ldap_search(server, bind_dn, password, base, filter, attribute='cn', expected='.*'):
	l = None
	try:
		l = ldap_connect(server, bind_dn, password)
		results = l.search_s(base, ldap.SCOPE_SUBTREE, filter, [attribute])

		for dn, entry in results:
			result = entry.get(attribute)
			if result:
				if re.match(expected, result[0]):
					return 0
			return 2
	except ldap.LDAPError, (e):
		print "Error: %s" % (e)
		return 2
	finally:
		if l: l.unbind_s()

	return 3

def ldap_create_ou(server, bind_dn, password, dn=OU):
	ou = dn.split(',')[0]
	if not ou:
		return 3

	attrs = {}
	attrs['objectclass'] = ['organizationalUnit']
	attrs['ou'] = ou
	attrs['description'] = 'Created on %s' % strftime("%Y-%m-%d %H:%M:%S", gmtime())

	l = None
	try:
		l = ldap_connect(server, bind_dn, password)
		mod = ldap.modlist.addModlist(attrs)
		l.add_s(dn, mod)
		return 0
	except ldap.LDAPError, (e):
		print "Error: %s" % (e)
		return 2
	finally:
		if l: l.unbind_s()

def ldap_remove_ou(server, bind_dn, password, dn=OU):
	l = None
	try:
		l = ldap_connect(server, bind_dn, password)
		l.delete_s(dn)
		return 0
	except ldap.LDAPError, (e):
		print "Error: %s" % (e)
		return 2
	finally:
		if l: l.unbind_s()

def ldap_read_ou(server, bind_dn, password, base, filter, attribute='ou'):
	x = ldap_search(server, bind_dn, password, base, filter, attribute)
	return x

def ldap_crud(server, bind_dn, password):
	base = OU
	filter = '(' + OU.split(',')[0] + ')'
	value = 0
	x = ldap_create_ou(server, bind_dn, password, dn=OU)
	if x > value: value = x
	x = ldap_read_ou(server, bind_dn, password, base, filter)
	if x > value: value = x
	x = ldap_remove_ou(server, bind_dn, password, dn=OU)
	if x > value: value = x
	return value
