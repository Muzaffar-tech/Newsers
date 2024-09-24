from django.contrib.auth import login, logout
from django.contrib.auth.decorators import permission_required, login_required
from django.core.handlers.wsgi import WSGIRequest
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.contrib import messages


from .models import News, Category, Comment
from .forms import RegisterForm, LoginForm
# Create your views here.

@login_required
def index(request):

    newses = News.objects.filter(is_active=True)
    news_banner = newses.filter(is_banner=True).last()
    news_top_story = newses.order_by("-views").first()
    latest_newses = newses.order_by("-created")[:8]
    latest_news = newses.order_by("-created")[:5]
    categories = Category.objects.all()
    most_views = newses.order_by("-views")[:5]

    context = {
        "news_banner": news_banner,
        "news_top_story":news_top_story,
        "latest_newses" : latest_newses,
        "categories":categories,
        "latest_news" : latest_news,
        "most_views":most_views
    }
    return render(request, "app/index.html", context)

@login_required
@permission_required("app.view_news")
def detail(request, pk):
    news = News.objects.get(pk=pk)
    context = {
        "news": news
    }

    return render(request, "app/detail.html", context)


def register(request: WSGIRequest):
    if request.method == "POST":
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f"Siz ro'yxatdan muvaffarqiyatli o'tdingiz!\n"
                                      f"Login parolni terib saytga kiring!")
            return redirect("login")
        else:
            print(form.error_messages, "**************")
    else:
        form = RegisterForm()
    context = {
        "form":form
    }

    return render(request, "register.html", context)



def user_login(request: WSGIRequest):
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Saytga xush kelibsiz! {user.username}")
            return redirect("home")
    form = LoginForm()
    context={
        "form":form
    }
    return render(request, "login.html", context)

@login_required
def user_logout(request):
    logout(request)
    messages.warning(request, f"Siz saytdan chiqdingiz!")
    return redirect("login")
@login_required
@permission_required('app.change_news', "login", raise_exception=True)
def change_news(request):
    return HttpResponse("O'zgartirish")


def save_comment(request: WSGIRequest, news_id):
    news = News.objects.get(id=news_id)
    Comment.objects.create(
        user=request.user,
        news=news,
        text=request.GET.get("text")

    )
    messages.success(request, "Commentariya saqlandi!!!")
    return HttpResponse("Saqlandi")

