import datetime

from django.db import IntegrityError
from django.db.models import Q, FilteredRelation, Avg
from django.forms import modelformset_factory, BaseModelFormSet
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.forms import UserCreationForm
from catalog.models import Whisky, EveningWhisky, Evening, Tasting


def index(request):
    """View function for home page of site."""

    # Generate counts of some main objects
    num_whiskies = Whisky.objects.all().count()
    num_evenings = Evening.objects.all().count()
    num_tastings = Tasting.objects.count()
    # My tastings (user = request.user)
    if request.user.is_authenticated:
        num_my_tastings = Tasting.objects.filter(user=request.user).count()
    else:
        num_my_tastings = 'We give whisky only to our friends :)'

    # The 'all()' is implied by default.
    num_eveningwhiskies = EveningWhisky.objects.count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_whiskies': num_whiskies,
        'num_evenings': num_evenings,
        'num_tastings': num_tastings,
        'num_my_tastings': num_my_tastings,
        'num_eveningwhiskies': num_eveningwhiskies,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class WhiskyListView(generic.ListView):
    model = Whisky
    paginate_by = 20


class EveningWhiskyListView(generic.ListView):
    model = EveningWhisky
    queryset = EveningWhisky.objects.filter(evening=datetime.date.today())


class EveningWhiskyTodayListView(generic.ListView):
    model = EveningWhisky
    template_name = 'catalog/eveningwhisky_today_list.html'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return EveningWhisky.objects.filter(evening=datetime.date.today()). \
                annotate(tasting_user=FilteredRelation('tasting', condition=Q(tasting__user=self.request.user))). \
                values('id', 'whisky_id', 'tasting_user__nose', 'tasting_user__taste', 'tasting')
        else:
            return EveningWhisky.objects.filter(evening=datetime.date.today()).values()


class WhiskyDetailView(generic.DetailView):
    model = Whisky


class EveningWhiskyDetailView(generic.DetailView):
    model = EveningWhisky


class EveningWhiskyCreate(CreateView):
    model = EveningWhisky
    fields = '__all__'
    success_url = reverse_lazy('eveningwhiskies')


class EveningWhiskyUpdate(UpdateView):
    model = EveningWhisky
    fields = '__all__'
    success_url = reverse_lazy('eveningwhiskies')


class EveningWhiskyDelete(DeleteView):
    model = EveningWhisky
    success_url = reverse_lazy('eveningwhiskies')


class WhiskyCreate(CreateView):
    model = Whisky
    fields = '__all__'


class WhiskyUpdate(UpdateView):
    model = Whisky
    fields = '__all__'


class WhiskyDelete(DeleteView):
    model = Whisky
    success_url = reverse_lazy('whiskies')


class EveningListView(generic.ListView):
    model = Evening


class EveningDetailView(generic.DetailView):
    model = Evening


class EveningCreate(CreateView):
    model = Evening
    fields = '__all__'


class EveningUpdate(UpdateView):
    model = Evening
    fields = '__all__'


class EveningDelete(DeleteView):
    model = Evening
    success_url = reverse_lazy('evenings')


class TastingListView(generic.ListView):
    model = Tasting

    def get_report_day(self):
        try:
            report_day = self.kwargs['evening']
        except KeyError:
            report_day = datetime.date.today()
        return report_day

    def get_queryset(self):
        report_day = self.get_report_day()
        queryset = Tasting.objects.filter(evening_whisky__evening=report_day).order_by('evening_whisky__whisky')
        # print(queryset)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_day'] = self.get_report_day()
        return context


class TastingResultListView(generic.ListView):
    model = Tasting

    template_name = 'catalog/tasting_result_list.html'

    def get_report_day(self):
        try:
            report_day = self.kwargs['evening']
        except KeyError:
            report_day = datetime.date.today()
        return report_day

    def get_queryset(self):
        report_day = self.get_report_day()
        # print(report_day)
        queryset = Tasting.objects.filter(evening_whisky__evening=report_day) \
            .values('evening_whisky__whisky_id') \
            .annotate(nose_taste=Avg('nose') + Avg('taste'), color=Avg('color'), smokiness=Avg('smokiness')) \
            .order_by('-nose_taste')
        # .annotate(nose=Avg('nose'), taste=Avg('taste'), color=Avg('color'), smokiness=Avg('smokiness'))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['report_day'] = self.get_report_day()
        return context


class TastingDetailView(generic.DetailView):
    model = Tasting


class TastingCreate(CreateView):
    model = Tasting
    fields = '__all__'


class TastingUpdate(UpdateView):
    model = Tasting
    fields = '__all__'


class TastingDelete(DeleteView):
    model = Tasting
    success_url = reverse_lazy('tastings')


class MySignupView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'catalog/signup.html'


class TastingEveningWhiskyCreate(CreateView):
    model = Tasting
    fields = ['nose', 'taste', 'color', 'smokiness']
    success_url = reverse_lazy('eveningwhiskies-today')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['whisky'] = EveningWhisky.objects.get(id=self.kwargs['eveningwhisky']).whisky_id
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.evening_whisky = EveningWhisky(self.kwargs['eveningwhisky'])
        try:
            return super().form_valid(form)
        except IntegrityError:
            # to do: error handling  Martin: back after create, here we cheat, should update
            return HttpResponseRedirect('/catalog/eveningwhiskies_today')


class TastingValueUpdate(UpdateView):
    model = Tasting
    fields = ['nose', 'taste', 'color', 'smokiness']
    success_url = reverse_lazy('eveningwhiskies-today')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['whisky'] = Tasting.objects.get(id=self.kwargs['pk']).evening_whisky.whisky
        return context


# class BaseTastingFormSet(BaseModelFormSet):
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.queryset = Tasting.objects.filter(evening_whisky__evening=datetime.date.today())


def taste_table(request):
    ExampleFormSet = modelformset_factory(Tasting, exclude=('user',), extra=1)  # , formset=BaseTastingFormSet)
    if request.method == 'POST':
        formset = ExampleFormSet(request.POST)
        for form in formset:
            form.instance.user = request.user
        instances = formset.save()

    def get_queryset():
        if request.user.is_authenticated:
            return EveningWhisky.objects.filter(evening=datetime.date.today()). \
                annotate(tasting_user=FilteredRelation('tasting', condition=Q(tasting__user=request.user))). \
                values('id', 'whisky_id', 'tasting_user__nose', 'tasting_user__taste', 'tasting')
        else:
            return EveningWhisky.objects.filter(evening=datetime.date.today()).values()

    formset = ExampleFormSet(queryset=Tasting.objects.filter(evening_whisky__evening=datetime.date.today()).
                             filter(user=request.user))
    # for form in formset:
    #     print(form)
    return render(request, 'catalog/taste_table.html', {'formset': formset})
