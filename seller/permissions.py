from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Seller

class SellerRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return hasattr(self.request.user, 'seller')
