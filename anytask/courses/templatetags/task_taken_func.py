from BeautifulSoup import BeautifulSoup, Comment
from django import template
from django.utils.translation import ugettext as _
from issues.models import Issue


register = template.Library()


@register.filter(name='score')
def task_taken_score(d, task):
    if d.has_key(task.id):
        if isinstance(d[task.id], Issue):
            return d[task.id].score()
        else:
            return d[task.id].score
    return 0


@register.filter(name='comment')
def task_taken_comment(d, task):
    if d.has_key(task.id):
        if isinstance(d[task.id], Issue):
            return d[task.id].last_comment()
        else:
            return d[task.id].teacher_comments
    return ''

@register.filter(name='label_type')
def issue_label_type(d, task):
    if d.has_key(task.id):
        if isinstance(d[task.id], Issue):
            if d[task.id].status == Issue.STATUS_REWORK:
                return 'label-important'
            if d[task.id].status == Issue.STATUS_VERIFICATION:
                return 'label-warning'
            if d[task.id].status == Issue.STATUS_ACCEPTED:
                return 'label-success'
            if d[task.id].status == Issue.STATUS_NEED_INFO:
                return 'label-info'
    return ''
