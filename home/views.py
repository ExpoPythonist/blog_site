from django.shortcuts import render, redirect
from django.contrib.auth import logout

from home.form import BlogForm
from home.models import BlogModel, Profile


def logout_view(request):
    logout(request)
    return redirect('/')


def home(request):
    context = {'blogs': BlogModel.objects.all()}
    return render(request, 'home.html', context)


def login_view(request):
    return render(request, 'login.html')


def blog_detail(request, slug):
    context = {}
    try:
        blog_obj = BlogModel.objects.filter(slug=slug).first()
        context['blog_obj'] = blog_obj
    except Exception as e:
        raise Exception(str(e))
    return render(request, 'blog_detail.html', context)


def see_blog(request):
    context = {}
    try:
        blog_objs = BlogModel.objects.filter(user=request.user)
        context['blog_objs'] = blog_objs
    except Exception as e:
        raise Exception(str(e))
    return render(request, 'see_blog.html', context)


def add_blog(request):
    context = {'form': BlogForm}
    try:
        if request.method == 'POST':
            form = BlogForm(request.POST)
            image = request.FILES.get('image', '')
            title = request.POST.get('title')
            user = request.user

            if form.is_valid():
                content = form.cleaned_data['content']

            blog_obj = BlogModel.objects.create(
                user=user, title=title,
                content=content, image=image
            )
            return redirect('/add-blog/')
    except Exception as e:
        raise Exception(str(e))
    return render(request, 'add_blog.html', context)


# def blog_update(request, slug):
#     try:
#
#         blog_obj = BlogModel.objects.get(slug=slug)
#         if blog_obj.user != request.user:
#             return redirect('/')
#         blog_data = {"title": blog_obj.title, "content": blog_obj.content}
#         context = blog_data
#
#         if request.method == 'POST':
#             title = request.POST.get('title', blog_obj.title)
#             content = request.POST.get('content', blog_obj.content)
#             user = request.user
#
#             blog_obj = BlogModel.objects.update(
#                 user=user, title=title,
#                 content=content
#             )
#             context = {"title": blog_obj.title, "content": blog_obj.content}
#
#     except Exception as e:
#         raise Exception(str(e))
#     return render(request, 'update_blog.html', context)


def blog_delete(request, id):
    try:
        blog_obj = BlogModel.objects.get(id=id)
        if blog_obj.user == request.user:
            blog_obj.delete()
    except Exception as e:
        raise Exception(str(e))
    return redirect('/see-blog/')


def register_view(request):
    return render(request, 'register.html')


def verify(request, token):
    try:
        profile_obj = Profile.objects.filter(token=token).first()

        if profile_obj:
            profile_obj.is_verified = True
            profile_obj.save()
        return redirect('/login/')

    except Exception as e:
        raise Exception(str(e))
    return redirect('/')