from string import Template

def t(template, **kwargs):
    new = Template(template)
    return new.substitute(kwargs)
