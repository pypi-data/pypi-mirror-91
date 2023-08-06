from bluedot_rest_framework.utils.models import models, AbstractRelationUser, AbstractRelationTime


class AbstractMaterial(AbstractRelationTime):
    material_type = models.IntegerField()
    category_id = models.IntegerField()
    title = models.CharField(max_length=100)
    banner = models.CharField(max_length=255)
    state = models.IntegerField(default=1)
    is_new = models.IntegerField(default=0)
    data = models.TextField()
    tags_id = models.IntegerField()
    extend = models.JSONField()
    article = models.JSONField()
    recommend = models.JSONField()

    class Meta:
        abstract = True
