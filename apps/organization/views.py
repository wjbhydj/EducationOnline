from django.shortcuts import render
from django.views.generic.base import View
from .models import CityDict, CourseOrg
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.

class OrgView(View):
    def get(self, request):
        all_orgs = CourseOrg.objects.all()
        category = request.GET.get('ct', '')
        if category:
            all_orgs = all_orgs.filter(category=category)

        org_onums = all_orgs.count()
        all_citys = CityDict.objects.all()

        city_id = request.GET.get('city', '')
        if city_id:
            all_orgs = all_orgs.filter(city_id=int(city_id))

        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_orgs, 3, request=request)
        orgs = p.page(page)
        return render(request, 'org-list.html', {
            'all_orgs':orgs,
            'org_onums':org_onums,
            'all_citys':all_citys,
            'city_id':city_id,
            'category':category,
        })