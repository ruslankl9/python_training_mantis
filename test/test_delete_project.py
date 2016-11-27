from model.project import Project
import random

def test_delete_some_project(app):
    app.session.ensure_login(username=app.config['webadmin']['username'], password=app.config['webadmin']['password'])
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="Some Project ({0})".format(random.randrange(1, 999999)), status="release",
                                   view_state="private", description="Some Project Description", active=True))
    old_projects = app.project.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.project.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects