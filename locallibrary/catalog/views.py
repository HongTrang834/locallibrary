from django.shortcuts import render
from .models import Book, Author, BookInstance, Genre
from django.views import generic
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

def index(request):
    # Đây là view cho trang chủ, bạn có thể giữ nguyên hoặc tùy chỉnh
    num_books = Book.objects.all().count()
    num_instances = BookInstance.objects.all().count()
    num_instances_available = BookInstance.objects.filter(status__exact='a').count()
    num_authors = Author.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
    

    context = {
        'num_books': num_books,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_authors': num_authors,
        'num_visits': num_visits,
    }
    return render(request, 'index.html', context=context)

class BookListView(generic.ListView):
    model = Book
    paginate_by = 10
    
    # Ghi đè phương thức để thêm dữ liệu tùy chỉnh vào template
    def get_context_data(self, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context

class BookDetailView(generic.DetailView):
    model = Book
    
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    """Generic class-based view listing books on loan to current user."""
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by = 10
    
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(status__exact='o').order_by('due_back')
class LoanedBooksAllListView(PermissionRequiredMixin, ListView):
    """Generic class-based view listing ALL books on loan. Only viewable by librarians."""

    # 1. Bảo vệ bằng quyền hạn
    permission_required = 'catalog.can_mark_returned'
    # (Nếu không có quyền này, Django sẽ tự động báo lỗi 403 Forbidden)

    # 2. Logic lấy dữ liệu
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_all.html'
    paginate_by = 10

    def get_queryset(self):
        # Lấy TẤT CẢ sách 'On loan', sắp xếp theo ngày hết hạn
        return BookInstance.objects.filter(status__exact='o').order_by('due_back')