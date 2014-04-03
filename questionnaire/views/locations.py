import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from questionnaire.models import Region, Country, Organization
from braces.views import LoginRequiredMixin


class ListRegions(LoginRequiredMixin, ListView):
    model = Region
    template_name = 'locations/region/index.html'


class ListCountries(LoginRequiredMixin, ListView):
    model = Country
    template_name = 'locations/country/index.html'

    def get(self, request, *args, **kwargs):
        self.region = Region.objects.get(id=self.kwargs['region_id'])
        return super(ListCountries, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.region.countries.all()


class RegionsForOrganization(LoginRequiredMixin, DetailView):
    model = Organization

    def get(self, request, *args, **kwargs):
        json_dump = json.dumps(list(self.get_object().regions.all().values('id', 'name')), cls=DjangoJSONEncoder)
        return HttpResponse(json_dump, mimetype='application/json')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.kwargs['organization_id'])


class CountriesForRegion(LoginRequiredMixin, DetailView):

    def get(self, request, *args, **kwargs):
        regions = Region.objects.filter(id__in=request.GET.getlist('regions'))
        countries = Country.objects.filter(regions__in=regions).values('id', 'name')
        json_dump = json.dumps(list(countries), cls=DjangoJSONEncoder)
        return HttpResponse(json_dump, mimetype='application/json')