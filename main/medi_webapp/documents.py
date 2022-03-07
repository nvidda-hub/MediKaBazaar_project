from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from medi_webapp.models import Product


@registry.register_document
class ProductDocument(Document):
    class Index:
        name = "product_search"
    
    class Django:
        model = Product

        fields = [
            "id",
            "product_name",
            "quantity",
            "price"
        ]