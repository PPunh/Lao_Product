from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.products.models import ProductsModel

from .models import SupplierProfile, SupplyListing


class SupplyModelTests(TestCase):
    def test_supplier_listing_can_reference_existing_product(self):
        user = get_user_model().objects.create_user(
            username='supplier-owner',
            email='supplier@example.com',
            password='password',
        )
        supplier = SupplierProfile.objects.create(owner=user, business_name='Lao Supply Co')
        product = ProductsModel.objects.create(name='Rice', is_sellable=True)

        listing = SupplyListing.objects.create(
            supplier=supplier,
            product=product,
            title='Wholesale Rice',
            description='Rice for wholesale buyers.',
            status=SupplyListing.Status.PUBLISHED,
        )

        self.assertEqual(listing.supplier.owner, user)
        self.assertEqual(product.supply_listings.get(), listing)