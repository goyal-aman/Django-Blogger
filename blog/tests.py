from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.test import Client
from django.utils import timezone

from .models import Post

User = get_user_model()


class LoginTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )

    def test_user_login(self):
        self.assertTrue(self.islogin)
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_user_logout(self):
        self.client.logout()
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 302)


class HomePageTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )

    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class PostModelTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )

        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_post_content(self):
        post = Post.objects.get(id=1)
        user = get_user_model().objects.get(username='test')
        response = self.client.get(
            reverse('blog-post-user', kwargs={'username': user.username}))

        exp_title = 'test title'
        exp_content = 'test content'
        exp_author = user

        self.assertEqual(exp_title, post.title)
        self.assertEqual(exp_content, post.content)
        self.assertEqual(exp_author, post.author)


class UserProfileListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )

        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_view_url_by_name(self):
        self.user = get_user_model().objects.get(username='test')
        response = self.client.get(
            reverse('blog-post-user', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        user = get_user_model().objects.get(username='test')
        response = self.client.get(
            reverse('blog-post-user', kwargs={'username': user.username})
        )
        self.assertTemplateUsed(response, 'blog/post_user.html')


class PostListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )

    def test_view_require_login(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 302)

    def test_page_login(self):
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )
        self.assertTrue(self.islogin)

    def test_veiw_url_by_name(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, 'blog/home.html')


