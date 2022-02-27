import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import F, Q
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import BookInstance, Whisky, EveningWhisky, Evening, Tasting

paginate_by = 20


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

    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains=FILTER_BOOKS)[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_queryset(self):
        return Whisky.objects.filter[:paginate_by]  # Get x books containing the title war

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class EveningWhiskyListView(generic.ListView):
    model = EveningWhisky


class EveningWhiskyTodayListView(generic.ListView):
    model = EveningWhisky
    template_name = 'catalog/eveningwhisky_today_list.html'

    def get_queryset(self):
        # return Voter.objects.annotate(value=F('vote__value'), year=F('vote__year')).values().filter(
        # name=self.request.user)
        # return EveningWhisky.objects.filter(evening=datetime.date.today())
        return EveningWhisky.objects.filter(evening=datetime.date.today()). \
            annotate(nose=F('tasting__nose'), taste=F('tasting__taste'), user=F('tasting__user__username')).values() \
            # .filter(Q(user=self.request.user) | Q(user=None)) #  liefert nicht die von anderen bereits bewerteten Whiskies


class WhiskyDetailView(generic.DetailView):
    model = Whisky


class EveningWhiskyDetailView(generic.DetailView):
    model = EveningWhisky


class LoanedBooksByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10

    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')


@login_required
@permission_required('catalog.can_mark_returned', raise_exception=True)
def renew_book_librarian(request, pk):
    book_instance = get_object_or_404(BookInstance, pk=pk)

    # If this is a POST request then process the Form data
    if request.method == 'POST':

        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)

        # Check if the form is valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
            book_instance.due_back = form.cleaned_data['renewal_date']
            book_instance.save()

            # redirect to a new URL:
            return HttpResponseRedirect(reverse('index'))  # all-borrowed'))

    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'book_instance': book_instance,
    }

    return render(request, 'catalog/book_renew_librarian.html', context)


class EveningWhiskyCreate(CreateView):
    model = EveningWhisky
    fields = '__all__'
    # initial = {'date_of_death': '11/06/2020'}


class EveningWhiskyUpdate(UpdateView):
    model = EveningWhisky
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class EveningWhiskyDelete(DeleteView):
    model = EveningWhisky
    success_url = reverse_lazy('eveningwhiskies')


class WhiskyCreate(CreateView):
    model = Whisky
    fields = '__all__'


class WhiskyUpdate(UpdateView):
    model = Whisky
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


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
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


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


# class TastingNext(CreateView):
#     model = Tasting
#     fields = '__all__'
#     template_name = 'catalog/tasting_next_form.html'
#
#     def get_queryset(self):
#         return Tasting.objects.filter(self.evening_whisky.evening=today)


class TastingUpdate(UpdateView):
    model = Tasting
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class TastingDelete(DeleteView):
    model = Tasting
    success_url = reverse_lazy('tastings')
