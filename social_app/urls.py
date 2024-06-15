from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include("accounts.urls")),
    path("moments/", include("moments.urls")),
    path("feature/", include("features.urls")),
    path("story/", include("story.urls")),
    path("blog/", include("blog.urls")),
    path("chat/", include("chatsystem.urls")),
    path("note/", include("notes.urls")),
    path("share/", include("share.urls")),
    path("post/", include("PostConnect.urls"))

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
