from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Album, Photo

class AlbumListView(ListView):
    model = Album
    template_name = 'albums/album_list.html'
    context_object_name = 'albums'

class AlbumDetailView(DetailView):
    model = Album
    template_name = 'albums/album_detail.html'
    context_object_name = 'album'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['photos'] = self.object.photos.all()
        return context

class AlbumCreateView(LoginRequiredMixin, CreateView):
    model = Album
    template_name = 'albums/album_form.html'
    fields = ['title', 'description']
    success_url = reverse_lazy('album_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

class PhotoCreateView(LoginRequiredMixin, CreateView):
    model = Photo
    template_name = 'albums/photo_form.html'
    fields = ['image', 'caption']

    def form_valid(self, form):
        album_id = self.kwargs.get('album_id')
        album = Album.objects.get(id=album_id)
        
        if album.owner != self.request.user:
            from django.core.exceptions import PermissionDenied
            raise PermissionDenied
            
        form.instance.album = album
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.kwargs['album_id']})
    
class AlbumUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Album
    template_name = 'albums/album_form.html'
    fields = ['title', 'description']

    def get_success_url(self):
        return reverse_lazy('album_detail', kwargs={'pk': self.object.pk})

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.owner
    
class AlbumDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Album
    template_name = 'albums/album_confirm_delete.html'
    success_url = reverse_lazy('album_list')

    def test_func(self):
        album = self.get_object()
        return self.request.user == album.owner
    
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')