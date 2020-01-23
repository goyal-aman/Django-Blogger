from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=get_user_model())
def create_profile(sender, instance, created, **kwargs):
    if created:
        new_user_profile = Profile.objects.create(user=instance)

        #assuming there is single super user.
        try:
            superuser = get_user_model().objects.get(is_superuser=True)
            superuser.profile.followedby.add(new_user_profile)
            new_user_profile.isfollowing.add(superuser.profile)
        except:
            pass
# @receiver(post_save, sender=get_user_model())
# def save_profile(sender, instance, **kwargs):
#     instance.profile.save()