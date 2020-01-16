from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from .models import Post


class HomePageTest(TestCase):
    def test_home_page_status_code(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)


class PostModelTest(TestCase):
    def setUp(self):
        self.testuser = get_user_model().objects.create(
            email='email@email.com',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
        )

        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.testuser
        )

    def test_post_content(self):
        post = Post.objects.get(id=1)
        user = get_user_model().objects.get(username='testuser')
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
        self.testuser = get_user_model().objects.create(
            email='email@email.com',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
        )

        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.testuser
        )

    def test_view_url_by_name(self):
        self.user = get_user_model().objects.get(username='testuser')
        response = self.client.get(
            reverse('blog-post-user', kwargs={'username': self.user.username})
        )
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        user = get_user_model().objects.get(username='testuser')
        response = self.client.get(
            reverse('blog-post-user', kwargs={'username': user.username})
        )
        self.assertTemplateUsed(response, 'blog/profile_post_list.html')


class PostListViewTest(TestCase):

    def test_veiw_url_by_name_and_page_exist(self):
        response = self.client.get(reverse('blog-home'))
        self.assertEqual(response.status_code, 200)

    def test_template_used(self):
        response = self.client.get(reverse('blog-home'))
        self.assertTemplateUsed(response, 'blog/home.html')


class PostDetailViewTest(TestCase):

    def setUp(self):
        self.testuser = get_user_model().objects.create(
            email='email@email.com',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
        )
        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.testuser
        )

    def test_view_url_by_name_and_template_used(self):
        user = get_user_model().objects.get(username='testuser')
        post = Post.objects.get(author=user)
        user = get_user_model().objects.get(username='testuser')
        response = self.client.get(
            reverse('blog-post-detail', kwargs={'pk': post.id})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_detail.html')


class PostCreateViewTest(TestCase):
    def setUP(self):
        self.testuser = get_user_model().objects.create(
            email='email@email.com',
            username='testuser',
            first_name='test_first_name',
            last_name='test_last_name',
            password='password'
        )
        self.post = Post.objects.create(
            title='test title',
            content='test content',
            author=self.testuser
        )
    '''
    TODO
    '''
    # def test_post_create_redirect_without_login(self):
    #     self.testuser = get_user_model().objects.create(
    #         email='email@email.com',
    #         username='testuser',
    #         first_name='test_first_name',
    #         last_name='test_last_name',
    #         password='passaman'
    #     )
    #     response = self.client.post(
    #         reverse('blog-post-create'),
    #         {
    #             'title':'new_title',
    #             'content':'new_content'
    #         }
    #     )
    #     self.assertEqual(response.status_code, 200)


    # def test_view_url_by_name_and_page_exist(self):
    #     response = self.client.get(reverse('blog-post-create'))
    #     self.assertEqual(response, 200)

    # def test_template_used(self):
    #     response = self.client.get(reverse('blog-post-create'))
    #     self.assertTemplateUsed(response, 'blog/post_form.html')


# class PostUpdateTest(TestCase):
'''
TODO: complete this and delete veiw
'''
#     def test_view_url_by_name_and_page_exist(self):
#         response = self.client.get(reverse('blog-post-create'))
#         self.assertEqual(response, 200)

#     def test_template_used(self):
#         response = self.client.get(reverse('blog-post-create'))
#         self.assertTemplateUsed(response, 'blog/post_form.html')
