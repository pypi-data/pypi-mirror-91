=====
kuldeep
=====

Kuldeep is a Django app to conduct Web-based kuldeep. For each question,
visitors can choose between a fixed number of answers.

Detailed documentation is in the "docs" directory.

Quick start
-----------

1. Add "kuldeep" to your INSTALLED_APPS setting like this::

    INSTALLED_APPS = [
        ...
        'rest_framework',
        'kuldeep',

    ]

2. Include the kuldeep URLconf in your project urls.py like this::
    instead from django.urls import path

    use this

    from django.urls import path, include
    from kuldeep.views import HarvestViewSet, BreadViewSet

    router = routers.DefaultRouter()

    router.register(r'harvest', HarvestViewSet),
    router.register(r'bread', BreadViewSet),

    urlpatterns = [
    path('admin/', admin.site.urls), # for admin
    path('', include(router.urls)), # for routers
    ]

3. Run ``python manage.py migrate`` to create the kuldeep models.

4. Start the development server and visit http://127.0.0.1:8000/admin/
   to create a poll (you'll need the Admin app enabled).

5. Visit http://127.0.0.1:8000/harvest or /bread to test postman collection.