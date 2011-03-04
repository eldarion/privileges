from django.db import models


class Privilege(models.Model):
    
    label = models.CharField(max_length=75, db_index=True)
    verbose_name = models.CharField(max_length=255)
    description = models.TextField()
    
    def __unicode__(self):
        return self.verbose_name
