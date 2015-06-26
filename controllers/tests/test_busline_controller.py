from django.test import SimpleTestCase, Client


STATUS_OK = 200
STATUS_REDIRECT = 302


class BuslineControllerTest (SimpleTestCase):

    def setUp(self):
        self.client = Client()

    def test_search_line(self):
        response = self.client.get("/buscar_linha/?busline=205")
        self.assertEquals(response.status_code, STATUS_OK)

    def test_advanced_search_line_less_than_two(self):
        response = self.client.get(
            "/resultado/busca_avancada/?busline_advanced=0&description=0&terminal__description=0")
        self.assertEquals(response.status_code, STATUS_OK)

    def test_advanced_search_line_two_or_more(self):
        response = self.client.post(
            "/resultado/busca_avancada/?busline_advanced=205&description=leste&terminal__description=gama")
        self.assertEquals(response.status_code, STATUS_OK)

    def test_advanced_search_page(self):
        response = self.client.get("/busca_avancada/")
        self.assertEquals(response.status_code, STATUS_OK)
