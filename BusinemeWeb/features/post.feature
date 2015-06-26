Feature: Make a post.
	To Make a post
	As an user	
	I want to make a post about a busline using some informations

	Scenario: I fill the field "busline"
	    Given I am on Busine.me homepage
        And I type "205" in the field "busline"
        When I press "Pesquisar"
	    Then I should see "Businar!"

	Scenario: I press the button "Businar!" on "busline_profile.html"
		Given I am on Busine.me homepage
		And I type "205" in the field "busline"
		And I press "Pesquisar"
		And I follow "/perfil_de_linha/0.205/"  
		Then I should see "0.205"      

		