class PostDetailViewTest(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )
        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_veiw_url_by_name(self):
        response = self.client.get(
            reverse('blog-post-detail', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse('blog-post-detail', kwargs={'pk': self.post.pk})
        )
        self.assertTemplateUsed(response, 'blog/post_detail.html')


class PostCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )

    def test_view_require_login(self):
        response = self.client.get(reverse('blog-post-create'))
        self.assertEqual(response.status_code, 302)

    def test_page_login(self):
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )
        self.assertTrue(self.islogin)

    def test_create_new_post(self):
        self.client.login(email='test@test.com', password='passaman')
        self.client.post(
            reverse('blog-post-create'),
            {
                'title': 'test_post',
                'content': 'test_content',
            }
        )
        self.post = Post.objects.first()

        self.assertEqual(self.post.title, 'test_post')
        self.assertEqual(self.post.content, 'test_content')

    def test_veiw_url_by_name(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(reverse('blog-post-create'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(reverse('blog-post-create'))
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostUpdateTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )
        self.other_user = User.objects.create_user(
            email='other@user.com',
            username='other_user',
            first_name='other_user_fname',
            last_name='other_user_lname',
            password='passaman'
        )
        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_view_require_login(self):
        response = self.client.get(
            reverse(
                'blog-post-update',
                kwargs={'pk': self.post.pk}
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_page_login(self):
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )
        self.assertTrue(self.islogin)

    def test_update_new_post(self):
        self.client.login(email='test@test.com', password='passaman')
        self.client.post(
            reverse('blog-post-update', kwargs={'pk': self.post.pk}),
            {
                'title': 'test_post_updated',
                'content': 'test_content_updated',
            }
        )

        self.post = Post.objects.first()

        self.assertEqual(self.post.title, 'test_post_updated')
        self.assertEqual(self.post.content, 'test_content_updated')

    def test_only_author_can_update_post(self):
        self.client.login(email='other@user.com', password='passaman')
        response = self.client.post(
            reverse('blog-post-update', kwargs={'pk': self.post.pk}),
            {
                'title': 'test_post_updated',
                'content': 'test_content_updated',
            }
        )
        self.assertEqual(response.status_code, 403)

    def test_veiw_url_by_name(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(
            reverse('blog-post-update', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(
            reverse('blog-post-update', kwargs={'pk': self.post.pk})
        )
        self.assertTemplateUsed(response, 'blog/post_form.html')


class PostDeleteTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            email='test@test.com',
            username='test',
            first_name='test_fname',
            last_name='test_lname',
            password='passaman'
        )
        self.other_user = User.objects.create_user(
            email='other@user.com',
            username='other_user',
            first_name='other_user_fname',
            last_name='other_user_lname',
            password='passaman'
        )
        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.user
        )

    def test_view_require_login(self):
        response = self.client.get(
            reverse(
                'blog-post-delete',
                kwargs={'pk': self.post.pk}
            )
        )
        self.assertEqual(response.status_code, 302)

    def test_page_login(self):
        self.islogin = self.client.login(
            email='test@test.com',
            password='passaman'
        )
        self.assertTrue(self.islogin)

    def test_post_delete_works(self):
        self.client.login(
            email='test@test.com',
            password='passaman'
        )
        response = self.client.post(
            reverse(
                'blog-post-delete',
                kwargs={'pk': self.post.pk}
            )
        )
        self.assertEqual(Post.objects.all().count(), 0)

    def test_only_author_can_delete_post(self):
        self.client.login(email='other@user.com', password='passaman')
        respose = self.client.post(
            reverse(
                'blog-post-delete',
                kwargs={'pk': self.post.pk}
            )
        )
        self.assertEqual(respose.status_code, 403)

    def test_veiw_url_by_name(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(
            reverse('blog-post-delete', kwargs={'pk': self.post.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        self.client.login(email='test@test.com', password='passaman')
        response = self.client.get(
            reverse('blog-post-delete', kwargs={'pk': self.post.pk})
        )
        self.assertTemplateUsed(response, 'blog/post_confirm_delete.html')


class ShowFollowerTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            email='user1@user.com',
            username='user1',
            first_name='user1_fname',
            last_name='user1_lname',
            password='passaman'
        )
        self.user2 = User.objects.create_user(
            email='user2@user.com',
            username='use2',
            first_name='user2_fname',
            last_name='user2_lname',
            password='passaman'
        )
        self.user3 = User.objects.create_user(
            email='user3@user.com',
            username='user3',
            first_name='user3_fname',
            last_name='user3_lname',
            password='passaman'
        )
        self.user1.profile.followedby.add(self.user2.profile)
        self.user1.profile.followedby.add(self.user3.profile)

    def test_user_followers(self):
        user = User.objects.get(username=self.user1.username)
        response = self.client.get(
            reverse('user-follower', kwargs={'username': user.username})
        )
        self.assertEqual(response.context['followers'][0], self.user2.profile)
        self.assertEqual(response.context['followers'][1], self.user3.profile)
        self.assertEqual(response.context['followers'].count(), 2)

    def test_veiw_url_by_name(self):
        response = self.client.get(
            reverse('user-follower',
                    kwargs={'username': self.user1.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse(
                'user-follower',
                kwargs={'username': self.user1.username}
            )
        )
        self.assertTemplateUsed(response, 'blog/followers.html')


class ShowFollowingTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user1 = User.objects.create_user(
            email='user1@user.com',
            username='user1',
            first_name='user1_fname',
            last_name='user1_lname',
            password='passaman'
        )
        self.user2 = User.objects.create_user(
            email='user2@user.com',
            username='use2',
            first_name='user2_fname',
            last_name='user2_lname',
            password='passaman'
        )
        self.user3 = User.objects.create_user(
            email='user3@user.com',
            username='user3',
            first_name='user3_fname',
            last_name='user3_lname',
            password='passaman'
        )
        self.user1.profile.isfollowing.add(self.user2.profile)
        self.user1.profile.isfollowing.add(self.user3.profile)

    def test_user_following(self):
        user = User.objects.get(username=self.user1.username)
        response = self.client.get(
            reverse('user-following', kwargs={'username': user.username})
        )
        self.assertEqual(response.context['followings'][0], self.user2.profile)
        self.assertEqual(response.context['followings'][1], self.user3.profile)
        self.assertEqual(response.context['followings'].count(), 2)

    def test_veiw_url_by_name(self):
        response = self.client.get(
            reverse('user-following',
                    kwargs={'username': self.user1.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(
            reverse(
                'user-following',
                kwargs={'username': self.user1.username}
            )
        )
        self.assertTemplateUsed(response, 'blog/following.html')
