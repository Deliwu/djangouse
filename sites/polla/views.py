from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from .models import Qustion, Choice
from django.core.urlresolvers import reverse
from django.template import loader


# Create your views here.
def index(request):
    latest_question_list = Qustion.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polla/index.html', context)


def detail(request, question_id):
    question = get_object_or_404(Qustion, id=question_id)
    print(request.GET)
    return render(request, 'polla/detail.html', {'question': question})


def results(request, question_id):
    question = get_object_or_404(Qustion, pk=question_id)
    return render(request, 'polla/results.html', {'question': question})


def vote(request, question_id):
    question = get_object_or_404(Qustion, pk=question_id)
    if request.method == 'POST':
        print(request.POST)
        choice_id = request.POST.getlist('choice', 0)
        print(choice_id)
        choice_id = choice_id[0]
        try:
            selected_choice = question.choices.get(pk=choice_id)
        except Choice.DoesNotExist:
            # Redisplay the question voting form.
            return render(request, 'polla/detail.html', {'question': question, 'error_message': "You didn't select a choice.",})
        else:
            selected_choice.votes += 1
            selected_choice.save()
            return HttpResponseRedirect(reverse('polla:results', args=(question.id,)))
    else:
        return HttpResponse('Your post question_id: %s' % question.id)
