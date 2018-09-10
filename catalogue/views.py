from django.http import HttpResponse

# import all the table of the database
from .models import Category, Product, Association
from django.contrib.auth.models import User

# import the utilisation of form
from .forms import ConnexionForm, AssociationForm

from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

# import of functionnality for user's table
from django.contrib.auth import authenticate, login, logout


# Main page
def acceuil(request):
    return render(request, 'catalogue/index.html')


# Page for create a new user
def join(request):
    return render(request, 'catalogue/create_user.html')


# Page for connexion
def connexion(request):

    # Initialisation of variable for the futur message for the user
    message = ''
    color = 'black'

    # If the user create a new account, the redirection is on this page
    if request.method == 'POST':
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        confirmation = request.POST.get('confirmation')

        # Verification of the same password with the confirmation
        if password != confirmation:
            # Modification of the message
            message = 'Les deux Password ne sont pas identique.'
            color = 'red'
            # And transmission of the message
            context = {
                'message': message,
                'color': color,
            }
            # Redirection to the page for create a new user
            return render(request, 'catalogue/create_user.html', context)

        # Verification of a good password
        if len(password) < 6:
            # Modification of the message
            message = 'Merci de choisir un password un peu plus compliqué.'
            color = 'red'
            # And transmission of the message
            context = {
                'message': message,
                'color': color,
            }
            # Redirection to the page for create a new user
            return render(request, 'catalogue/create_user.html', context)

        # Verification of a good username
        if len(username) < 6:
            # Modification of the message
            message = 'Merci de choisir un pseudo plus long.'
            color = 'red'
            # And transmission of the message
            context = {
                'message': message,
                'color': color,
            }
            # Redirection to the page for create a new user
            return render(request, 'catalogue/create_user.html', context)

        # Recuperation of all user in the database
        user = User.objects.filter(email=email)
        # Verification if the email not already used
        if not user.exists():

            user = User.objects.filter(username=username)
            # Verification if the pseudo not already used
            if not user.exists():
                # Creation of a new user
                user = User.objects.create_user(username, email, password)
                # Modification of the message
                message = 'Vous venez de créer votre compte, merci de vous identifiez maintenant.'
                color = 'green'

            else:
                # Modification of the message
                message = 'Ce pseudo est déjà utilisé, merci d\'en trouver un autre.'
                color = 'red'
                # And transmission of the message
                context = {
                    'message': message,
                    'color': color,
                }
                # Redirection to the page for connexion
                return render(request, 'catalogue/create_user.html', context)

        else:
            # Modification of the message
            message = 'Il existe déjà un compte avec cet email, essayez donc de vous identifier avec.'
            color = 'red'
    # And transmission of the message
    context = {
        'message': message,
        'color': color,
    }
    # Redirection to the page for connexion
    return render(request, 'catalogue/connexion.html', context)


# Page of User
def user(request):
    # Creation of a variable for no error
    error = False

    # If the user use the conection page, he is redirected here
    if request.method == "POST":
        # From for connection
        form = ConnexionForm(request.POST)
        # Verification of the form validity
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            # Authentification enabled
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
            else:
                error = True
                # Also error = True, the redirecting is to the connection page
                return render(request, 'catalogue/connexion.html')

        else:
            form = ConnexionForm()
    # Return the user to his own page
    return render(request, 'catalogue/user.html', locals())


# Page of Aliment's user
def aliment(request):
    # If the user click on substitute an aliment, he is redirecting here
    if request.method == "POST":
        # Verification of the form
        form = AssociationForm(request.POST)

        if form.is_valid():
            # If the form is valid, create a new association (user, prod, substitute)
            association = Association(asso_user=form["user"].value(
            ), asso_product=form["product"].value(), asso_product_sub=form["product_sub"].value())
            association.save()

        else:
            form = AssociationForm()
    # Display the page with all the association of substitution
    association_list = Association.objects.filter().order_by('-id')
    products = Product.objects.filter()
    # Transmission of the list
    context = {
        'association_list': association_list,
        'products': products,
    }

    return render(request, 'catalogue/aliment.html', context)


# Creation of a special button disconnect from the nav bar
def deconnexion(request):
    # Django using logout to the user
    logout(request)
    # Moodification of the message
    message = 'A bientôt ! Et au plaisir de vous revoir très vite entouré de bon aliment !'
    color = 'green'
    # Transmission of the message
    context = {
        'message': message,
        'color': color,
    }
    # Redirecting the disconnected user on the connection page
    return render(request, 'catalogue/connexion.html', context)


# Creation of the views listing for the catalogue
def listing(request):
    # Creation a list on the alphabetical order
    products_list = Product.objects.filter().order_by('name')
    # Creation of pagination with only 12 products by page
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


# Page of the detail for an product
def detail(request, product_id):
    # Search of product of substitution, using the category_id
    product = get_object_or_404(Product, pk=product_id)
    category = Category.objects.get(pk=product.category_id)
    categorys_name = category.name
    # and using the nutriscore
    nutri_list = []
    count = product.nutriscore
    while (count > 0):
        count -= 1
        if count != 0:
            nutri_list.append(count)

    message = "Malheureusement, ou bienheureusement selon le point de vue, ce produit est le meilleur dans sa catégorie. Donc pas besoin de le remplacer."

    products = Product.objects.filter(category_id=product.category_id).filter(
        nutriscore__in=nutri_list).order_by('nutriscore')[:12]

    context = {
        'message': message,
        'products': products,
        'product_name': product.name,
        'product_description': product.description,
        'product_nutriscore': product.nutriscore,
        'categorys_name': categorys_name,
        'product_id': product.id,
        'thumbnail': product.picture,
        'nutrition': product.nutrition,
        'link': product.url_off,
    }

    return render(request, 'catalogue/detail.html', context)


# Search page of the website for the catalogue
def search(request):
    # Recuperation of the query from the user
    query = request.GET.get('query')
    if not query:
        # If no query, the website display 12 random products
        products = Product.objects.all().order_by('?')[:12]
    else:
        products = Product.objects.filter(name__icontains=query)

    categorys = Category.objects.filter()

    if not products.exists():
        products = Product.objects.filter(category__name__icontains=query)

    message = "Malheureusement nous n'avons trouvé aucun article correspondant à votre requête."
    link = "https://fr.openfoodfacts.org/cgi/search.pl?search_terms={}&search_simple=1&action=process".format(query)
    name = "Résultats pour la requête %s" % query
    context = {
        'message': message,
        'products': products,
        'categorys': categorys,
        'name': name,
        'link': link
    }

    return render(request, 'catalogue/search.html', context)


# Legal Mention
def legal_mention(request):
    return render(request, 'catalogue/legal_mention.html')
