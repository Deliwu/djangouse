from django.shortcuts import render
from django.http import HttpResponse
from .models import Qustion
from django.template import loader


# Create your views here.
def index(request):
    latest_question_list = Qustion.objects.order_by('-pub_date')[:5]
    template = loader.get_template('polla/index.html')
    context = {'latest_question_list': latest_question_list}
    return HttpResponse(template.render(context))


def detail(request, question_id):
    return HttpResponse('Your are looking at question {}'.format(question_id))


def results(request, question_id):
    response = "You are looking at results of question {}".format(question_id)
    return HttpResponse(response)


def vote(request, question_id):
    return HttpResponse("Your are voting on question {}".format(question_id))
