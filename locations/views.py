from django.forms.forms import NON_FIELD_ERRORS
from django.views.generic import FormView


from locations import forms, models
from whereis.geo import find_location, LocationLookupError


class CreateLocation(FormView):
    """
    Allows a user to report their location through the web.
    """

    template_name = "locations/create.html"
    form_class = forms.Location
    success_url = "/add/"

    def form_valid(self, form):
        try:
            location_data = find_location(form.data_as_email)
        except LocationLookupError, e:
            form._errors[NON_FIELD_ERRORS] = form.error_class([e.message])
            return self.form_invalid(form)
        location = models.Location.objects.create(**location_data)
        return self.render_to_response(self.get_context_data(form=form, location=location))
