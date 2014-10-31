import unicodedata

def normalize_value(value):
	if type(value) is unicode:
		return value.encode('ascii', 'replace')
	return value

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    only_ascii = nkfd_form.encode('ASCII', 'ignore')
    return only_ascii
