# Url
# from django.contrib import admin
from django.urls import path, include
# from drf_yasg.views import get_schema_view
# from drf_yasg import openapi

# schema_view = get_schema_view(
#     openapi.Info(
#         title="Your API",
#         default_version='v1',
#         description="API description",
#     ),
#     public=True,
# )

urlpatterns = [
    # path('api/', admin.site.urls), # si je met ça je suis toujorus redirigé vers le login
    path('api/', include('project.urls')),
    path('api/', include('issue.urls')),
    path('api/', include('contributor.urls')),
    path('api/', include('authentification.urls')),
    path('api/', include('comment.urls')),
    path('api/', include('user.urls')),
    # re_path(r'^swagger/$', schema_view.with_ui('swagger',
    #                                            cache_timeout=0), name='schema-swagger-ui'),
]
