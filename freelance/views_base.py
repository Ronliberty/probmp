

from django.http import HttpResponseForbidden
from django.template.loader import render_to_string
from django.views import View

class HTMXOnlyView(View):
    def render_to_response(self, context, **response_kwargs):
        if not self.request.headers.get('HX-Request'):
            return HttpResponseForbidden(
                render_to_string(
                    'custom_account/errors/htmx_only.html',
                    context,
                    request=self.request
                )
            )
        return super().render_to_response(context, **response_kwargs)
