from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views import View
from django.contrib import messages
from django.contrib.auth import logout
from .serializer import ReportSerializer
from app.serializer import NotificationSerializer, ActionPlanSerializer, LocationSerializer, ForceSerializer, RecommendForceSerializer, DeployForceSerializer, StatisticsSerializer, UpdateSerializer, OperationOrderSerializer, CrisisOutcomeSerializer, ReceiveOrderSerializer, CreateUpdateSerializer
#from app.models import Report, GenerateOrder, ActionPlan, Location, Update, Statistics, Force, RecommendForce, DeployForce, OperationOrder, CrisisOutcome, Notification
from app.models import *
from rest_framework import permissions, serializers, viewsets, status
from rest_framework.response import Response
from django.contrib.auth import models
from django.core import serializers


def index(request):
    context = {}
    logged = loader.get_template('app/index.html')
    if (request.user.is_authenticated()):
        return HttpResponse(logged.render(context, request))
    else:
        return HttpResponseRedirect('login/')


def opsorder(request):
    # username = get_object_or_404(get_user_model(), username=username)
    return render(request, 'app/opsorder.html',{
        "integer_values": GenerateOrder.objects.order_by("id"),
})

#After CMO send crisis, fetch from database and display here.
def opsorderdetails(request):
    # username = get_object_or_404(get_user_model(), username=username)
    crisis_id = request.GET['crisis_id']
    return render(request, 'app/opsorderdetail.html',
{       "integer_values": ActionPlan.objects.order_by("ActionPlanID"),
        'crisis_id': int(crisis_id + ''),
        "integer_values2": RecommendForce.objects.order_by("RecommendForceID"),
        "integer_values3": Location.objects.order_by("LocationID"),
        "integer_values4": Force.objects.all(),
})

def receivingOpsOrder(request):
    # username = get_object_or_404(get_user_model(), username=username)
    return render(request, 'app/receivingOpsOrder.html',{
        "integer_values": GenerateOrder.objects.order_by("id"),
})


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('../login/')


def create_report_view(request):
    if request.method == 'POST':
        Title = request.POST['Title']
        Description = request.POST['Description']
        ToWho = request.POST['ToWho']
        report = Notification(
            Title = Title,
            Description = Description,
            ToWho = ToWho,
        )
        report.save()
        messages.success(request, "You have successfully submitted the report [""]")
    return HttpResponse('')


# class ReportViewSet(viewsets.ModelViewSet):
#     lookup_field = 'id'
#     queryset = Report.objects.all()
#     serializer_class = ReportSerializer

def getInbox(request):
    return render(request, 'app/inbox.html', {})

def getLiveFeed(request):
    crisis = ActionPlan.objects.filter(Status='ACTIVE')

    return render(request, 'app/livefeed.html', {'hidden_value': 'YOLO', 'crisis': crisis}) # [{'DeploymentID': 15, 'LocationLat': 1.3521602, 'LocationLong': 103.68414}, {'DeploymentID': 18, 'LocationLat': 1.3533628, 'LocationLong': 103.68184}]})

#InsertOpsOrder
def insertOpsOrder(request):
    if request.method == 'GET':
        crisis_id = request.GET['crisis_id'];
        action_id = request.GET['action_id'];
        description = request.GET['description'];
        SAF = request.GET['SAF'];
        SCDF = request.GET['SCDF'];
        SPF = request.GET['SPF'];
        Cleaner = request.GET['Cleaner'];

        operationOrder = OperationOrder()
        operationOrder.ActionPlanID = action_id
        operationOrder.CrisisID = crisis_id
        operationOrder.Description = description
        operationOrder.save()

        if (SAF):
            deployForce = DeployForce()
            deployForce.ForceType = "SAF"
            deployForce.OpsID = operationOrder
            deployForce.Utilization = SAF
            deployForce.save()
        if (SCDF):
            deployForce = DeployForce()
            deployForce.ForceType = "SCDF"
            deployForce.OpsID = operationOrder
            deployForce.Utilization = SCDF
            deployForce.save()
        if (SPF):
            deployForce = DeployForce()
            deployForce.ForceType = "SPF"
            deployForce.OpsID = operationOrder
            deployForce.Utilization = SAF
            deployForce.save()
        if (Cleaner):
            deployForce = DeployForce()
            deployForce.ForceType = "Cleaners"
            deployForce.OpsID = operationOrder
            deployForce.Utilization = Cleaner
            deployForce.save()

        return JsonResponse("OK", safe=False)


#Notification
def getNotification(request):
   if request.method == 'GET':
       username1 = request.GET['userType'];
       user1 = models.User.objects.filter(username=username1).values('groups')
       userGroup = ''
       if user1[0]["groups"] == 3:
           userGroup = 'Troop'
       if user1[0]["groups"] == 2:
           userGroup = 'HQ Operators'
       if user1[0]["groups"] == 1:
           userGroup = 'HQ General'

       notification = Notification.objects.filter(ToWho=userGroup).order_by("-Date_time")
       data = serializers.serialize('json',notification)

       return JsonResponse(data,safe=False)

