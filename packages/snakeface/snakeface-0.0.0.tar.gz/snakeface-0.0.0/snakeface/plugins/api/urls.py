from django.urls import path
from django.conf.urls import include, url
import rest_framework.authtoken.views as authviews

from rest_framework import routers
import yeastphenome.apps.api.urls.serializers as views

router = routers.DefaultRouter()
router.register(r"^papers", views.PaperViewSet, basename="paper")

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


# Documentation URL
schema_view = get_schema_view(
    openapi.Info(
        title="YeastPhenome API",
        default_version="v1",
        description="Programmatic functions for YeastPhenome.org",
        #      terms_of_service="https://www.google.com/policies/terms/",
        license=openapi.License(name="Apache License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAnyGet,),
)


urlpatterns = [
    path("", include(router.urls)),
    path("papers/<int:paper_id>/references", views.GetPaperReferences.as_view()),
    path("genes/", views.GetGenes.as_view(), name="get_genes"),
    path("genes/<str:systematic_name>/similar", views.GetSimilarGenes.as_view()),
    path(
        "observable/<int:observable_id>/datasets",
        views.GetObservableDatasets.as_view(),
        name="observable_datasets",
    ),
    path(
        "genes/datasets/<str:systematic_name>/",
        views.GetGeneDatasets.as_view(),
        name="gene_datasets",
    ),
    path(
        "genes/<str:systematic_name>/<int:N>/similar", views.GetSimilarGenes.as_view()
    ),
    path(
        "genes/<str:systematic_name>/<int:N>/similar/<int:reverse>",
        views.GetSimilarGenes.as_view(),
    ),
    path(
        "search/datasets/explore",
        views.DatasetsSearch.as_view(),
        name="datasets_search",
    ),
    path(
        "search/conditions/explorr",
        views.ConditionsSearch.as_view(),
        name="conditions_search",
    ),
    path("search/papers/explore", views.PapersSearch.as_view(), name="papers_search"),
    path(
        "search/phenotypes/explore",
        views.PhenotypesSearch.as_view(),
        name="phenotypes_search",
    ),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    path("api-token-auth/", authviews.obtain_auth_token),
    url(r"^schema/$", schema_view, name="api-schema"),
    url(
        r"^swagger(?P<format>\.json|\.yaml)$",
        schema_view.without_ui(cache_timeout=0),
        name="schema-json",
    ),
    url(
        r"^swagger/$",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    url(r"^docs/$", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

app_name = "api"
