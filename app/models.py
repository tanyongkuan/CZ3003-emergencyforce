from django.db import models
from channels.binding.websockets import WebsocketBinding
# Create your models here


class Notification(models.Model):
    NotificationID = models.AutoField(primary_key=True)
    Title = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)
    ToWho = models.TextField(null=True, blank=True)
    Read = models.BooleanField(default=False)
    Date_time = models.DateTimeField(auto_now_add=True)


class ActionPlan(models.Model):
    ActionPlanID = models.IntegerField(primary_key=True)
    ActionPlanDescription = models.TextField(null=True, blank=True)
    CrisisID = models.IntegerField()
    CrisisDescription = models.TextField(null=True, blank=True)
    Date_time = models.DateTimeField()
    Status = models.TextField(null=True, blank=True, default="Active")


class Location(models.Model):
    LocationID = models.AutoField(primary_key=True)
    Lat = models.DecimalField(decimal_places=10,max_digits=20)
    Long = models.DecimalField(decimal_places=10,max_digits=20)
    AOE = models.IntegerField()
    Category = models.TextField(null=True, blank=True)
    ActionPlanID = models.ForeignKey(ActionPlan, db_column="ActionPlanID")


class OperationOrder(models.Model):
    OpsID = models.AutoField(primary_key=True)
    ActionPlanID = models.IntegerField()
    CrisisID = models.IntegerField()
    Description = models.TextField(null=True, blank=True)


class Update(models.Model):
    UpdateID = models.AutoField(primary_key=True)
    OpsID = models.IntegerField()
    Date_time = models.DateTimeField()
    Type = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)


class Statistics(models.Model):
    StatisticsID = models.AutoField(primary_key=True)
    AffectedAOE = models.IntegerField()
    TotalInjured = models.IntegerField()
    TotalDeaths = models.IntegerField()
    TotalDuration = models.TextField(null=True, blank=True)
    UpdateID = models.ForeignKey(Update, db_column="UpdateID")


class Force(models.Model):
    ForceType = models.CharField(primary_key=True, max_length=200)
    TotalTroops = models.IntegerField()


class RecommendForce(models.Model):
    class Meta:
        unique_together = (('ForceType', 'ActionPlanID'),)

    RecommendForceID = models.AutoField(primary_key=True)
    ForceType = models.CharField(max_length=200)
    ActionPlanID = models.ForeignKey(ActionPlan, db_column="ActionPlanID")
    Recommended = models.DecimalField(decimal_places=2,max_digits=5)
    Max = models.DecimalField(decimal_places=2,max_digits=5)


class DeployForce(models.Model):
    class Meta:
        unique_together = (('ForceType', 'OpsID'),)

    DeployForceID = models.AutoField(primary_key=True)
    ForceType = models.CharField(max_length=200)
    OpsID = models.ForeignKey(OperationOrder, db_column="OpsID")
    Utilization = models.DecimalField(decimal_places=2,max_digits=5)


class CrisisOutcome(models.Model):
    CrisisID = models.IntegerField(primary_key=True)
    OutcomeDate = models.DateTimeField()
    AffectedRadius = models.IntegerField()
    TotalDuration = models.IntegerField()
    CasualtiesCivilian = models.IntegerField()
    CasualtiesEF = models.IntegerField()
    CasualtiesEnemy = models.IntegerField()
    DeathCivilian = models.IntegerField()
    DeathEF = models.IntegerField()
    DeathEnemy = models.IntegerField()
    Description = models.TextField(null=True, blank=True)


# DK FOR WAD???
class Report(models.Model):
    approve = models.CharField(max_length=250)
    approveDP = models.CharField(max_length=250)


# DK FOR WAD???
class GenerateOrder(models.Model):
    CallerName = models.CharField(max_length=100, default=10)
    Location = models.CharField(max_length=100, default=0)
    Deployment = models.CharField(max_length=100, default=0)
    DeploymentAmount = models.CharField(max_length=100, default=0)
    Date_time = models.CharField(max_length=100, default=0)
    Description = models.CharField(max_length=100, default=0)


# DK FOR WAD???
class Fake(models.Model):
    userId = models.CharField(max_length=250)
    title = models.CharField(max_length=250)
    body = models.CharField(max_length=250)


class ReportBinding(WebsocketBinding):
    model = GenerateOrder
    stream = "intval"
    fields = ["CallerName", "Location", "Deployment", "DeploymentAmount", "Date_time", "Description"]
    # must follow your database name if not it will be undefine. And order do matters

    @classmethod
    def group_names(cls, *args, **kwargs):
        return ["binding.values"]

    def has_permission(self, user, action, pk):
        return True