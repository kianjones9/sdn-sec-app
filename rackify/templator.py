from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader("rackify")
)
template = env.get_template("per_rack_con_net.jinja")

# from subprocess import call

def init_rack_network(templateVars: dict):

    # templateVars[]
    outputText = template.render( templateVars )

    print(outputText)