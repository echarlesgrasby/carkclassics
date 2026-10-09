from django.urls import path
from frontmatter import views

app_name = "seminar"

urlpatterns = [
    path("", views.LandingView.as_view(), name="landing"),
    path("readings/", views.TextListView.as_view(), name="texts"),
    path("minutes/", views.SessionListView.as_view(), name="sessions"),
    path("minutes/<slug:cycle_slug>/<int:number>/", views.session_detail, name="session_detail"),
]
# In the project urls.py: path("seminar/", include("seminar.urls")),
# In development also add: + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
