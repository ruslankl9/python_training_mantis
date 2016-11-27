from model.project import Project
import random

def test_delete_some_project(app):
    if len(app.project.get_project_list()) == 0:
        app.project.create(Project(name="Some Project ({0})".format(random.randrange(1, 999999)), status="выпущен",
                                   view_state="приватная", description="Some Project Description", active=True))
    old_projects = app.project.get_project_list()
    project = random.choice(old_projects)
    app.project.delete_project_by_id(project.id)
    new_projects = app.project.get_project_list()
    assert len(old_projects) - 1 == len(new_projects)
    old_projects.remove(project)
    assert old_projects == new_projects