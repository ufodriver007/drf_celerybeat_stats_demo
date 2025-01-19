from django.db import models


class ParserCall(models.Model):
    phrase_region_id = models.CharField(max_length=200, verbose_name='pr_id')
    phrase = models.CharField(max_length=200, verbose_name='phrase')
    region = models.CharField(max_length=200, verbose_name='region')
    number_of_ads = models.PositiveIntegerField(default=None, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phrase_region_id

    class Meta:
        verbose_name = 'ParserCall'
        verbose_name_plural = 'ParserCalls'
