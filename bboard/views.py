from django.urls import reverse_lazy
from django.shortcuts import render
from django.views.generic.edit import CreateView

from .forms import BbForm

from .models import Bb, Group

class BbCreateView(CreateView):
    template_name = 'bboard/create.html'
    form_class = BbForm
    success_url = reverse_lazy('index')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context


def index(request):
    bbs = Bb.objects.all()
    groups = Group.objects.all()
    context = {'bbs': bbs, 'groups': groups}
    return render(request, 'bboard/index.html', context)

def by_group(requset, group_id):
    bbs = Bb.objects.filter(group=group_id)
    groups = Group.objects.all()
    current_group = Group.objects.get(pk=group_id)
    context = {'bbs': bbs, 'groups': groups, 'current_group': current_group}
    return render(requset, 'bboard/by_group.html', context)


