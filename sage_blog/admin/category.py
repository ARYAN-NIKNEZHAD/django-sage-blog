from django.contrib import admin
from django.db.models import Count, Q, QuerySet
from django.utils.translation import gettext_lazy as _

from sage_blog.models import PostCategory
from sage_blog.admin.filters import PostsStatusFilter


@admin.register(PostCategory)
class PostCategoryAdmin(admin.ModelAdmin):
    """
    Django admin customization for the PostCategory model.

    This admin class customizes the display and search capabilities for PostCategories
    in the Django admin interface. It provides an intuitive interface for managing blog
    post categories.
    """

    # Display settings
    admin_priority = 1
    list_display = ("title", "slug", "is_published", "published_posts_count", "modified_at")
    list_filter = (PostsStatusFilter, "is_published")
    search_fields = ("title",)
    date_hierarchy = "created_at"
    ordering = ("title",)
    save_on_top = True

    # Form layout customization
    fieldsets = (
        (None, {"fields": ("title", "slug", "is_published")}),
        (_("Timestamps"), {"fields": ("created_at", "modified_at")}),
    )
    readonly_fields = ("created_at", "modified_at", "slug")

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.join_posts()
        return queryset

    @admin.display(description=_("Published Posts"))
    def published_posts_count(self, obj):
        # Annotate the count of published posts directly when accessed
        return obj.posts.filter(is_published=True).count()
