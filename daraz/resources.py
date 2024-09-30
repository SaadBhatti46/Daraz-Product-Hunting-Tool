from import_export import resources
from .models import *


class ProductResources(resources.ModelResource):
    class Meta:
        model = Product