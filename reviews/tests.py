from django.test import TestCase
from reviews.models import Company
from reviews.models import Reviewer
from reviews.models import Review

from django.core.exceptions import ValidationError

class CompanyTestCase(TestCase):
    def setUp(self):
        company = Company.objects.create(name="apple")
        reviewer = Reviewer.objects.create(name="john")

    def test_company_rating_none(self):
        """The company does not have rating"""
        company = Company.objects.get(name="apple")
        self.assertIsNone(company.get_rating())

    def test_company_rating_five(self):
        """The company rating should be five"""
        company = Company.objects.get(name="apple")
        reviewer = Reviewer.objects.get(name="john")
        review = Review.objects.create(rating=5, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer)
        self.assertEqual(company.get_rating(), 5)

    def test_company_rating_five(self):
        """The company rating should be two point five"""
        company = Company.objects.get(name="apple")
        reviewer = Reviewer.objects.get(name="john")
        review = Review.objects.create(rating=5, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer)
        review = Review.objects.create(rating=0, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer)
        self.assertEqual(company.get_rating(), 2.5)

    def test_rating_invalid(self):
        """The rating should be between 0 and 5"""
        company = Company.objects.get(name="apple")
        reviewer = Reviewer.objects.get(name="john")
        review = Review.objects.create(rating=6, title="review", summary="review text", ip="127.0.0.1", company=company, reviewer=reviewer)
        self.assertRaises(ValidationError, review.clean_fields)

    def test_rating_summary_invalid(self):
        """The rating summary should not have more than 10k characters"""
        company = Company.objects.get(name="apple")
        reviewer = Reviewer.objects.get(name="john")
        s = ''.join([str(i) for i in range(10005) if i])
        review = Review.objects.create(rating=5, title="review", summary=s, ip="127.0.0.1", company=company, reviewer=reviewer)
        self.assertRaises(ValidationError, review.clean_fields)
