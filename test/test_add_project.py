from model.project import Project
import random

def test_add_project(app):
    app.session.ensure_login(username=app.config['webadmin']['username'], password=app.config['webadmin']['password'])
    old_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    project = Project(name="New Project ({0})".format(random.randrange(1, 999999)),
                      status="development", view_state="public", description="New Project Description", active=True)
    app.project.create(project)
    new_projects = app.soap.get_project_list(app.config['webadmin']['username'], app.config['webadmin']['password'])
    old_projects.append(project)
    assert sorted(old_projects, key=Project.id_or_max) == sorted(new_projects, key=Project.id_or_max)