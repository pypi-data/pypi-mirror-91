# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['postgrest_py']

package_data = \
{'': ['*']}

install_requires = \
['deprecation>=2.1.0,<3.0.0', 'httpx>=0.16.1,<0.17.0']

setup_kwargs = {
    'name': 'postgrest-py',
    'version': '0.4.0',
    'description': 'PostgREST client for Python. This library provides an ORM interface to PostgREST.',
    'long_description': '[![](https://img.shields.io/github/license/supabase/postgrest-py)](https://github.com/supabase/postgrest-py)\n[![](https://img.shields.io/pypi/pyversions/postgrest-py)](https://pypi.org/project/postgrest-py)\n[![](https://img.shields.io/pypi/v/postgrest-py)](https://pypi.org/project/postgrest-py)\n\n# postgrest-py\n\nPostgREST client for Python. This library provides an ORM interface to PostgREST.\n\nStatus: **Unstable**\n\n## INSTALLATION\n\n### Requirements\n\n- Python >= 3.7\n- PostgreSQL >= 12\n- PostgREST >= 7\n\n### Instructions\n\n#### With Poetry (recommended)\n\n```sh\n$ poetry add postgrest-py\n```\n\n#### With Pip\n\n```sh\n$ pip install postgrest-py\n```\n\n## USAGE\n\n### Getting started\n\n```py\nimport asyncio\nfrom postgrest_py import PostgrestClient\n\nasync def main():\n    async with PostgrestClient("http://localhost:3000") as client:\n        r = await client.from_("countries").select("*").execute()\n        countries = r.json()\n\nasyncio.run(main())\n```\n\n### Create\n\n```py\nawait client.from_("countries").insert({ "name": "Việt Nam", "capital": "Hà Nội" }).execute()\n```\n\n### Read\n\n```py\nr = await client.from_("countries").select("id", "name").execute()\ncountries = r.json()\n```\n\n### Update\n\n```py\nawait client.from_("countries").eq("name", "Việt Nam").update({"capital": "Hà Nội"}).execute()\n```\n\n### Delete\n\n```py\nawait client.from_("countries").eq("name", "Việt Nam").delete().execute()\n```\n\n### General filters\n\n### Stored procedures (RPC)\n\n## DEVELOPMENT\n\n```sh\n$ git clone https://github.com/supabase/postgrest-py.git\n$ cd postgrest-py\n$ poetry install\n```\n\n### Testing\n\n```sh\n$ poetry run pytest\n```\n\n## CHANGELOG\n\nRead more [here](https://github.com/supabase/postgrest-py/blob/master/CHANGELOG.md).\n\n## TODO\n\nRead more [here](https://github.com/supabase/postgrest-py/blob/master/TODO.md).\n\n## SPONSORS\n\nWe are building the features of Firebase using enterprise-grade, open source products. We support existing communities wherever possible, and if the products don’t exist we build them and open source them ourselves. Thanks to these sponsors who are making the OSS ecosystem better for everyone.\n\n[![Worklife VC](https://user-images.githubusercontent.com/10214025/90451355-34d71200-e11e-11ea-81f9-1592fd1e9146.png)](https://www.worklife.vc)\n[![New Sponsor](https://user-images.githubusercontent.com/10214025/90518111-e74bbb00-e198-11ea-8f88-c9e3c1aa4b5b.png)](https://github.com/sponsors/supabase)\n',
    'author': 'Lương Quang Mạnh',
    'author_email': 'luongquangmanh85@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/supabase/postgrest-py',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
