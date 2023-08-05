import re


def clean_query(query):
    query = re.sub(r"\n", "", query)
    return query
