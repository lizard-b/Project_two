from django.http import HttpResponseForbidden


def form_valid(self, form):
    post = form.save(commit=False)
    if (self.request.path == f'/news/{post.id}/edit/' and post.post_type != 'NEW') or \
            (self.request.path == f'/articles/{post.id}/edit/' and post.post_type != 'ART'):
        return HttpResponseForbidden("Вы не можете вносить изменения в данный тип поста.")
    return super().form_valid(form)
