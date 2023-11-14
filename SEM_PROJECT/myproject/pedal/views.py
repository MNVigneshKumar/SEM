from django.http import HttpResponse
from django.shortcuts import  render,redirect
from django.views.decorators.csrf import csrf_exempt
from django.core.files.images import ImageFile
import razorpay
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from .forms import SignUpForm,CycleForm
from .models import Cycle,AppUser,Order,Payment,Rent
from datetime import datetime,timedelta


orders={}

cnt=0
# class Cycle:

# 	def __init__(self,model,address,dop,price,img='cycle1.png'):
# 		global cnt
# 		cnt+=1
# 		self.model=model
# 		self.address=address
# 		self.dop=dop
# 		self.price=price
# 		self.img="http://localhost:8080/"+str(img)
# 		self.id=cnt
# 		print(f"{self.id} and {self.model}")
# 	def __str__(self):
# 		return f"cyle_id:{self.id} model {self.model} "


class Review:
	def __init__(self,cycle_id,content,user_name,img_link,date):
		self.cycle_id=cycle_id
		self.content=content
		self.user_name=user_name
		self.img_link=img_link
		self.date=date

class User:
	def __init__(self,user_name,email_id,contact):
		self.user_name=user_name
		self.email_id=email_id
		self.contact=contact


# cycles=[Cycle(model='hero Razor back',address='1102 MSA 1 ',dop='06/09/19',price='190',img='cycle2.jpg'),
# 		Cycle(model='hero Sprint',address='1201 MSA 2',dop='06/06/23',price='1000'),
# 		Cycle(model='atlas',address='1102 Malviya Bahvan',dop='06/06/23',price='2000'),
# 		Cycle(model='hercules',address='312 Ram Bhavan',dop='06/06/23',price='1000'),
# 		Cycle(model='hero Sprint',address='2321 Buddha Bhavan',dop='06/06/23',price='1000')
# 		]
img1="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(26).webp"
img2="https://mdbcdn.b-cdn.net/img/Photos/Avatars/img%20(23).webp"
cont="Suspendisse quos? Tempus cras iure temporibus? Eu laudantium cubilia sem sem! Repudiandae et! Massa senectus enim minim sociosqu delectus posuere."
reviews=[Review(cycle_id=1,content=cont,user_name='Ramesh',img_link=img1,date='06/06/23'),
		 Review(cycle_id=1,content=cont,user_name='Suresh',img_link=img2,date='01/12/23'),
		 Review(cycle_id=1,content="Good cycle. well maintained",user_name='Ramesh',img_link=img1,date='06/06/23'),
		 Review(cycle_id=1,content="Good cycle. well maintained",user_name='Suresh',img_link=img2,date='01/12/23')
		]





def index(request):
	#appUser=AppUser.objects.get(authUser=request.user)
	user=request.user
	cycles=Cycle.objects.filter(lend_or_sell='lend',is_avail=True)
	if user.is_authenticated:
		appUser=AppUser.objects.get(authUser=request.user)
		cycles=Cycle.objects.filter(lend_or_sell='lend',is_avail=True).exclude(owner=appUser).all()
	context = {
	'cycles': cycles,
  }
	if request.method=='POST':
		username=request.POST['username']
		password=request.POST['password']
		user=authenticate(request,username=username,password=password)
		if user!=None:
			login(request,user)
			messages.success(request,"You have been logged in!!!")

		else:
			messages.success(request,"There was an error logging in.Please try again")
			return redirect('/login')




	return render(request, "index.html",context=context)

def login_user(request):
   
	return render(request, "login.html")

def logout_user(request):
	logout(request)
	messages.success(request,"You have been logged out!!!")
	return render(request, "login.html")


