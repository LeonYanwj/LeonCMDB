from django.contrib import admin
from salt_restapi import models
# Register your models here.

admin.site.register(models.AgentDeployHostMess)
admin.site.register(models.SaltConfigEnv)
