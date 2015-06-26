Feature: visualize busline profile.
    To get some info about an especific busline
    As an user
    I want to access its profile

    Scenario: Visualize busline profile
        Given I am on Busine.me homepage
        And I type "205" in the field "busline"
        When I press "Pesquisar"
        And I follow "/perfil_de_linha/0.205/"
        Then I should see "0.205"