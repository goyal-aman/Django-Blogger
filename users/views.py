from django.shortcuts import render, redirect, get_object_or_404, reverse, HttpResponse
from .forms import UserCreationForm, UserUpdateForm, ProfileUpdateForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

# Create your views here.
# class UserProfileListView(ListView):
#     '''
#     modified get_queryset, return only posts queryset filtered by username
#     kwarg: username
#     '''
#     model = Post
#     template_name = 'blog/profile_post_list.html'
#     context_object_name = 'object'
#     paginate_by = 10
    
#     def get_user(self, **kwargs):
#         '''return user object with username = self.kwargs.get('username')'''
#         return get_user_model().objects.get(username=self.kwargs.get('username'))
    
#     def get_queryset(self):
#         self.profile_user = get_object_or_404(get_user_model(), username=self.kwargs.get('username'))
#         return Post.objects.filter(author=self.profile_user)


def user_profile_page(request, username):
    return render(request, 'users/profile_post_list.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username    = form.cleaned_data.get('username')
            messages.success(request,f'{username} Registered')
            return redirect('users-login')
    else:
        form = UserCreationForm()
    return render(request, 'users/register.html', { 'form':form})

@login_required
def profile_edit(request):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request,'Updated')
            return redirect('users-profile-edit')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'p_form':p_form,
        'u_form':u_form
    }
    return render(request, 'users/profile.html', context)

def follow_user(request, id):
    '''id: id of the to-user'''
    if request.user.is_authenticated:
        to_user     = get_object_or_404(User, id=id)
        from_user   = get_object_or_404(User, id=request.user.id)
        
        from_user.profile.isfollowing.add(to_user.profile)
        to_user.profile.followedby.add(from_user.profile)
        return redirect(reverse('blog-post-user', kwargs={'username':to_user.username}))

def unfollow_user(request, id):
    '''id: id of the to-user'''
    if request.user.is_authenticated:
        to_user     = get_object_or_404(User, id=id)
        from_user   = get_object_or_404(User, id=request.user.id)
        print(f"this is to user {to_user}, this is from_user {from_user}")
        from_user.profile.isfollowing.remove(to_user.profile)
        to_user.profile.followedby.remove(from_user.profile)

        # friend_request = FriendRequest.objects.filter(to_user=to_user, from_user=from_user).first()
        # friend_request.delete()

        return redirect(reverse('blog-post-user', kwargs={'username':to_user.username}))

