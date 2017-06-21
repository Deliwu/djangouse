import csv
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound
from .models import Qustion, Choice
from django.core.urlresolvers import reverse
from django.template import loader
from django.views.decorators.http import require_http_methods, require_safe
from django.views.decorators.gzip import gzip_page
from django.views.decorators.cache import never_cache
from .forms import ContactForm, AuthorForm, PublisherForm, Publisher


# Create your views here.
def index(request):
    latest_question_list = Qustion.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polla/index.html', context)


@never_cache
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


def export(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/CSV')
    response['Content-Disposition'] = 'attachment; filename"somefilename.csv"'

    writer = csv.writer(response)
    writer.writerow(['First row', 'Foo', 'Bar', 'Baz'])
    writer.writerow(['Second row', 'A', 'B', 'C', '"Testing"', "Here's a quote"])

    return response


def polla_404_handler(request):
    return HttpResponseNotFound("Not found", status=404)


def upload(request):
    if request.method == 'POST':
        upload_file = request.FILES.get('file', None)
        if upload_file is None:
            return HttpResponse('No file get')
        else:
            with open('/tmp/%s' % upload_file.name, 'wb') as f:
                f.write(upload_file.read())
            return HttpResponse('OK')
    else:
        return render(request, 'polla/upload.html')


def send_mail(request):
    if request.method == 'GET':
        form = ContactForm()
        return render(request, 'polla/sendmail.html', {'form': form})
    else:
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            message = form.cleaned_data['message']
            sender = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']

            return HttpResponse('subject: %s message: %s sender: %s cc_myself: %s' % (subject, message, sender, cc_myself))
        else:
            return render(request, 'polla/sendmail.html', {'form': form})


def author_add(request):
    if request.method == 'GET':
        form = AuthorForm()
        return render(request, 'polla/author_add.html', {'form': form})


def publisher_add(request):
    if request.method == 'POST':
        form = PublisherForm(request.POST)
        if form.is_valid():
            publisher = form.save()
            return HttpResponse('Add ok')
    else:
        form = PublisherForm(initial={'name': "O'Reilly", 'city': 'hangzhuo'})

    return render(request, 'polla/publisher_add.html', {'form': form})


def publisher_update(request, publisher_id):
    publisher = get_object_or_404(Publisher, id=publisher_id)

    if request.method == 'GET':
        form = PublisherForm(instance=publisher)
        return render(request, 'polla/publisher_add.html', {'form': form})
    elif request.method == 'POST':
        form = PublisherForm(request.POST, instance=publisher)
        if form.is_valid():
            form.save()
            return HttpResponse('Update success')

    return HttpResponse('Valid')
