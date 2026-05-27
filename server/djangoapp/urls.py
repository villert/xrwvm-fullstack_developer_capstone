# Uncomment the imports before you add the code
# from django.urls import path
from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'djangoapp'
urlpatterns = [
    # path for login and logout
    path(route='login', view=views.login_user, name='login'),
    path(route='logout', view=views.logout_user, name='logout'),
    path(route='register', view=views.registration, name='register'),

    # dealer and review endpoints
    path(route='get-dealers', view=views.get_dealerships, name='get_dealers'),
    path(route='get-dealer/<int:dealer_id>/', view=views.get_dealer_details, name='get_dealer'),
    path(route='get-dealers-by-state/<str:state>/', view=views.get_dealers_by_state, name='dealers_by_state'),
    path(route='get-dealer-reviews/<int:dealer_id>/', view=views.get_dealer_reviews, name='dealer_reviews'),
    path(route='get_dealers', view=views.get_dealerships, name='get_dealers_legacy'),
    path(route='get_dealers/<str:state>', view=views.get_dealers_by_state, name='dealers_by_state_legacy'),
    path(route='dealer/<int:dealer_id>', view=views.get_dealer_details, name='dealer_legacy'),
    path(route='reviews/dealer/<int:dealer_id>', view=views.get_dealer_reviews, name='dealer_reviews_legacy'),

    # cars and sentiment
    path(route='get-carmakes', view=views.get_all_carmakes, name='car_makes'),
    path(route='get_cars', view=views.get_all_carmakes, name='car_makes_legacy'),
    path(route='analyze-review', view=views.analyze_review, name='analyze_review'),
    path(route='add_review', view=views.add_review, name='add_review'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
