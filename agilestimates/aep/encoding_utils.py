def normalize_value(value):
	if type(value) is unicode:
		return value.encode('ascii', 'replace')
	return value