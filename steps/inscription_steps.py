import pytest
from pytest_bdd import given, when, then, scenarios
from selenium.webdriver.common.by import By
from pages.inscription_page import InscriptionPage

scenarios('../features/inscription.feature')


@given('I am on the "Registration" page', target_fixture='page')
def open_page(driver):
    page = InscriptionPage(driver)
    page.open()
    return page


@given('I fill the registration form as a student')
def fill_student(page):
    page.fill_student_form()


@given('I fill the registration form as a searcher')
def fill_searcher(page):
    page.fill_searcher_form()


@given('I fill the registration form as an institutional user')
def fill_institutionnel(page):
    page.fill_institutionnel_form()


@when('I verify the registration submit button is available')
def verify_submit(page):
    btn = page.get_submit_button()
    assert btn.is_displayed()


@then('the submit button should display "Créer un compte"')
def check_submit_text(page):
    btn = page.get_submit_button()
    assert "un compte" in btn.get_attribute("value")
