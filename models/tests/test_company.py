from django.test import SimpleTestCase
from models.company import Company


class TestCompany(SimpleTestCase):

    def create_company(self):
        Company.objects.all().delete()
        company1 = Company()
        company1.name = "pioneira"
        company1.save()

    def test_post_instance(self):
        company = Company()
        self.assertIsNotNone(company)

    def test_unicode(self):
        Company.objects.all().delete()
        company1 = Company()
        company1.name = "pioneira"
        company1.save()
        self.assertEquals(company1.__unicode__(), "pioneira")

    def test_all(self):
        Company.objects.all().delete()
        db_before = Company.all()
        self.create_company()
        db_after = Company.all()
        self.assertTrue(db_before != db_after)

    def test_filter_by_name(self):
        self.create_company()
        companys = Company.filter_by_name("pioneira")
        self.assertEquals(1, len(companys))
