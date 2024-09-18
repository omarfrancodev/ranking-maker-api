from django.urls import path, include
from rest_framework.routers import DefaultRouter
from users.views import PersonViewSet
from categories.views import CategoryViewSet, SubcategoryViewSet
from content.views import ContentViewSet
from viewings.views import ViewingViewSet
from rankings.views import RankingHeaderViewSet
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="API Documentation",
        default_version='v1',
        description="API for Ranking Maker",
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter()
router.register(r'persons', PersonViewSet)
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubcategoryViewSet)
router.register(r'contents', ContentViewSet)
router.register(r'viewings', ViewingViewSet)
router.register(r'rankings', RankingHeaderViewSet)


url_api = 'api/'

urlpatterns = [
    path(url_api, include(router.urls)),
    path('swagger/', schema_view.with_ui('swagger',
         cache_timeout=0), name='schema-swagger-ui'),
]
