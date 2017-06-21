from django import template


register = template.Library()


@register.filter(name='Lower')  # 注册一个过滤器，名字为Lower
def lower(text):
    return text.lower()


@register.filter
def question_choice_count(question):  # 这里过滤器没有，则函数名就是过滤器的名字
    return question.choices.count()


@register.filter
def question_choice_add(question, num):
    return question.choices.count() + int(num)
