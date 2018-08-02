from django.http import HttpResponse

from .models import Category, Product

from django.template import loader

from django.shortcuts import render, get_object_or_404

from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def index(request):
	
	products = Product.objects.filter()[:12]
	categorys = Category.objects.filter()
	
	context = {
		'products': products,
		'categorys': categorys
	}
	
	return render(request, 'catalogue/index.html', context)


def listing(request):
	products_list = Product.objects.filter()
	paginator = Paginator(products_list, 4)
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

	message = "Malheureusement, ou bienheureusement, ce produit est le meilleur dans sa catégorie. Donc pas besoin de le remplacer."

	products = Product.objects.filter(category_id=product.category_id).filter(nutriscore__in=nutri_list).order_by('nutriscore')

	context = {
		'message': message,
		'products': products,
		'product_name': product.name,
		'product_description': product.description,
		'product_nutriscore' : product.nutriscore,
		'categorys_name': categorys_name,
		'product_id': product.id,
		'thumbnail': product.picture
	}
	
	return render(request, 'catalogue/detail.html', context)



def search(request):
    query = request.GET.get('query')
    if not query:
        products = Product.objects.all()
    else:
        products = Product.objects.filter(name__icontains=query)

    categorys = Category.objects.filter()

    if not products.exists():
    	products = Product.objects.filter(category__name__icontains=query)

    paginator = Paginator(products, 4)
    page = request.GET.get('page')

    try:
    	products = paginator.page(page)
    except PageNotAnInteger:
    	products = paginator.page(1)
    except EmptyPage:
    	products = paginator.page(paginator.num_pages)


    message = "Malheureusement nous n'avons trouvé aucun article correspondant à votre requête."
    name = "Résultats pour la requête %s"%query
    context = {
    	'message': message,
    	'products': products,
    	'paginate': True,
    	'categorys': categorys,
    	'name': name
    }

    return render(request, 'catalogue/search.html', context)
