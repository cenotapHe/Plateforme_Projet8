from django.http import HttpResponse

from .models import Category, Product, Association

from .forms import ConnexionForm, AssociationForm

from django.template import loader

from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.contrib.auth.models import User

from django.contrib.auth import authenticate, login, logout



def index(request):
	
	return render(request, 'catalogue/index.html')


def join(request):

	return render(request, 'catalogue/create_user.html')


def connexion(request):


	message = ''
	color = 'black'

	if request.method == 'POST':
		email = request.POST.get('email')
		username = request.POST.get('username')
		password = request.POST.get('password')
		confirmation = request.POST.get('confirmation')

		if password != confirmation:

			message = 'Les deux Password ne sont pas identique.'
			color = 'red'

			context = {
					'message': message,
					'color': color,
				}

			return render(request, 'catalogue/create_user.html', context)

		if len(password) < 6:

			message = 'Merci de choisir un password un peu plus compliqué.'
			color = 'red'

			context = {
					'message': message,
					'color': color,
				}

			return render(request, 'catalogue/create_user.html', context)

		if len(username) < 6:

			message = 'Merci de choisir un pseudo plus long.'
			color = 'red'

			context = {
					'message': message,
					'color': color,
				}

			return render(request, 'catalogue/create_user.html', context)

		user = User.objects.filter(email=email)
		if not user.exists():

			user = User.objects.filter(username=username)
			if not user.exists():

				user = User.objects.create_user(username, email, password)
				message = 'Vous venez de créer votre compte, merci de vous identifiez maintenant.'
				color = 'green'

			else :
				message = 'Ce pseudo est déjà utilisé, merci d\'en trouver un autre.'
				color = 'red'

				context = {
					'message': message,
					'color': color,
				}

				return render(request, 'catalogue/create_user.html', context)

		else :
			message = 'Il existe déjà un compte avec cet email, essayez donc de vous identifier avec.'
			color = 'red'

	context = {
		'message': message,
		'color': color,
	}

	return render(request, 'catalogue/connexion.html', context)


def user(request):

	error = False

	if request.method == "POST":
		form = ConnexionForm(request.POST)

		if form.is_valid():
			username = form.cleaned_data["username"]
			password = form.cleaned_data["password"]
			user = authenticate(username=username, password=password)

			if user:
				login(request, user)
			else:
				error = True

				return render(request, 'catalogue/connexion.html')

		else:
			form = ConnexionForm()

	return render(request, 'catalogue/user.html', locals())


def aliment(request):

	if request.method == "POST":
		
		form = AssociationForm(request.POST)

		print(form["user"].value())
		print(form["product"].value())
		print(form["product_sub"].value())

		if form.is_valid():

			association = Association(asso_user=form["user"].value(), asso_product=form["product"].value(), asso_product_sub=form["product_sub"].value())

			association.save()

		else:
			form = AssociationForm()

	association_list = Association.objects.filter().order_by('-id')
	products = Product.objects.filter()

	context = {
		'association_list': association_list,
		'products': products,
	}


	return render(request, 'catalogue/aliment.html', context)


def deconnexion(request):
	logout(request)
	message = 'A bientôt ! Et au plaisir de vous revoir très vite entouré de bon aliment !'
	color = 'green'
	context = {
		'message': message,
		'color': color,
	}
	return render(request, 'catalogue/connexion.html', context)


def listing(request):
	products_list = Product.objects.filter().order_by('name')
	paginator = Paginator(products_list, 12)
	page = request.GET.get('page')
	try:
		products = paginator.page(page)
	except PageNotAnInteger:
		products = paginator.page(1)
	except EmptyPage:
		products = paginator.page(paginator.num_pages)

	context = {
		'products': products,
		'paginate': True
	}
	
	return render(request, 'catalogue/listing.html', context)



def detail(request, product_id):

	product = get_object_or_404(Product, pk=product_id)
	category = Category.objects.get(pk=product.category_id)
	categorys_name = category.name

	nutri_list = []
	count = product.nutriscore
	while (count > 0):
		count -= 1
		if count != 0:
			nutri_list.append(count)

	message = "Malheureusement, ou bienheureusement selon le point de vue, ce produit est le meilleur dans sa catégorie. Donc pas besoin de le remplacer."

	products = Product.objects.filter(category_id=product.category_id).filter(nutriscore__in=nutri_list).order_by('nutriscore')[:12]

	context = {
		'message': message,
		'products': products,
		'product_name': product.name,
		'product_description': product.description,
		'product_nutriscore' : product.nutriscore,
		'categorys_name': categorys_name,
		'product_id': product.id,
		'thumbnail': product.picture,
		'nutrition': product.nutrition,
		'link': product.url_off,
	}
	
	return render(request, 'catalogue/detail.html', context)



def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all().order_by('?')[:12]
    else:
        products = Product.objects.filter(name__icontains=query)

    categorys = Category.objects.filter()

    if not products.exists():
    	products = Product.objects.filter(category__name__icontains=query)


    message = "Malheureusement nous n'avons trouvé aucun article correspondant à votre requête."
    name = "Résultats pour la requête %s"%query
    context = {
    	'message': message,
    	'products': products,
    	'categorys': categorys,
    	'name': name
    }

    return render(request, 'catalogue/search.html', context)


