from django.views.generic import TemplateView

class IndexView(TemplateView):
    template_name = 'authentication/pages/index.html'