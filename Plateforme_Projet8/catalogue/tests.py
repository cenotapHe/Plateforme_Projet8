from django.test import TestCase

from django.urls import reverse

from .models import Product, Category, Association
from django.contrib.auth.models import User


class IndexPageTestCase(TestCase):

    def test_index_page_returns_200(self):
        response = self.client.get(reverse('acceuil'))
        self.assertEqual(response.status_code, 200)


class DetailPageTestCase(TestCase):

	def setUp(self):
		new_category = Category.objects.create(name="New Category")
		new_category_id = Category.objects.get(name="New Category").id
		new_product = Product.objects.create(name="New Product", nutriscore=5, category_id=new_category_id)


	def test_detail_page_returns_200(self):
		new_product_id = Product.objects.get(name="New Product").id
		response = self.client.get(reverse('catalogue:detail', args=(new_product_id,)))
		self.assertEqual(response.status_code, 200)


	def test_detail_page_returns_404(self):
		new_product_id = Product.objects.get(name="New Product").id + 100
		response = self.client.get(reverse('catalogue:detail', args=(new_product_id,)))
		self.assertEqual(response.status_code, 404)

	def test_proposition_for_substitution(self):
		new_product_id = Product.objects.get(name="New Product").id
		old_context = self.client.get(reverse('catalogue:detail', args=(new_product_id,))).context
		
		new_category_id = Product.objects.get(name="New Product").id
		new_product_2 = Product.objects.create(name="New Product 2", nutriscore=1, category_id=new_category_id)

		new_product_id = Product.objects.get(name="New Product").id
		new_context = self.client.get(reverse('catalogue:detail', args=(new_product_id,))).context

		self.assertNotEqual(old_context, new_context)


class JoinUserTestCase(TestCase):

	def test_index_page_returns_200(self):
		response = self.client.get(reverse('catalogue:user'))
		self.assertEqual(response.status_code, 200)


	def test_index_page_returns_200(self):
		response = self.client.get(reverse('catalogue:connexion'))
		self.assertEqual(response.status_code, 200)


	def test_new_user_is_created(self):
		old_users = User.objects.count()
		email = str('test@test.test')
		username = str('Patrick')
		password = str('password')
		confirmation = str('password')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		new_users = User.objects.count()
		self.assertEqual(new_users, old_users + 1)


	def test_too_small_username(self):
		old_users = User.objects.count()
		email = str('test@test.test')
		username = str('Pat')
		password = str('password')
		confirmation = str('password')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		new_users = User.objects.count()
		self.assertEqual(new_users, old_users)


	def test_no_confirmation_password(self):
		old_users = User.objects.count()
		email = str('test@test.test')
		username = str('Patrick')
		password = str('password')
		confirmation = str('test')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		new_users = User.objects.count()
		self.assertEqual(new_users, old_users)


	def test_two_account_with_same_pseudo(self):
		email = str('test@test.test')
		username = str('Patrick')
		password = str('password')
		confirmation = str('password')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		old_users = User.objects.count()
		email = str('lol@lol.lol')
		username = str('Patrick')
		password = str('motdepasse')
		confirmation = str('motdepasse')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		new_users = User.objects.count()
		self.assertEqual(new_users, old_users)


	def test_two_account_with_same_email(self):
		email = str('test@test.test')
		username = str('Patrick')
		password = str('password')
		confirmation = str('password')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		old_users = User.objects.count()
		email = str('test@test.test')
		username = str('Josiane')
		password = str('motdepasse')
		confirmation = str('motdepasse')
		response = self.client.post(reverse('catalogue:connexion'), {
				'email': email,
				'username': username,
				'password': password,
				'confirmation': confirmation,
			})
		new_users = User.objects.count()
		self.assertEqual(new_users, old_users)


class CataloguehUserTestCase(TestCase):

	def test_catalogue_page_returns_200(self):
		response = self.client.get(reverse('catalogue:listing'))
		self.assertEqual(response.status_code, 200)


class SearchUserTestCase(TestCase):

	def test_search_page_returns_200(self):
		chocolat = str('chocolat')
		response = self.client.get(reverse('catalogue:search'), {
			'query': chocolat,
			})
		self.assertEqual(response.status_code, 200)


	def test_search_page_returns_200_with_no_query(self):
		chocolat = str('')
		response = self.client.get(reverse('catalogue:search'), {
			'query': chocolat,
			})
		self.assertEqual(response.status_code, 200)


class AlimentUserTestCase(TestCase):

	def aliment_page_returns_200(self):
		response = self.client.get(reverse('catalogue:aliment'))
		self.assertEqual(response.status_code, 200)


	def substitute_aliment(self):
		old_association = Association.objects.count()
		response = self.client.post(reverse('catalogue:aliment'), {
			'asso_user': 1,
			'asso_product': 1, 
			'asso_product_sub': 1,
			})
		new_association = Association.objects.count()
		self.assertEqual(old_association, new_association + 1)