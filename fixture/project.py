import re
from model.project import Project

class ProjectHelper(object):

    def __init__(self, app):
        self.app = app
        self.project_cache = None

    def change_field_value(self, field_name, text):
        wd = self.app.wd
        if text is not None:
            wd.find_element_by_name(field_name).click()
            wd.find_element_by_name(field_name).clear()
            wd.find_element_by_name(field_name).send_keys(text)

    def change_select_value(self, select_name, value):
        wd = self.app.wd
        if value is not None:
            xpath_str = "//select[@name='{select_name}']//option[@value='{value}']".format(
                select_name=select_name, value=value
            )
            if not wd.find_element_by_xpath(xpath_str).is_selected():
                wd.find_element_by_xpath(xpath_str).click()

    def change_check_value(self, check_name, value):
        wd = self.app.wd
        xpath_str = "//input[@name='{check_name}']".format(check_name=check_name)
        if wd.find_element_by_xpath(xpath_str).is_selected() != value:
            wd.find_element_by_xpath(xpath_str).click()

    def open_manage_overview_page(self):
        wd = self.app.wd
        wd.find_element_by_css_selector("a.manage-menu-link").click()

    def open_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("/manage_proj_page.php"):
            if not wd.current_url.endswith("/manage_overview_page.php"):
                self.open_manage_overview_page()
            wd.find_element_by_css_selector("div#manage-menu ul li:nth-child(2) a").click()

    def fill_project_form(self, project):
        status_values = {
            'в разработке': '10',
            'выпущен': '30',
            'стабильный': '50',
            'устарел': '70'
        }
        view_state_values = {
            'публичная': '10',
            'приватная': '50'
        }
        self.change_field_value("name", project.name)
        self.change_select_value("status", status_values[project.status])
        self.change_select_value("view_state", view_state_values[project.view_state])
        self.change_field_value("description", project.description)

    def return_to_projects_page(self):
        wd = self.app.wd
        if not wd.current_url.endswith("manage_proj_page.php"):
            wd.find_element_by_xpath("//div/div[4]/div/span/a").click()

    def create(self, project):
        wd = self.app.wd
        self.open_projects_page()
        # init project creation
        wd.find_element_by_css_selector("form[action='manage_proj_create_page.php'] input[type='submit']").click()
        self.fill_project_form(project)
        # submit project creation
        wd.find_element_by_css_selector("form#manage-project-create-form input[type='submit']").click()
        self.return_to_projects_page()
        self.project_cache = None

    def open_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        link = wd.find_element_by_css_selector("a[href='manage_proj_edit_page.php?project_id={0}']".format(id))
        link.click()

    def delete_project_by_id(self, id):
        wd = self.app.wd
        self.open_projects_page()
        self.open_project_by_id(id)
        # submit deletion
        wd.find_element_by_css_selector("form#project-delete-form input[type='submit']").click()
        # click confirm button
        wd.find_element_by_css_selector("#content input[type='submit']").click()
        self.return_to_projects_page()
        self.project_cache = None

    def get_project_list(self):
        if self.project_cache is None:
            wd = self.app.wd
            self.open_projects_page()
            self.project_cache = []
            for tr in wd.find_elements_by_css_selector("#content div:nth-child(2) tbody tr"):
                href = tr.find_element_by_css_selector("td:nth-child(1) a").get_attribute("href")
                id = re.findall(r"\?project_id=(\d+)", href)[0]
                name = tr.find_element_by_css_selector("td:nth-child(1) a").text
                status = tr.find_element_by_css_selector("td:nth-child(2)").text
                active = tr.find_element_by_css_selector("td:nth-child(3)").text.strip() == "X"
                view_state = tr.find_element_by_css_selector("td:nth-child(4)").text
                description = tr.find_element_by_css_selector("td:nth-child(5)").text
                self.project_cache.append(Project(id=id, name=name, status=status, active=active, view_state=view_state,
                                                description=description))
        return list(self.project_cache)