def register_user(request):
	if request.method == 'POST':
		form = SignUpForm(request.POST)
		if form.is_valid():
			form.save()
			# Authenticate and login
			username = form.cleaned_data['username']
			password = form.cleaned_data['password1']
			user = authenticate(username=username, password=password)
			login(request, user)
			file_key=None
			for file_key in sorted(request.FILES):
				print(file_key)
				pass
			#wrapped_file = ImageFile(request.FILES[file_key])
			#filename = wrapped_file.name
			print(request.FILES)
			
			app_user = AppUser()
			app_user.authUser = user
			app_user.address=form.cleaned_data['address']
			app_user.phone=form.cleaned_data['phone']
			app_user.profile_img = request.FILES[file_key]
			app_user.save()

			messages.success(request, "You Have Successfully Registered! Welcome!")
			return redirect('/')
	else:
		form = SignUpForm()
		return render(request, 'register.html', {'form':form})

	return render(request, 'register.html', {'form':form})


def buy(request):
	user=request.user
	cycles=Cycle.objects.filter(lend_or_sell='sell',is_avail=True)
	if user.is_authenticated:
		appUser=AppUser.objects.get(authUser=request.user)
		cycles=Cycle.objects.filter(lend_or_sell='sell',is_avail=True).exclude(owner=appUser).all()
	context = {
	'cycles': cycles,
  }
	return render(request, "buy.html",context=context)


def sell(request):


	form = CycleForm
	if request.method == "POST":
		# form = CycleForm(request.POST, request.FILES)
		# if form.is_valid():
		#     cycle = form.save(commit=False)
		#     cycle.owner_id = request.user.id # logged in user
		#     cycle.save()
		# 	#form.save()
		#     return redirect('/')
		file_key=None
		for file_key in sorted(request.FILES):
			pass
		wrapped_file = ImageFile(request.FILES[file_key])
		filename = wrapped_file.name
		from .models import Cycle,AppUser
		cycle = Cycle()
		appUser=AppUser.objects.get(authUser=request.user)
		cycle.owner = appUser
		print(request.POST['lendorSell'])
		cycle.model=request.POST['bikeModel']
		cycle.lend_or_sell=request.POST['lendorSell']
		if cycle.lend_or_sell=="lend":
			cycle.is_avail=False
		cycle.dop=request.POST['dateOfPurchase']
		cycle.price=request.POST['Price']
		cycle.cycle_img = request.FILES[file_key]
		cycle.save()
		return redirect('/')


	# else:
	#     form = CycleForm


	return render(request, 'sell.html', {'form':form})
	#return render(request, "sell.html")

def reports(request):
	return render(request, "reports.html")

def history(request):
	return render(request, "history.html")

def shops(request):
	return render(request, "shops.html")


def details(request,id):
	context={"reviews":reviews}
	cycle=Cycle.objects.get(id=id)
	context["cycle"]=cycle
	if cycle.no_of_rents!=0:
		rating=int(cycle.total_stars/cycle.no_of_rents)
		rating_stars=[i for i in range(rating) ]
	else:
		rating_stars=[]
	context["rating"]=rating_stars
	# for cycle in cycles:
	# 	if cycle.id==id:
	# 		context["cycle"]=cycle
	return render(request, "details.html",context=context)

def rented_bikes(request):
	context={}
	if request.user.is_authenticated:
		appUser=AppUser.objects.filter(authUser=request.user)[0]
		rents=Rent.objects.filter(user=appUser,is_avail=True)
		if len(rents)!=0:
			current_dateTime = datetime.now()
			rent = rents[0]
			if rent.end_time.replace(tzinfo=None)<current_dateTime:
				rent.is_avail=False
				cycle=rent.cycle
				cycle.is_being_rented=False
				rent.save()
				cycle.save()
				print("Rent Duration Over")
			#owned_cycle=Cycle.objects.get(owner=appUser,lend_or_sell="sell")
			cycle_rented=rent.cycle
			context["cycle_rented"]=cycle_rented
	return render(request, "rented_bikes.html",context=context)

