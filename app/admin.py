from django.contrib import admin
from .models import Notification
from .models import ActionPlan
from .models import Location
from .models import Update
from .models import Statistics
from .models import Force
from .models import RecommendForce
from .models import DeployForce
from .models import OperationOrder
from .models import CrisisOutcome
from .models import Report
from .models import Fake
from .models import GenerateOrder
# Register your models here.

admin.site.register(Notification)
admin.site.register(ActionPlan)
admin.site.register(Location)
admin.site.register(Update)
admin.site.register(Statistics)
admin.site.register(Force)
admin.site.register(RecommendForce)
admin.site.register(DeployForce)
admin.site.register(OperationOrder)
admin.site.register(CrisisOutcome)
admin.site.register(Report)
admin.site.register(
    GenerateOrder,
    list_display=["CallerName", "Location", "Deployment","DeploymentAmount","Date_time","Description"],
)
admin.site.register(Fake)