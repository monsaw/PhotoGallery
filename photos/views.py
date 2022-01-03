from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from photos.models import Category, Photo
from django.contrib.auth import login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import FormView
from django.contrib.auth.decorators import login_required
# Create your views here.
class CustomisedLogin(LoginView):
    template_name = 'photos/login.html'
    fields = '__all__'
    redirect_authenticated_user =True

    def get_success_url(self):
        return reverse_lazy('gallery')

class RegisterPage(FormView):
    template_name = 'photos/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('gallery')

    def form_valid(self,form):
        user = form.save()
        if user is not None:
            login(self.request,user)
        return super(RegisterPage , self).form_valid(form)

@login_required
def gallery(request):
    category = request.GET.get('category')
    if category == None :
        photos = Photo.objects.all()
    else:
        photos = Photo.objects.filter(category__name = category)

    categories = Category.objects.all()
    
    context = {'categories' : categories , 'photos':photos}
    return render(request, 'photos/gallery.html', context)


@login_required
def addPhoto(request):
    categories = Category.objects.all()
    context = {'categories' : categories}
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get("image")

        if data['category'] != 'none':
            category = Category.objects.get(id= data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name = data['category_new']) 
        else:
            category = None

        photo = Photo.objects.create(
            category = category,
            photo = image,
            description = data['description']
        )
        return redirect('gallery')

    return render(request, 'photos/add.html',context)

@login_required
def viewPhoto(request, pk):
    photo = Photo.objects.get(id = pk)
    return render(request, 'photos/photo.html', {'photo':photo})

