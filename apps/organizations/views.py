from django.shortcuts import render
from django.views.generic.base import View
from django.shortcuts import render_to_response
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse

from apps.organizations.models import CourseOrg, City
from apps.organizations.forms import AddAskForm
from MxOnline.settings import MEDIA_URL
# Create your views here.


class AddAskView(View):
    def post(self, request, *args, **kwargs):
        userask_form = AddAskForm(request.POST)
        if userask_form.is_valid():
            userask_form.save(commit=True)
            return JsonResponse(
                {"status":"success"}
            )
        else:
            return JsonResponse(
                {"status": "fail",
                 "msg":"添加出错"}
            )


class OrgView(View):
    def get(self, request, *args, **kwargs):
        all_orgs = CourseOrg.objects.all()
        all_cities = City.objects.all()
        hot_orgs = all_orgs.order_by('-click_nums')[:3]

        # 对课程机构进行筛选
        category = request.GET.get("ct", "")
        if category:
            all_orgs = all_orgs.filter(category=category)

        # 对城市进行筛选
        city_id = request.GET.get("city", "")
        if city_id:
            if city_id.isdigit:
                all_orgs = all_orgs.filter(city_id=int(city_id))

        #对机构进行排序
        sort = request.GET.get("sort", "")
        if sort == "students":
            all_orgs = all_orgs.order_by("-students")
        elif sort == "courses":
            all_orgs = all_orgs.order_by("-course_nums")

        org_nums = all_orgs.count()
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        # Provide Paginator with the request object for complete querystring generation
        # 对课程机构数据进行分页
        p = Paginator(all_orgs, per_page=10, request=request)

        orgs = p.page(page)

        return render(request, "org-list.html",{
            "all_orgs": orgs,
            "org_nums": org_nums,
            "all_cities": all_cities,
            "category": category,
            "city_id": city_id,
            "sort":sort,
            "hot_org": hot_orgs,
        })