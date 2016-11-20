from django.test import TestCase
from django.core.cache import cache
from reviews.models import Company
from reviews.models import Reviewer
from reviews.models import Review
from oauth.models import Client

from django.core.exceptions import ValidationError

class CompanyTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name="test_apple_test")
        cache.set("rating_%s_test_apple_test" % str(company.pk), None)
        client = Client.objects.create(username='test', password='password', token='token')
        reviewer = Reviewer.objects.create(name="john",client=client)

    def test_company_rating_none(self):
        """The company does not have rating"""
        company = Company.objects.get(name="test_apple_test")
        self.assertIsNone(company.get_rating())

    def test_company_rating_five(self):
        """The company rating should be five"""
        company = Company.objects.get(name="test_apple_test")
        reviewer = Reviewer.objects.get(name="john")
        client = Client.objects.get(username='test')
        review = Review.objects.create(rating=5, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer, client=client)
        company.update_average_rating()
        self.assertEqual(company.get_rating(), 5)

    def test_company_rating_five(self):
        """The company rating should be two point five"""
        company = Company.objects.get(name="test_apple_test")
        reviewer = Reviewer.objects.get(name="john")
        client = Client.objects.get(username='test')
        review = Review.objects.create(rating=5, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer, client=client)
        review = Review.objects.create(rating=0, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer, client=client)
        company.update_average_rating()
        self.assertEqual(company.get_rating(), 2.5)

    def test_rating_invalid(self):
        """The rating should be between 0 and 5"""
        company = Company.objects.get(name="test_apple_test")
        reviewer = Reviewer.objects.get(name="john")
        client = Client.objects.get(username='test')
        review = Review.objects.create(rating=6, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer, client=client)
        company.update_average_rating()
        self.assertRaises(ValidationError, review.clean_fields)

    def test_rating_summary_invalid(self):
        """The rating summary should not have more than 10k characters"""
        company = Company.objects.get(name="test_apple_test")
        reviewer = Reviewer.objects.get(name="john")
        client = Client.objects.get(username='test')
        s = ''.join([str(i) for i in range(10005) if i])
        review = Review.objects.create(rating=5, title="review", summary=s, ip="127.0.0.1", company=company, reviewer=reviewer, client=client)
        company.update_average_rating()
        self.assertRaises(ValidationError, review.clean_fields)
