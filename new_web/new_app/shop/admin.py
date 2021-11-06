from django.contrib import admin

from .models import Product,Orders,OrderUpdate,ProductComment,Contact

admin.site.register(Product)
admin.site.register(Contact)
admin.site.register(Orders)
admin.site.register(OrderUpdate)
admin.site.register(ProductComment)

