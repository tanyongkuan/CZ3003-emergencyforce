from django.http import JsonResponse
from app.models import Report, GenerateOrder, ActionPlan, Location, Update, Statistics, Force, RecommendForce, DeployForce, OperationOrder, CrisisOutcome, Notification
from rest_framework import permissions, serializers, status
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from django.utils.six import BytesIO
from rest_framework.parsers import JSONParser
from .models import Report
from .models import Fake


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        #fields =('approve,approveDP')
        fields = '__all__'
#
# class FakeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Fake
#         fields = '_all_'


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ('NotificationID', 'Title', 'Description', 'ToWho', 'Read', 'Date_time')


class ActionPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActionPlan
        fields = ('ActionPlanID', 'ActionPlanDescription', 'CrisisID', 'CrisisDescription', 'Date_time', 'Status')


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
         model = Location
         fields = ('LocationID', 'Lat', 'Long', 'AOE', 'Category', 'ActionPlanID')


class ForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Force
        fields = ('ForceType', 'TotalTroops')


class RecommendForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecommendForce
        fields = ('RecommendForceID', 'ForceType', 'ActionPlanID', 'Recommended', 'Max')


class DeployForceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeployForce
        fields = ('DeployForceID', 'ForceType', 'OpsID', 'Utilization')


class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistics
        fields = ('StatisticsID', 'AffectedAOE', 'TotalInjured', 'TotalDeaths', 'TotalDuration', 'UpdateID')


class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ('UpdateID', 'OpsID', 'Date_time', 'Type', 'Description')


class OperationOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = OperationOrder
        fields = ('OpsID', 'ActionPlanID', 'CrisisID', 'Description')


class CrisisOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CrisisOutcome
        fields = ('CrisisID', 'OutcomeDate', 'AffectedRadius', 'TotalDuration', 'CasualtiesCivilian', 'CasualtiesEF', 'CasualtiesEnemy', 'DeathCivilian', 'DeathEF', 'DeathEnemy', 'Description')


class ReceiveOrderSerializer(serializers.Serializer):

    class NotificationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Notification
            fields = ('NotificationID', 'Title', 'Description', 'ToWho', 'Read', 'Date_time')

    class LocationSerializer(serializers.ModelSerializer):
        class Meta:
            model = Location
            fields = ('LocationID', 'Lat', 'Long', 'AOE', 'Category')


    class RecommendForceSerializer(serializers.ModelSerializer):
        class Meta:
            model = RecommendForce
            fields = ('RecommendForceID', 'ForceType', 'Recommended', 'Max')

    Location = serializers.ListField(child=LocationSerializer(), required=False)
    Deployment = serializers.ListField(child=RecommendForceSerializer(), required=False)
    ActionPlanID = serializers.IntegerField()
    ActionPlanDescription = serializers.CharField(max_length=10000)
    CrisisID = serializers.IntegerField()
    CrisisDescription = serializers.CharField(max_length=10000)
    Date_time = serializers.DateTimeField()
    Status = serializers.CharField(max_length=200, default='ACTIVE')

    def create(self, validated_data):
        loc = validated_data.pop('Location')
        dep = validated_data.pop('Deployment')
        plan = ActionPlan.objects.create(**validated_data)
        notify = NotificationSerializer({
            'Title': 'New Action Plan From CMO',
            'Description': 'You have a new action plan',
            'ToWho': 'HQ General'
        })
        json = JSONRenderer().render(notify.data)
        stream = BytesIO(json)
        data = JSONParser().parse(stream)
        Notification.objects.create(**data)
        for d1 in loc:
            Location.objects.create(ActionPlanID=plan, **d1)
        for d2 in dep:
            RecommendForce.objects.create(ActionPlanID=plan, **d2)
        return plan


class CreateUpdateSerializer(serializers.Serializer):

    class StatisticsSerializer(serializers.ModelSerializer):
        class Meta:
            model = Statistics
            fields = ('AffectedAOE', 'TotalInjured', 'TotalDeaths', 'TotalDuration')

    Statistics = serializers.ListField(child=StatisticsSerializer(), required=False)
    OpsID = serializers.IntegerField()
    Date_time = serializers.DateTimeField()
    Type = serializers.CharField(max_length=10000)
    Description = serializers.CharField(max_length=10000)

    def create(self, validated_data):
        sp = validated_data.pop('Statistics')
        update = Update.objects.create(**validated_data)
        for s1 in sp:
            Statistics.objects.create(UpdateID=update, **s1)
        return update