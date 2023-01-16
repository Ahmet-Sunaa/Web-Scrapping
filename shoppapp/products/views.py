from django.shortcuts import render , get_object_or_404
from django.db.models import  Q
from .models import Products
from .tasks import start_task
from django.core.paginator import Paginator



def home(request):
   if Products.objects.filter(id=1).exists():
      pass
   else:
      start_task.apply_async()
   return render(request,"yönlendirme sayfası.html",{'status':"Veriler Çekliyor Lütfen Bekleyiniz"})


def view_products(request):
   product_list = Products.objects.all()
   os=[]
   screen_sizes=[]
   brands=[]
   rams=[]
   cpu_models=[]
   disk_sizes=[]
   models=[]
   ratings=[]
   for br in product_list:
         brands.append(br.brand)
   brands=list(set(brands))
   for ss in product_list:
         screen_sizes.append(ss.screen_size.replace(","," "))
   screen_sizes=list(set(screen_sizes))
   for o in product_list:
         os.append(o.operating_system)
   os=list(set(os))
   for ram in product_list:
         rams.append(ram.ram)
   rams=list(set(rams))
   for cpu in product_list:
         cpu_models.append(cpu.processor_model)
   cpu_models=list(set(cpu_models))
   for size in product_list:
         disk_sizes.append(size.disk_size)
   disk_sizes=list(set(disk_sizes))
   for model in product_list:
         models.append(model.model)
   models=list(set(models))
   for rating in product_list:
         ratings.append(rating.rating)
   ratings=list(set(ratings))
   query=request.GET.get('q')
   if query:
      product_list=product_list.filter(
         Q(title__icontains=query) |
         Q(model__icontains=query) |
         Q(seller_name__icontains=query) 
      )
   paginator = Paginator(product_list, 24) 
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   return render(request,'eticaret.html',{'page_obj': page_obj ,'brands':brands,'screen_size':screen_sizes,'os':os,'rams':rams,'cpu_model':cpu_models,'disk_size':disk_sizes,'models':models,'ratings':ratings})

def view_all_products(request):
   product_list=Products.objects.all()
   query=request.GET.get('q')
   if query:
      product_list=product_list.filter(
         Q(title__icontains=query) |
         Q(model__icontains=query) |
         Q(seller_name__icontains=query)
      )
   paginator = Paginator(product_list, 24)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)
   return render(request,'fullpcler.html',{'page_obj': page_obj})

def feature(request,id):
   pro=get_object_or_404(Products,id=id)
   context={
      "product":pro
   }
   return render(request,"main.html",context)


def category_by_brand(request,brand):
   filtered_list=Products.objects.filter(brand=brand)
   paginator = Paginator(filtered_list, 24)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)

   return render(request,'eticaret.html',{'page_obj': page_obj})

def category_by_size(request,size):
   print(size)
   filtered_list=Products.objects.filter(screen_size__icontains=size.replace("-",","))
   paginator = Paginator(filtered_list, 24)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)

   return render(request,'eticaret.html',{'page_obj': page_obj})



def category_by_os(request,os):
   filtered_list=Products.objects.filter(operating_system=os)
   paginator = Paginator(filtered_list, 24)
   page_number = request.GET.get('page')
   page_obj = paginator.get_page(page_number)

   return render(request,'eticaret.html',{'page_obj': page_obj})