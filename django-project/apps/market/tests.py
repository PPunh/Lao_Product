from django.contrib.auth import get_user_model
from django.test import TestCase

from apps.news.models import DemandCenterModel
from apps.products.models import ProductsModel

from .models import MarketCategory, MarketUpdate


class MarketModelTests(TestCase):
    def test_market_update_can_reference_product_and_demand_center(self):
        user = get_user_model().objects.create_user(
            username='market-editor',
            email='market@example.com',
            password='password',
        )
        category = MarketCategory.objects.create(name='Agriculture')
        product = ProductsModel.objects.create(name='Organic Rice')
        demand_center = DemandCenterModel.objects.create(
            name='Vientiane Food Center',
            address='Vientiane',
            contact_number='02012345678',
            email='center@example.com',
        )

        update = MarketUpdate.objects.create(
            author=user,
            category=category,
            product=product,
            demand_center=demand_center,
            title='Rice demand is growing',
            summary='Local demand has increased.',
            content='More buyers are looking for locally produced rice.',
            is_published=True,
        )

        self.assertEqual(update.category, category)
        self.assertEqual(product.market_updates.get(), update)
        self.assertEqual(demand_center.market_updates.get(), update)