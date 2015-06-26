from lettuce import before, step, world
from lettuce.django import django_url
from splinter.browser import Browser


@before.all
def set_browser():
    # world.browser = Browser('zope.testbrowser')
    world.browser = Browser('firefox')


@step(r'I am on Busine.me homepage')
def i_am_on_busineme_home_page(step):
    """Verify if the actual page is the homepage of the application."""
    name = "/"
    full_url = django_url(name)
    world.browser.response = world.browser.visit(full_url)


@step(r'I am on Busine.me loginpage')
def i_am_on_busineme_login_page(step):
    """Verify if the actual page is the loginpage of the application."""
    name = "/login/"
    full_url = django_url(name)
    world.browser.response = world.browser.visit(full_url)


@step('I type "(.*)" in the field "(.*)"')
def i_type_value_in_the_field_field_name(step, value, field_name):
    """Enter the predefined values on predefined field."""
    world.browser.fill(field_name, value)


@step('I press "(.*)"')
def i_press(step, button):
    """Activate the predefined button."""
    world.browser.find_by_value(button).first.click()


@step(r'I should see "(.*)"')
def i_should_see(step, value):
    r"""
    Verify if the header text of the actual page\
    matches the predefined string for this field.
    """
    world.browser.find_by_value(value).first


@step('I should see a description saying "(.*)"')
def i_should_see_a_description(step, value):
    r"""
    Verify if the displayed description string matches\
    with the expected description string for this field.
    """
    header = world.browser.find_by_tag('h4')[0]  # first result
    assert header.text == value


@step('I follow "(.*)"')
def i_follow(step, link):
    """go to specifyed link"""
    world.browser.click_link_by_href(link)


@step('I should see a message saying "Erro"')
def i_should_see_an_error_message(step):
    r"""
    Verify if the message that was displayed starts\
    with the predefined string for this field.
    """
    world.browser.find_by_css("h2").first.value


# @step('Then I should see "(.*)"')
# def then_i_should_see(step, value):
#     r"""
#     Verify if the displayed description string matches\
#     with the expected description string for this field.
#     """
#     world.browser.find_by_css('h3').first.value

# @step('I press "Businar!"')
# def i_press_post(step):
#     r"""
#     Verify if when the post button is activated\
#     the "/realizar_post/" url is called.
#     """

#     world.browser.click_link_by_text("Businar!")
