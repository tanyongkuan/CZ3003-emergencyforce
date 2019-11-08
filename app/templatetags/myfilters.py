from django import template

register = template.Library()

@register.filter(name='is_Gen')
def is_Gen(user):
    return user.groups.filter(name='HQ General').exists()

@register.filter(name='is_Troop')
def is_Troop(user):
   return user.groups.filter(name='Troop').exists()

@register.filter(name="getQuery")
def getQuery(request):
    return int(request.GET.get('crisis_id'))


@register.filter(name="getActID")
def getActID(request):
    return int(request.GET.get('act_id'))

@register.filter(name="getOpsID")
def getOpsID(request):
    return int(request.GET.get('ops_id'))

@register.filter(name='getSAF')
def getSAF(request):
   return int(request.GET.get('saf'))

@register.filter(name="getSCDF")
def getSCDF(request):
    return int(request.GET.get('scdf'))


@register.filter(name="getSPF")
def getSPF(request):
    return int(request.GET.get('spf'))

@register.filter(name="getCleaner")
def getCleaner(request):
    return int(request.GET.get('cleaner'))