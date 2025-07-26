# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.user_trees, name='user_trees'),
#     path('tree/<int:pk>/', views.tree_detail, name='tree_detail'),
#     path('add/', views.add_planted_tree, name='add_planted_tree'),
#     path('accounts/trees/', views.account_trees, name='account_trees'),
#     path('api/my-trees/', views.my_trees_api, name='my_trees_api'),

# ]

from django.urls import path
from .views import (
    UserTreeListView,
    TreeDetailView,
    AddPlantedTreeView,
    AccountTreesView,
    my_trees_api,
)

urlpatterns = [
    path('', UserTreeListView.as_view(), name='user_trees'),
    path('tree/<int:pk>/', TreeDetailView.as_view(), name='tree_detail'),
    path('add/', AddPlantedTreeView.as_view(), name='add_planted_tree'),
    path('accounts/trees/', AccountTreesView.as_view(), name='account_trees'),
    path('api/my-trees/', my_trees_api, name='my_trees_api'),
]
