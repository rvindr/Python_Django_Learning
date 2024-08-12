from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry
from .models import Products

@registry.register_document
class ProductDocument(Document):
    class Index:
        name = "product" # Name of the Elasticsearch index
        settings = {'number_of_shards': 1,
                    'number_of_replicas': 0}


    class Django:
        model = Products
        fields = [
            'title',
            'image',
            'category',
            'description',
            'sku'
        ]
    