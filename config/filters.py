from .models import Job
import django_filters


class JobFilter(django_filters.FilterSet):
    salary_gt = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="gt",
    )
    salary_lt = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="lt",
    )
    salary_gte = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="gte",
    )
    salary_lte = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="lte",
    )
    salary_range = django_filters.NumberFilter(
        field_name="salary",
        lookup_expr="range",
    )

    min_experience_years_gte = django_filters.NumberFilter(
        field_name="min_experience_years", lookup_expr="gte"
    )
    min_experience_years_lte = django_filters.NumberFilter(
        field_name="min_experience_years", lookup_expr="lte"
    )

    max_experience_years_gte = django_filters.NumberFilter(
        field_name="max_experience_years", lookup_expr="gte"
    )
    max_experience_years_lte = django_filters.NumberFilter(
        field_name="max_experience_years", lookup_expr="lte"
    )

    class Meta:
        model = Job
        fields = [
            "company__id",
            "location",
            "is_active",
            "category",
            "experience",
            "mode",
            "salary_currency",
        ]
