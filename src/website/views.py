from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import PhotoForm
from .models import Photo


class UploadView(CreateView):
    template_name = "website/index.html"
    form_class = PhotoForm
    success_url = "/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        gallery = [
            {
                "file_name": photo.file.name.replace("gallery/", ""),
                "download_url": f'/download/{photo.file.name.replace("gallery/", "")}',
                "delete_url": f"/api/photo/delete/{photo.pk}",
            }
            for photo in Photo.objects.all()
        ]
        context["gallery"] = gallery
        return context

    def post(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        files = request.FILES.getlist("file")

        if "file" not in request.FILES or not form.is_valid():
            return HttpResponseRedirect(reverse_lazy("website:index"))

        if form.is_valid():
            for file in files:
                Photo.objects.create(file=file)
            return HttpResponseRedirect(self.request.path_info)
        else:
            return self.form_invalid(form)


def download(request, file_name: str) -> HttpResponse:
    response = HttpResponse()
    del response["Content-Type"]
    response["X-Accel-Redirect"] = f"/internal/{file_name}"
    response["Content-Disposition"] = f"attachment; filename={file_name}"
    return response
