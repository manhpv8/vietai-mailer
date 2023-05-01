import codecs

def read_html_template(location_path: str) -> str:
    f=codecs.open(location_path, 'r')
    return f.read()