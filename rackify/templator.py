import os
from jinja2 import Environment, PackageLoader
env = Environment(
    loader=PackageLoader("rackify")
)
template = env.get_template("per_rack_con_net.jinja")

# from subprocess import call

def init_rack_network(templateVars: dict):

    outputText = template.render( templateVars )

    os.system(outputText)