from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView


api_v1_urlpatterns = [
    # Schema
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

    # Account
    path('account/', include('account.urls', namespace='account')),
    # Pages
#    path('pages/', include('pages.urls', namespace='pages')),
    # Blog
    path('blog/', include('blog.urls', namespace='blog')),
    # Faqs
    path('faqs/', include('questions.urls', namespace='faqs')),
    # Rules
    path('rules/', include('rules.urls', namespace='rules')),
    # Contact Us
    path('contact-us/', include('contact_us.urls', namespace='contact_us')),
    # Project
    path('project/', include('project.urls', namespace='project')),
    # Contractor
    path('contractor/', include('contractor.urls', namespace='contractor')),
]

urlpatterns = [
    # Third party
    path('ckeditor/', include('ckeditor_uploader.urls')),
    # API
    path('api/v1/', include(api_v1_urlpatterns)),
#    path("bankgateways/", az_bank_gateways_urls()),
    # Admin
    path('admin/', admin.site.urls),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
