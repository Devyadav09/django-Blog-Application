from django.shortcuts import render, redirect ,HttpResponse ,HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from .forms import singupform , postform
from django.contrib.auth import authenticate, login ,logout
from.models import BlogModel , Comment
from django.http import JsonResponse 
from django.views.generic import UpdateView
from django.urls import reverse_lazy





def home(request):
    if request.method == 'POST':
        fm = singupform(request.POST)
        if fm.is_valid():
            fm.save()
            return HttpResponseRedirect('/login/')
    else:
        fm = singupform() 
    return render(request, 'home/home.html', {'form': fm}) 

def user_login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect("/menupage/")
    if request.method == 'POST':
        fm = AuthenticationForm(request, data=request.POST)
        if fm.is_valid():
            uname = fm.cleaned_data['username']
            upass = fm.cleaned_data['password']
            user = authenticate(username=uname, password=upass)
            
            if user==None:
                pass
            else:
                login(request,user) 
                return HttpResponseRedirect("/menupage/")       
    else:
        fm = AuthenticationForm()
    return render(request, 'home/login.html', {'form': fm})




def menu(request):
    if request.user.is_authenticated:
        # Retrieve blogs ordered by created_at field in descending order
        blogs = BlogModel.objects.order_by('-created_at')
        context = {'blogs': blogs}
        return render(request, 'home/menu.html', context)
    else:
        return HttpResponseRedirect("/login/")
    
def user_logout(request):
    logout(request)
    return HttpResponseRedirect("/login/")



def addpost(request):
    context = {'form': postform}
    try:
        if request.method == 'POST':
            form = postform(request.POST,request.FILES)
            
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                print('Valid')
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                userid=request.user , title=title,
                content=content, image=image
            )
            print(blog_obj)
            return redirect('/menupage/')
    except Exception as e:
        print(e)

    return render(request, 'home/addpost.html', context)        
            
            
            
            
            
def upload_image(request):
    if request.method == 'POST' and request.FILES.get('file'):
        image = request.FILES['file']
        # Save the image to your media directory
        # You may need to handle renaming and unique filenames
        image_path = 'blog/' + image.name
        with open(image_path, 'wb+') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        # Return the URL of the saved image
        return JsonResponse({'link': image_path})
    return JsonResponse({'error': 'Invalid request'})



def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
        comments = Comment.objects.filter(blog=blog_obj)  # Retrieve comments related to the blog
        context['comments'] = comments

        if request.method == 'POST':
            comment_content = request.POST.get('content')
            user = request.user if request.user.is_authenticated else None
            if comment_content and user:  # Ensure comment content and user are present
                comment = Comment.objects.create(
                    content=comment_content,
                    user=user,
                    blog=blog_obj
                )
               
            else:
                # Handle the case when either comment content or user is missing
                # You may want to display an error message or handle it differently
                pass
    except Exception as e:
        print(e)
    return render(request, 'home/blog_detail.html', context)
  
  
def mypost(request):
    if request.user.is_authenticated:
        posts=BlogModel.objects.filter(userid=request.user)
        return render(request,'home/mypost.html',{'posts':posts})
    else:
        return HttpResponseRedirect('/menupage/')
    
    

def deletepost(request,slug):
    if request.user.is_authenticated:
        posts=BlogModel.objects.filter(slug=slug)
        posts.delete()
        return HttpResponseRedirect('/mypost/')
    else:
        return HttpResponseRedirect('/menupage/')
     
    
    
    
class UpdatePostView(UpdateView):
    model = BlogModel
    template_name = 'edit_blog_post.html'
    fields = ['title', 'content', 'image']
    slug_field = 'slug'  # Specify the slug field in your BlogModel
    slug_url_kwarg = 'slug'
    
    def get_success_url(self):
        # Assuming 'mypost' is the name of the URL pattern for mypost.html
        return reverse_lazy('mypost')
    
    
    
    
def search(request):
    if request.method == "POST":
        searched = request.POST['searched']
        blogs = BlogModel.objects.filter(title__contains=searched)
        return render(request, "search.html", {'searched':searched, 'blogs':blogs})
    else:
        return render(request, "search.html", {})