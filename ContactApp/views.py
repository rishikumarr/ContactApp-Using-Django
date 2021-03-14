from django.shortcuts import render,redirect
from .models import Contact
from django.contrib.auth.forms import UserCreationForm
from ContactApp.forms import CreateUserForm
from django.http import HttpResponse
import csv
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from django.contrib.auth.forms import UserChangeForm
from django.views.generic.edit import FormView
from django.contrib.auth import login

class RegisterPage(FormView):
    template_name = 'ContactApp/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super (RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('index')
        return super(RegisterPage, self).get(*args, **kwargs)

class CustomLoginView(LoginView):
    template_name='ContactApp/login.html'
    fields = '__all__'
    redirect_authenticated_user=True

    def get_success_url(self):
        return reverse_lazy('index')

@login_required()
def index(request):
    contacts=Contact.objects.filter(user=request.user)
    search_input=request.GET.get('search-area')
    if search_input:
       contacts=contacts.filter(full_name__icontains=search_input)
    else:
        contacts=contacts.all()
        search_input=''
    return render(request,'ContactApp/index.html', {'contacts':contacts,'search-input':search_input})

    

@login_required()
def viewContact(request,pk):
    contact=Contact.objects.get(id=pk)
    return render(request,'ContactApp/view-contact.html',{'contact':contact})

@login_required()
def editContact(request,pk):
    contact=Contact.objects.get(id=pk)
    if request.method=="POST":
        contact.full_name=request.POST["full_name"]
        contact.phone=request.POST['phone']
        contact.email=request.POST['email']
        contact.address=request.POST['address']
        contact.save()
        return redirect('/')
    return render(request,'ContactApp/edit-contact.html',{'contact':contact})
    
@login_required()
def addContact(request):
    if request.method=="POST":
        request.user.contact_set.create(            
            full_name=request.POST["full_name"],
            phone=request.POST['phone'],
            email=request.POST['email'],
            address=request.POST['address'],)
        return redirect('/')
    return render(request,'ContactApp/add-contact.html')

@login_required()
def deleteContact(request,pk):
    contact=Contact.objects.get(id=pk)
    if request.method=="POST":
        contact.delete()
        return redirect('/')
    return render(request,'ContactApp/delete-contact.html',{'contact':contact})

@login_required
def settings(request):
    return render(request,'ContactApp/settings.html')

@login_required
def export_csv(request):
    response =  HttpResponse(content_type='text/csv')
    response['Content-Disposition']='attachment; filename=Contacts.csv'

    writer = csv.writer(response)
    writer.writerow(['Name','Phone','Email','Address'])

    contacts=Contact.objects.filter(user=request.user)
    for contact in contacts:
        writer.writerow([contact.full_name,contact.phone,contact.email,contact.address])
    return response
