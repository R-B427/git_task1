# mypollapp/views.py
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question


def register(request):
    """
    Handles user registration.

    If the request method is POST, it processes the registration form.
    If the form is valid, it redirects to the 'index' page.
    Otherwise, it renders the 'login.html' template with an error message.

    Returns:
        HttpResponse: The rendered 'login.html' page or a redirect to 'index'.
    """
    if request.method == 'POST':
        # registration logic here
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user = User.objects.create_user(username=username,
                                            password=password)
            user.save()
            login(request, user)
            return redirect('mypollapp:index')  # redirect to poll homepage
        else:
            return render(
                request,
                'authentication/register.html',
                {'error': 'Please provide username and password.'}
            )
    return render(request, 'authentication/register.html')


def authenticate_user(request):
    """
    Handles user authentication.

    If the request method is POST, it processes the login form.
    If the form is valid, it redirects to the 'index' page.
    Otherwise, it renders the 'login.html' template with an error message.

    Returns:
        HttpResponse: The rendered 'login.html' page or a redirect to 'index'.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mypollapp:index')  # redirect to polls after login
        else:
            return redirect('mypollapp:login')  # or return with error message

    return render(request, 'authentication/login.html')


def show_user(request):
    """
    View function to display the current user's information.
    Returns:
        HttpResponse: Renders the 'authentication/user.html'
        template with the user's username and password (if available)
        in the context.
    """
    print(request.user.username)
    # You have a typo: request.user.oassd -> probably password? But user.password is hashed anyway.
    return render(request, 'authentication/user.html', {
        "username": request.user.username,
        # "password": request.user.password  # usually you don't expose password!
    })


@login_required(login_url='/login/')
def index(request):
    """
    View function for displaying the latest 5 published questions.

    Returns:
        HttpResponse: Rendered HTML page displaying
          the list of latest questions.
    """
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'mypollapp/index.html', context)


@login_required(login_url='/login/')
def detail(request, question_id):
    """
    View function for displaying the details of a specific question.

    Returns:
        HttpResponse: The rendered detail page for the specified question.

    Raises:
        Http404: If the Question with the given question_id does not exist.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'mypollapp/detail.html', {'question': question})


@login_required(login_url='/login/')
def vote(request, question_id):
    """
    Handles voting for a specific question.

    Retrieves the Question object by its ID,
    processes the user's selected choice from the POST data,
    increments the vote count for the selected choice,
    and saves the result. If no choice is selected,
    renders the detail page with an error message.
    Upon successful voting, redirects to the results page.

    Returns:
        HttpResponse: Renders the detail page with an error message
          if no choice is selected.
        HttpResponseRedirect: Redirects to the results page
          upon successful voting.
    """
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, question.choice_set.model.DoesNotExist):
        return render(request, 'mypollapp/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(
            reverse('mypollapp:results', args=(question.id,))
        )

@login_required(login_url='/login/')
def results(request, question_id):
    """
    Display the results for a specific poll question.

    Returns:
        HttpResponse: The rendered results page for the specified question.

    Raises:
        Http404: If the Question with the given question_id does not exist.
    """
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'mypollapp/results.html', {'question': question})


def bootstrap_page(request):
    """
    Renders the 'bootstrap.html' template for the mypollapp application.

    Returns:
        HttpResponse: The rendered 'bootstrap.html' page.
    """
    return render(request, 'mypollapp/bootstrap.html')


def user_login(request):
    """
    Handles user login.

    If the request method is POST, it processes the login form.
    If the form is valid, it redirects to the 'index' page.
    Otherwise, it renders the 'login.html' template with an error message.

    Returns:
        HttpResponse: The rendered 'login.html' page or a redirect to 'index'.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('mypollapp:index')
        # Redirect to poll app main page
        else:
            # Show error and stay on login page
            return render(
                request,
                'authentication/login.html',
                {'error': 'Invalid username or password.'}
            )
    else:
        return render(request, 'authentication/login.html')


def landing_page(request):
    """
    Renders the landing page with options to navigate to the login
      or registration forms.
    Returns:
        HttpResponse: The rendered 'authentication/welcome.html' template.
    """

    # This page has buttons to go to login or register forms
    return render(request, 'authentication/welcome.html')


def user_logout(request):
    """
    Logs out the current user and redirects to the landing page.
    Returns:
        HttpResponseRedirect:
        Redirects the user to the landing page after logout.
    """

    logout(request)
    return redirect('mypollapp:landing_page')
 # Redirect to the landing page after logout
