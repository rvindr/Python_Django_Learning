
from django.urls import path, include
from tracker.views import ExpenseView,DeleteExpenseView

urlpatterns = [

    path('',ExpenseView.as_view(),name='expense_view'),
    path('delete/<str:expense_id>/', DeleteExpenseView.as_view(), name='delete_expense'),

]
