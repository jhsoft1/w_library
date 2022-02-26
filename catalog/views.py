import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views import generic
from django.views.generic import CreateView, UpdateView, DeleteView

from catalog.forms import RenewBookForm
from catalog.models import Book, BookInstance, Author, Genre, Whisky, EveningWhisky, Evening, Tasting

FILTER: str = ''
FILTER_GENRES: str = 'poetry'


def index(request):
    """View function for home page of site."""

    # Generate counts of some main objects
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()

    # Available books (status = 'a')
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()

    # The 'all()' is implied by default.
    num_authors = Author.objects.count()

    num_books_contain = Book.objects.filter(title__icontains=FILTER).count()
    num_genres_contain = Genre.objects.filter(name__icontains=FILTER_GENRES).count()

    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_books_contain': num_books_contain,
        'num_genres_contain': num_genres_contain,
        'FILTER': FILTER,
        'FILTER_GENRES': FILTER_GENRES,
        'num_visits': num_visits,
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


class WhiskyListView(generic.ListView):
    model = Whisky
    paginate_by = 20

    # context_object_name = 'my_book_list'   # your own name for the list as a template variable
    # queryset = Book.objects.filter(title__icontains=FILTER_BOOKS)[:5]  # Get 5 books containing the title war
    # template_name = 'books/my_arbitrary_template_name_list.html'  # Specify your own template name/location
    def get_queryset(self):
        return Whisky.objects.filter(name__icontains=FILTER)[:self.paginate_by]  # Get x books containing the title war

    # def get_context_data(self, **kwargs):
    #     # Call the base implementation first to get the context
    #     context = super(BookListView, self).get_context_data(**kwargs)
    #     # Create any data and add it to the context
    #     context['some_data'] = 'This is just some data'
    #     return context


class EveningWhiskyListView(generic.ListView):
    model = EveningWhisky


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


class TastingUpdate(UpdateView):
    model = Tasting
    fields = '__all__'  # Not recommended (potential security issue if more fields added)


class TastingDelete(DeleteView):
    model = Tasting
    success_url = reverse_lazy('tastings')