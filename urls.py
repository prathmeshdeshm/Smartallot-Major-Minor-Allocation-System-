from django.urls import path
from . import views

urlpatterns = [
    # Dashboards
    path('', views.home, name='home'),
    path('dashboard/admin/', views.admin_dashboard, name='admin_dashboard'),
    path('dashboard/student/', views.student_dashboard, name='student_dashboard'),

    # Course Management
    path('manage-courses/', views.manage_courses, name='manage_courses'),
    path('courses/create/', views.course_create, name='course_create'),
    path('courses/<str:course_type>/<int:pk>/update/', views.course_update, name='course_update'),
    path('courses/<str:course_type>/<int:pk>/delete/', views.course_delete, name='course_delete'),

    # ---------- MINOR RULES ----------
    path('rules/<int:branch_pk>/create/', views.rule_create, name='rule_create'),
    path('rules/<int:pk>/edit/', views.rule_edit, name='rule_edit'),
    path('rules/<int:pk>/toggle/', views.rule_toggle_active, name='rule_toggle'),
    path('rules/<int:pk>/delete/', views.rule_delete, name='rule_delete'),

    # ---------- OE RULES ----------
    path('rules/oe/<int:oe_pk>/add/', views.oe_rule_create, name='oe_rule_create'),
    path('rules/oe/<int:pk>/edit/', views.oe_rule_edit, name='oe_rule_edit'),
    path('rules/oe/<int:pk>/toggle/', views.oe_rule_toggle_active, name='oe_rule_toggle'),
    path('rules/oe/<int:pk>/delete/', views.oe_rule_delete, name='oe_rule_delete'),

    # Reports
    path('reports/download/csv/', views.download_csv_report, name='download_csv_report'),
]
