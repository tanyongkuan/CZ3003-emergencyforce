from django.conf.urls import url ,include
from app import views
from rest_framework import routers
# router = routers.SimpleRouter()
# from app.views import ReportViewSet
# router.register(r'id', ReportViewSet)
from django.contrib.auth.views import logout

router = routers.DefaultRouter()
router.register(r'api/notification', views.NotificationViewSet)
router.register(r'api/order', views.ReceiveOrderViewSet)
router.register(r'api/actionPlan', views.ActionPlanViewSet)
router.register(r'api/location', views.LocationViewSet)
router.register(r'api/update', views.UpdateViewSet)
router.register(r'api/createUpdate', views.CreateUpdateViewSet)
router.register(r'api/statistics', views.StatisticsViewSet)
router.register(r'api/force', views.ForceViewSet)
router.register(r'api/recommendForce', views.RecommendForceViewSet)
router.register(r'api/deployForce', views.DeployForceViewSet)
router.register(r'api/operationOrder', views.OperationOrderViewSet)
router.register(r'api/crisisOutcome', views.CrisisOutcomeViewSet)

urlpatterns = [
    # Matches any html file - to be used for gentella
    # Avoid using your .html in your resources.
    # Or create a separate django app.
    url(r'^', include(router.urls)),
    # url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^.*\.html', views.gentella_html, name='gentella'),
    #url(r'^api/v1/',include(routers.urls)),
    url(r'livefeed|livefeed.html', views.getLiveFeed),
    url(r'^opsorder/', views.opsorder),

    # From view inbox -> view whole opsorder -> send
    url(r'^inbox.html|inbox',views.getInbox),
    url(r'^opsorderdetails', views.opsorderdetails, name = 'opsorderdetails'),
    url(r'^generateoporderAPI/$', views.create_report_view, name='operator'),
    #Notification
    url(r'^getNotification/', views.getNotification),
    url(r'^updateNotification/', views.updateNotification),
    url(r'^addOpsOrder/', views.insertOpsOrder),

    # The home page
    url(r'^$', views.index, name='index'),
    url(r'^loggout/$', views.logout_view),
]