# This converts a valid string to a list
import ast

def stolist(stringlist):
    try:
        plain_string = stringlist.replace(']', '').replace('[', '').replace("'", '').replace('"', '').replace('"', '')
        plain_string = plain_string.replace('{', '').replace('}', '')
        plain_string = plain_string.replace('\n', '')
        plain_string = plain_string.split(',')
        cleaned_array = []
        for g in plain_string:
            cleaned_array.append(g.lstrip())

        return cleaned_array
    except Exception:
        return []

def stolist2(stringlist):
    try:
        cleaned_array = ast.literal_eval(stringlist)

        return cleaned_array
    except Exception:
        return []