def updateNotification(request):
   if request.method == 'GET':
       firstNotify = int(request.GET["firstNotify"])
       secondNotify = int(request.GET["secondNotify"])
       thirdNotify = int(request.GET["thirdNotify"])
       fourthNotify = int(request.GET["fourthNotify"])
       fifthNotify = int(request.GET["fifthNotify"])

       if(firstNotify != 0):
           notify = Notification.objects.get(pk = firstNotify)
           notify.Read = True;
           notify.save()
       if(secondNotify != 0):
           notify = Notification.objects.get(pk = secondNotify)
           notify.Read = True;
           notify.save()
       if(thirdNotify != 0):
           notify = Notification.objects.get(pk = thirdNotify)
           notify.Read = True;
           notify.save()
       if(fourthNotify != 0):
           notify = Notification.objects.get(pk = fourthNotify)
           notify.Read = True;
           notify.save()
       if(fifthNotify != 0):
           notify = Notification.objects.get(pk = fifthNotify)
           notify.Read = True;
           notify.save()

       return JsonResponse("OK",safe=False)
#ENDNotication


def gentella_html(request):
    context = {}
    # The template to be loaded as per gentelella.
    # All resource paths for gentelella end in .html.

    # Pick out the html file name from the url. And load that template.
    load_template = request.path.split('/')[-1]
    if (load_template == 'livefeed.html'):
        return getLiveFeed(request)
    else:
        template = loader.get_template('app/' + load_template)
        if (request.user.is_authenticated()):
            return HttpResponse(template.render(context, request))
        else:
            return HttpResponseRedirect('login/')


class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.all()
    serializer_class = NotificationSerializer


class ActionPlanViewSet(viewsets.ModelViewSet):
    queryset = ActionPlan.objects.all()
    serializer_class = ActionPlanSerializer

    def retrieve(self, request, pk=None):
        qa = ActionPlan.objects.filter(ActionPlanID__exact=pk)
        data = [{
            'ActionPlanID': item.ActionPlanID,
            'Action Plan Description': item.ActionPlanDescription,
            'CrisisID': item.CrisisID,
            'Crisis Description': item.CrisisDescription,
            'Datetime': item.Date_time,
            'Status': item.Status,
            'Location': [{
                'LocationID': li.LocationID,
                'Lat': li.Lat,
                'Long': li.Long,
                'AOE': li.AOE,
                'Category': li.Category
            } for li in Location.objects.filter(ActionPlanID__exact=pk)],
            'Deployment': [{
                'ForceType': ri.ForceType,
                'Recommended': ri.Recommended,
                'MaxUtilization': ri.Max
            } for ri in RecommendForce.objects.filter(ActionPlanID__exact=pk)]
        } for item in qa]
        return JsonResponse(data, safe=False)

    def list(self, request, *args, **kwargs):
        qa = ActionPlan.objects.all()
        data = [{
            'ActionPlanID': item.ActionPlanID,
            'Action Plan Description': item.ActionPlanDescription,
            'CrisisID': item.CrisisID,
            'Crisis Description': item.CrisisDescription,
            'Datetime': item.Date_time,
            'Status': item.Status,
            'Location': [{
                'LocationID': li.LocationID,
                'Lat': li.Lat,
                'Long': li.Long,
                'AOE': li.AOE,
                'Category': li.Category
            } for li in Location.objects.filter(ActionPlanID__exact=item.ActionPlanID)],
            'Deployment': [{
                'ForceType': ri.ForceType,
                'Recommended': ri.Recommended,
                'MaxUtilization': ri.Max
            } for ri in RecommendForce.objects.filter(ActionPlanID__exact=item.ActionPlanID)]
        } for item in qa]
        return JsonResponse(data, safe=False)


class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class ForceViewSet(viewsets.ModelViewSet):
    queryset = Force.objects.all()
    serializer_class = ForceSerializer


class RecommendForceViewSet(viewsets.ModelViewSet):
    queryset = RecommendForce.objects.all()
    serializer_class = RecommendForceSerializer


class DeployForceViewSet(viewsets.ModelViewSet):
    queryset = DeployForce.objects.all()
    serializer_class = DeployForceSerializer


class StatisticsViewSet(viewsets.ModelViewSet):
    queryset = Statistics.objects.all()
    serializer_class = StatisticsSerializer


class UpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = UpdateSerializer
# class UpdateViewSet(viewsets.ModelViewSet):
#     queryset = Update.objects.all()
#     serializer_class = UpdateSerializer
#
#     def retrieve(self, request, pk=None):
#         ua = Update.objects.filter(UpdateID__exact=pk)
#         data = [{
#             'ActionPlanID': item.ActionPlanID,
#             'CrisisID': item.CrisisID,
#             'Description': item.Description,
#             'Datetime': item.Date_time,
#             'Type': item.Type,
#             'Statistics': [{
#                 'AffectedAOE': si.AffectedAOE,
#                 'TotalInjured': si.TotalInjured,
#                 'TotalDeaths': si.TotalDeaths,
#                 'TotalDuration': si.TotalDuration,
#                 'Force': [{
#                     'ForceType': di.ForceType,
#                     'Utilization': di.Utilization
#                 } for di in DeployForce.objects.filter(StatisticsID__exact=si.StatisticsID)]
#             } for si in Statistics.objects.filter(UpdateID__exact=pk)]
#         } for item in ua]
#         return JsonResponse(data, safe=False)
#
#     def list(self, request, *args, **kwargs):
#         ua = Update.objects.all()
#         data = [{
#             'ActionPlanID': item.ActionPlanID,
#             'CrisisID': item.CrisisID,
#             'Description': item.Description,
#             'Datetime': item.Date_time,
#             'Type': item.Type,
#             'Statistics': [{
#                 'AffectedAOE': si.AffectedAOE,
#                 'TotalInjured': si.TotalInjured,
#                 'TotalDeaths': si.TotalDeaths,
#                 'TotalDuration': si.TotalDuration,
#                 'Force': [{
#                     'ForceType': di.ForceType,
#                     'Utilization': di.Utilization
#                 } for di in DeployForce.objects.filter(StatisticsID__exact=si.StatisticsID)]
#             } for si in Statistics.objects.filter(UpdateID__exact=item.UpdateID)]
#         } for item in ua]
#         return JsonResponse(data, safe=False)


class OperationOrderViewSet(viewsets.ModelViewSet):
   queryset = OperationOrder.objects.all()
   serializer_class = OperationOrderSerializer

   def retrieve(self, request, pk=None):
       oo = OperationOrder.objects.filter(OpsID__exact=pk)
       data = [{
           'OpsID': item.OpsID,
           'CrisisID': item.CrisisID,
           'Description': item.Description,
           'ActionPlan': [{
               'ActionPlanID': ap.ActionPlanID,
               'ActionPlanDescription': ap.ActionPlanDescription,
               'CrisisID': ap.CrisisID,
               'CrisisDescription': ap.CrisisDescription,
               'Datetime': ap.Date_time,
               'Status': ap.Status,
               'Location': [{
                   'LocationID': loc.LocationID,
                   'Lat': loc.Lat,
                   'Long': loc.Long,
                   'AOE': loc.AOE,
                   'Category': loc.Category,
               } for loc in Location.objects.filter(ActionPlanID__exact=item.ActionPlanID)]
           } for ap in ActionPlan.objects.filter(ActionPlanID__exact=item.ActionPlanID)],
           'DeployForce': [{
               'ForceType': df.ForceType,
               'Utilization': df.Utilization
           } for df in DeployForce.objects.filter(OpsID__exact=item.OpsID)]
       } for item in oo]
       return JsonResponse(data, safe=False)

   def list(self, request, *args, **kwargs):
       oo = OperationOrder.objects.all().order_by('CrisisID')
       data = [{
           'OpsID': item.OpsID,
           'CrisisID': item.CrisisID,
           'Description': item.Description,
           'ActionPlan': [{
               'ActionPlanID': ap.ActionPlanID,
               'ActionPlanDescription': ap.ActionPlanDescription,
               'CrisisID': ap.CrisisID,
               'CrisisDescription': ap.CrisisDescription,
               'Datetime': ap.Date_time,
               'Status': ap.Status,
               'Location': [{
                   'LocationID': loc.LocationID,
                   'Lat': loc.Lat,
                   'Long': loc.Long,
                   'AOE': loc.AOE,
                   'Category': loc.Category,
               } for loc in Location.objects.filter(ActionPlanID__exact=item.ActionPlanID)]
           } for ap in ActionPlan.objects.filter(ActionPlanID__exact=item.ActionPlanID)],
           'DeployForce': [{
               'ForceType': df.ForceType,
               'Utilization': df.Utilization
           } for df in DeployForce.objects.filter(OpsID__exact=item.OpsID)]
       } for item in oo]
       return JsonResponse(data, safe=False)


class CrisisOutcomeViewSet(viewsets.ModelViewSet):
    queryset = CrisisOutcome.objects.all()
    serializer_class = CrisisOutcomeSerializer


class ReceiveOrderViewSet(viewsets.ModelViewSet):
    queryset = ActionPlan.objects.all()
    serializer_class = ReceiveOrderSerializer


class CreateUpdateViewSet(viewsets.ModelViewSet):
    queryset = Update.objects.all()
    serializer_class = CreateUpdateSerializer