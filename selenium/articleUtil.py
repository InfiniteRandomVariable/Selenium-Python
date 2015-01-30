import re


def truncatedStringForRow(text, WORD_LIMIT=250):
	if len(text) > (WORD_LIMIT -2):
		## tpC = re.sub(r'\.*$',"", text)
		return "%s..." % re.sub(r'\.+$',"", text.strip()[0:WORD_LIMIT])
	else:
		return text
