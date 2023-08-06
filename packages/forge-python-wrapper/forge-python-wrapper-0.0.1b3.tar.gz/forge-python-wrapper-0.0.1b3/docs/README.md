# Forge Python Wrapper

Forge API Client Wrapper for Python

[![Python 3.7](https://img.shields.io/badge/python-3.7-blue.svg)](https://www.python.org/downloads/release/python-370)
[![Python 3.8](https://img.shields.io/badge/python-3.8-blue.svg)](https://www.python.org/downloads/release/python-380)

[![PyPI version](https://badge.fury.io/py/forge-python-wrapper.svg)](https://badge.fury.io/py/forge-python-wrapper)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/forge-python-wrapper.svg?label=pypi%20downloads)](https://pypi.org/project/forge-python-wrapper/)
[![Build Status](https://travis-ci.org/lfparis/forge-python-wrapper.svg?branch=master)](https://travis-ci.org/lfparis/forge-python-wrapper)
[![Coverage Status](https://coveralls.io/repos/github/lfparis/forge-python-wrapper/badge.svg?branch=master)](https://coveralls.io/github/lfparis/forge-python-wrapper?branch=master)

## Installing

```bash
pip install forge-python-wrapper
```

## Documentation

*Coming soon!*

### Usage Examples

```python
"""
If the following Environment Variables are defined there is no need to explicitly provide them when constructing the ForgeApp:
    For 2-legged context:
        FORGE_HUB_ID
        FORGE_CLIENT_ID
        FORGE_CLIENT_SECRET
    Extras for 3-legged context:
        FORGE_REDIRECT_URI
        FORGE_USERNAME
        FORGE_PASSWORD
"""

# 3-legged context - Needed to work with BIM 360 Team Hubs
app = ForgeApp(
    client_id="<your_app_client_id>",
    client_secret="<your_app_client_secret>",
    three_legged=True,
    redirect_uri="<your_app_redirect_uri>",
    username="<your_autodesk_username>",
    password="<your_autodesk_password>",
)

app.get_hubs()
app.hub_id = app.hubs[0]["id"]

app.get_projects(source="docs")
project = app.find_project("<Project Name>", key="name")
project = app.find_project("<Project Id>", key="id")

project.get_top_folders()
top_folders = project.top_folders

project.project_files.get_contents()
contents = project.project_files.contents

parent_folder_id = pj.project_files.id
project.add_folder(pj.project_files.id, "New Folder Name")


# 2-legged context - Needed for methods that use the BIM 360 API
app = ForgeApp(
    client_id="<your_app_client_id>",
    client_secret="<your_app_client_secret>",
    hub_id="<your_hub_id>",
)

app.get_companies()
company = app.find_company("Company Name")

app.get_users()
admin_user = app.find_user("admin_user@domain.com")
normal_user_1 = app.find_user("other_user_1@domain.com")
normal_user_2 = app.find_user("other_user_2@domain.com")

app.get_projects(source="all")

new_project = app.add_project("New Project Name")

new_project.update(name="Updated Project Name", status="active")

new_project.get_roles()
roles = new_project.roles
role_id = roles[0]["id"]

new_project.x_user_id = admin_user["uid"]
new_project.add_users([admin_user], access_level="admin")
new_project.add_users([normal_user_1, normal_user_2], access_level="user", role_id=role_id)

new_role_id = roles[1]["id"]
new_project.update_user(normal_user_1, company_id=company["id"], role_id=new_role_id)
```

## License
[MIT](https://opensource.org/licenses/MIT)