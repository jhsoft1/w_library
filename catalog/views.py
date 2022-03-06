import datetime
from django.db.models import Q, FilteredRelation
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView
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

#
# @login_required
# @permission_required('catalog.can_mark_returned', raise_exception=True)
# def renew_book_librarian(request, pk):
#     book_instance = get_object_or_404(BookInstance, pk=pk)
#
#     # If this is a POST request then process the Form data
#     if request.method == 'POST':
#
#         # Create a form instance and populate it with data from the request (binding):
#         form = RenewBookForm(request.POST)
#
#         # Check if the form is valid:
#         if form.is_valid():
#             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
#             book_instance.due_back = form.cleaned_data['renewal_date']
#             book_instance.save()
#
#             # redirect to a new URL:
#             return HttpResponseRedirect(reverse('index'))  # all-borrowed'))
#
#     # If this is a GET (or any other method) create the default form.
#     else:
#         proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
#         form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})
#
#     context = {
#         'form': form,
#         'book_instance': book_instance,
#     }
#
#     return render(request, 'catalog/book_renew_librarian.html', context)


class EveningWhiskyCreate(CreateView):
    model = EveningWhisky
    fields = '__all__'


class EveningWhiskyUpdate(UpdateView):
    model = EveningWhisky
    fields = '__all__'


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


class TastingEveningWhiskyCreate(CreateView):
    model = Tasting
    fields = ['nose', 'taste']
    success_url = reverse_lazy('eveningwhiskies-today')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.evening_whisky = EveningWhisky(self.kwargs['eveningwhisky'])
        return super().form_valid(form)


class TastingValueUpdate(UpdateView):
    model = Tasting
    fields = ['nose', 'taste']
    success_url = reverse_lazy('eveningwhiskies-today')
