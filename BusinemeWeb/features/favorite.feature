Feature: Favorite busline.
    To see my favorite buslines
    As an user
    I would like to favorite my favorite busline
   
   Scenario: I press the button "Favoritar"
        I am on Busine.me loginpage
        And I press "cadastre"
        And I type "name" in the field "name"
        And I type "username@email.com" in the field "email"
        And I type "username" in the field "username"
        And I type "1234" in the field "password"
        And I press "enviar"
        And I type "username" in the field "username"
        And I type "1234" in the field "password"
        And I press "entrar"
        And I type "205" in the field "busline"
        And I press "Pesquisar"
        And I follow "/perfil_de_linha/0.205/"
        And I follow "/fav/0.205/"
        And I should see "Linhas Favoritas"
        When I follow "#busline1"
        Then I should see "Businar!"


   
