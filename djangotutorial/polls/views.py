#WEB
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import get_object_or_404, render

#LOGIN NEEDED TO ACCESS POLLS
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, DeleteView
from django.contrib.auth.decorators import login_required, user_passes_test

#ONLY ADMINS CAN ACCESS
from .decorators import admin_required
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.admin.views.decorators import staff_member_required

#AUTHENTICATION
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages

#CANDIDATE
from .models import Candidate

#MISC
from django.utils import timezone
from django.urls import reverse
from django.db.models import F
from django.views import generic
from django.shortcuts import render
from .models import Choice, Question

def is_admin(user):
    return user.is_staff

def main_page(request):
    candidates = Candidate.objects.all()
    return render(request, 'candidates/main_page.html', {'candidates': candidates})

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

@staff_member_required
def admin_view(request):
    context = {
        'title': "Admin View",
        'message': "frfr",
    }
    render(request, 'admin/admin_view.html', context)

@login_required
def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/results.html', {'question': question})

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)

def index(request):
    latest_question_list = Question.objects.order_by("-pub_date")[:5]
    output = ", ".join([q.question_text for q in latest_question_list])
    return HttpResponse(output)

@login_required
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

@login_required
def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'polls/detail.html', {'question': question})

@login_required
def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        # Check if the user has already voted for any choice in this question
        for choice in question.choice_set.all():
            if request.user in choice.voters.all():
                return render(request, 'polls/detail.html', {
                    'question': question,
                    'error_message': "You have already voted for this question.",
                })
        selected_choice.votes += 1
        selected_choice.voters.add(request.user)
        selected_choice.save()
        return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

@login_required
@user_passes_test(is_admin)
def reset_voters(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    for choice in question.choice_set.all():
        choice.voters.clear()
        choice.votes = 0
        choice.save()
    return redirect('polls:results', question_id=question.id)

def get_queryset(self):
    return Question.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:5]

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('polls:index')
        else:
            messages.error(request, 'Invalid username or password')
    return render(request, 'polls/login.html')

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                login(request, user)
                return redirect('polls:index')
        else:
            messages.error(request, 'Passwords do not match')
    return render(request, 'polls/register.html')

class AdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_staff

class IndexView(LoginRequiredMixin, ListView):
    model = Question
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.order_by("-pub_date")[:5]

class DetailView(LoginRequiredMixin, DetailView):
    model = Question
    template_name = "polls/detail.html"
    context_object_name = "latest_question_list"
    
    def get_queryset(self):
        return Question.objects.filter(pub_date__lte=timezone.now())

class ResultsView(LoginRequiredMixin, DeleteView):
    model = Question
    template_name = "polls/results.html"