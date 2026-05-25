Feature: Registration on Campus France

  Background:
    Given I am on the "Registration" page

  @student
  Scenario: Student profile - submit button is ready
    Given I fill the registration form as a student
    When I verify the registration submit button is available
    Then the submit button should display "Créer un compte"

  @searcher
  Scenario: Searcher profile - submit button is ready
    Given I fill the registration form as a searcher
    When I verify the registration submit button is available
    Then the submit button should display "Créer un compte"

  @institutional
  Scenario: Institutional profile - submit button is ready
    Given I fill the registration form as an institutional user
    When I verify the registration submit button is available
    Then the submit button should display "Créer un compte"