def owned_bikes(request):
	context={}
	if request.user.is_authenticated:
		appUser=AppUser.objects.get(authUser=request.user)
		owned_cycles=Cycle.objects.filter(owner=appUser,lend_or_sell="lend").all()
		cycles=[]
		for cycle in owned_cycles:
			cycle_data={"cycle_id":None,"cycle_model":None,"being_rented":None,"rentee_name":"NA"}
			cycle_data["cycle_id"]=cycle.id
			cycle_data["cycle_model"]=cycle.model
			if cycle.is_being_rented:
					rent=Rent.objects.get(cycle=cycle)
					current_dateTime = datetime.now()
					if rent.end_time.replace(tzinfo=None)<current_dateTime:
						rent.is_avail=False
						cycle_rented=rent.cycle
						cycle_rented.is_being_rented=False
						rent.save()
						cycle_rented.save()
					else:
						cycle_data["being_rented"]="Yes"
						cycle_data["rentee_name"]=rent.user.authUser.first_name
			cycles.append(cycle_data)



		#rent=Rent.objects.filter(user=appUser).all()
		# if len(rent)!=0:
		# 	rent=Rent.objects.get(user=appUser)
		# 	current_dateTime = datetime.now()
		# 	if rent.end_time.replace(tzinfo=None)<current_dateTime:
		# 		print("Rent Duration Over")
			
			#for c in own
		#cycle_rented=rent.cycle
		context["owned_cycles"]=cycles
	return render(request, "owned_bikes.html",context=context)

def checkout(request):
	data=request.POST
	print(data)
	cycle={"cycle_model":data["cycle_model"],
			 "cycle_price":int(data["cycle_price"])}
	cyc_id=data["cycle_id"]
	cycle=Cycle.objects.get(id=cyc_id)
	#user=User(user_name="Ramesh",email_id="gaurav.kumar@example.com",contact="9991232234")
	user=AppUser.objects.get(authUser=request.user)
	print(f"\n\n {user.phone} {user.authUser.first_name} {user.authUser.email}\n\n")
	client = razorpay.Client(auth=("rzp_test_hQHF0MU9H0s3HU", "4PJIN81Fhl66bGWTLmtkj2Ma"))

	payment_data = { "amount": int(data["cycle_price"])*100, "currency": "INR", "receipt": "order_rcptid_11" }
	payment = client.order.create(data=payment_data)

	orders[payment['id']]={"status":"payment requested","cycle_id":data["cycle_id"]}
	print(f"Orders are as follows\n {orders} \n and payment_data is is {payment}\n")
	context={"payment":payment,"cycle":cycle,"user":user}
	order=Order()
	order.user=user
	order.cycle=cycle
	order.razorpay_order_id=payment['id']
	order.payment_staus="payment requested"
	order.save()

	import json

	#print(context)
	return render(request, "checkout.html",context=context)

def lend(request):
	if request.user.is_authenticated:
		print(request.POST['cycle_id'])
		cycle=Cycle.objects.get(id=request.POST['cycle_id'])
		cycle.is_avail=True
		cycle.save()
		return redirect('/')


@csrf_exempt
def payments(request):
	print(request.POST)
	payments_details={'order_id': request.POST['razorpay_order_id'],
					  'payment_id': request.POST['razorpay_payment_id']
					  }
	payment=Payment()
	payment.razorpay_order_id=request.POST['razorpay_order_id']
	payment.razorpay_payment_id=request.POST['razorpay_payment_id']
	payment.razorpay_signature=request.POST['razorpay_signature']
	payment.save()
	order=Order.objects.get(razorpay_order_id=payment.razorpay_order_id)
	order.payment_staus="payment sucessful"
	order.save()
	

	current_dateTime = datetime.now()
	cycle=order.cycle
	rented_details=[]
	if cycle.lend_or_sell=="lend":
		rent=Rent()
		rent.user=AppUser.objects.get(authUser=request.user)
		rent.cycle=cycle
		rent.start_time=current_dateTime
		rent.payment=payment
		rent.end_time=current_dateTime+ timedelta(hours=2)
		rent.save()
		cycle.no_of_rents+=1
		cycle.is_being_rented=True
		rented_details.append(rent)
	
	cycle.is_avail=False
	
	cycle.save()
	cycle_id=orders[request.POST['razorpay_order_id']]['cycle_id']
	payments_details['cycle_id']=cycle_id
	context={"payments_details":payments_details,"rented_details":rented_details}
	return  render(request, "payments.html",context=context)
