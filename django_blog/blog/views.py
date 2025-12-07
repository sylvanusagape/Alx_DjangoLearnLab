from django.views.generic import (
    ListView as DjangoListView,
    DetailView as DjangoDetailView,
    CreateView,
    UpdateView,
    DeleteView,
)
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from .forms import CustomUserCreationForm, UserUpdateForm, CommentForm
from django.urls import reverse, reverse_lazy
from .models import Comment, Post
from django.db.models import Q
from taggit.models import Tag


# User-related views
def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = CustomUserCreationForm()
    return render(request, "blog/register.html", {"form": form})


@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        if u_form.is_valid():
            u_form.save()
            return redirect("profile")
    else:
        u_form = UserUpdateForm(instance=request.user)

    return render(request, "blog/profile.html", {"u_form": u_form})


# Post views
class PostListView(DjangoListView):
    model = Post
    template_name = "blog/post_list.html"  # Specify the template to use
    context_object_name = "posts"
    ordering = ["-published_date"]  # Order posts by the published date (newest first)


class PostDetailView(DjangoDetailView):
    model = Post
    template_name = "blog/post_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["comments"] = Comment.objects.filter(post=self.object).order_by(
            "-created_at"
        )
        context["comment_form"] = CommentForm()
        return context

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        post = self.get_object()
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect("post-detail", pk=post.pk)
        return self.get(request, *args, **kwargs)


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Set the author to the logged-in user
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.object.pk})


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ["title", "content"]
    template_name = "blog/post_form.html"

    def form_valid(self, form):
        form.instance.author = self.request.user  # Ensure author is the logged-in user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.author
        )  # Only allow authors to update their posts


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = "blog/post_confirm_delete.html"
    success_url = reverse_lazy("post-list")  # Redirect after deletion

    def test_func(self):
        post = self.get_object()
        return (
            self.request.user == post.author
        )  # Only allow authors to delete their posts


# Comment views
class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"  # Create this template if it doesn't exist

    def form_valid(self, form):
        form.instance.author = self.request.user
        form.instance.post = get_object_or_404(Post, id=self.kwargs["post_id"])
        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy("post-detail", kwargs={"pk": self.kwargs["post_id"]})


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Comment
    form_class = CommentForm
    template_name = "blog/comment_form.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post"] = (
            self.object.post
        )  # Assuming Comment model has a ForeignKey to Post
        return context

    def get_success_url(self):
        return reverse(
            "post-detail", kwargs={"pk": self.object.post.pk}
        )  # Redirect to post detail after updating comment

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only the author can edit


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = "blog/comment_confirm_delete.html"

    def get_success_url(self):
        post = self.get_object().post
        return reverse_lazy("post-detail", kwargs={"pk": post.pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author  # Only the author can delete


# Tagging and Search Functionality
class PostSearchView(DjangoListView):
    model = Post
    template_name = "blog/search_results.html"
    context_object_name = "posts"

    def get_queryset(self):
        query = self.request.GET.get("q")
        if query:
            return Post.objects.filter(
                Q(title__icontains=query)
                | Q(content__icontains=query)
                | Q(tags__name__icontains=query)
            ).distinct()
        return Post.objects.none()


class PostByTagListView(DjangoListView):
    model = Post
    template_name = "blog/post_list.html"
    context_object_name = "posts"

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs.get("tag_slug"))
        return Post.objects.filter(tags__in=[tag])