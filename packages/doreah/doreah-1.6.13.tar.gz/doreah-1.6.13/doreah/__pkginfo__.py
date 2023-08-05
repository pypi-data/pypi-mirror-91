name = "doreah"
desc = "Small toolkit of utilities for python projects"

version = 1,6,13
versionstr = ".".join(str(n) for n in version)

author = {
	"name": "Johannes Krattenmacher",
	"email": "python@krateng.dev",
	"github": "krateng"
}

requires = [
	"lxml",
	"mechanicalsoup",
	"requests",
	"pyyaml",
	"beautifulsoup4",
	"jinja2>2.11"
]
resources = [
	'res/*',
	'res/*/*',
	'res/*/*/*'
]

commands = {
	"pyhpserver":"pyhp2:run_testserver"
}
