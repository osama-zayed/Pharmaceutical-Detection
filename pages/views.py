from django.shortcuts import render,redirect,get_object_or_404
from django.core.files.storage import FileSystemStorage
import cv2
from pyzbar.pyzbar import decode
from django.shortcuts import render

from api.views import Pharmaceutical_Detection
from .models import Medication
from .models import Rating
from . import models
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User
from django.shortcuts import redirect, get_object_or_404
from PIL import Image
import uuid

def is_admin(user):
    return user.is_authenticated and user.is_superuser
def is_authenticated(user):
    return user.is_authenticated

def index(request):
    return render(request,'pages/home.html')

def about_us(request):
    return render(request,'pages/about_us.html')

@user_passes_test(is_authenticated)
def start(request):
    rating = models.Rating.objects.all()
    return render(request,'pages/start.html',{'rating':rating})

def Review(request):
    rating = models.Rating.objects.all()
    return render(request,'pages/Review.html', {'ratings': rating})

# ////////////////////////////////////////
@user_passes_test(is_admin)
def showUser(request):
    users = User.objects.all()
    return render(request,'pages/User/showUser.html', {'users': users})


def toggle_user_activation(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.is_active = not user.is_active
    user.save()
    messages.success(request, 'تم تغيير حالة المستخدم بنجاح')
    return redirect(request.META.get('HTTP_REFERER'))

#Drugs ////////////////////
@user_passes_test(is_admin)
def Drugs(request):
    medications = models.Medication.objects.all()
    return render(request,'pages/Drugs/index.html', {'medications': medications})

@user_passes_test(is_admin)
def AddDrugs(request):
    Categorys = models.Category.objects.all()
    return render(request,'pages/Drugs/AddDrugs.html', {'Categorys': Categorys})

@user_passes_test(is_admin)
def add_drugs(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            drug_type = request.POST.get('model-select')
            file = request.FILES['file']
            fs = FileSystemStorage() 
            filename = fs.save(file.name, file)
            image_path = fs.path(filename)
            qr_code_data = read_qr_code(image_path)
            category_id = request.POST.get('category')
            category = get_object_or_404(models.Category, id=category_id)
            medication = Medication(name=name, type=drug_type, qr_code=qr_code_data, category=category,image=image_path)
            medication.save()
            
            messages.success(request, 'تمت العملية بنجاح!')
            return redirect(Drugs)  

        except Exception as e:
            messages.error(request, 'العملية فشلت')
            return  redirect(request.META.get('HTTP_REFERER'))   
    messages.error(request, 'العملية فشلت')
    return redirect(request.META.get('HTTP_REFERER'))

@user_passes_test(is_admin)
def delete_medication(request, medication_id):
    try:
        medication = get_object_or_404(Medication, pk=medication_id)
        medication.delete()
        messages.success(request, 'تمت العملية بنجاح!')
        return redirect(Drugs) 
    except print(0):
        messages.error(request, 'العملية فشلت')
        return  redirect(request.META.get('HTTP_REFERER'))   

#End Drugs ////////////////////
#Category ////////////////////
@user_passes_test(is_admin)
def Category(request):
    Categorys = models.Category.objects.all()
    return render(request,'pages/Category/index.html', {'Categorys': Categorys})

@user_passes_test(is_admin)
def AddCategory(request):
    return render(request,'pages/Category/AddCategory.html')

@user_passes_test(is_admin)
def add_Category(request):
    if request.method == 'POST':
        try:
            name = request.POST.get('name')           
            medication = models.Category(name=name)
            medication.save()
            messages.success(request, 'تمت العملية بنجاح!')
            return redirect(Category)  
        except Exception as e:
            messages.error(request, 'العملية فشلت')
            return  redirect(request.META.get('HTTP_REFERER'))   
    messages.error(request, 'العملية فشلت')
    return redirect(request.META.get('HTTP_REFERER')) 

@user_passes_test(is_admin)
def delete_Category(request, Category_id):
    try:
        Categorys = get_object_or_404(models.Category, pk=Category_id)
        Categorys.delete()
        messages.success(request, 'تمت العملية بنجاح!')
        return redirect(Category) 
    except print(0):
        messages.error(request, 'العملية فشلت')
        return  redirect(request.META.get('HTTP_REFERER'))   

#End Category ////////////////////

def add_rating(request): 
    if request.method == 'POST':
        if request.user.is_authenticated:
            stars = request.POST.get('stars')
            comment = request.POST.get('comment')
            try:
                stars = int(stars)
                if stars < 1 or stars > 5:
                    raise ValueError("Invalid stars value")
            except (ValueError, TypeError):
                messages.error(request, 'قيمة التقييم غير صحيحة.')
                return redirect(request.META.get('HTTP_REFERER'))
            try:                                
                rating = Rating(stars=stars, comment=comment,user=request.user)
                rating.save()
               
            except Exception as e:
                messages.error(request, 'حدث خطأ أثناء إضافة التقييم.')
                return redirect(request.META.get('HTTP_REFERER'))

            messages.success(request, 'تمت العملية بنجاح!')
            return redirect('start')  
        messages.error(request, 'يجب أن يكون المستخدم مسجل الدخول لإضافة تقييم.')
        return redirect(index)

    messages.error(request, 'حدث خطأ أثناء إضافة التقييم.')
    return redirect(request.META.get('HTTP_REFERER'))

# def qrcode_view(request):
#     try:
#         if request.method == 'POST':
#                 file = request.FILES['file']
#                 try:
#                     image = Image.open(file)
#                     if image.format.lower() in ['jpeg', 'png', 'gif']:
#                         fs = FileSystemStorage()
#                         filename = fs.save(file.name, file)
#                         image_path = fs.path(filename)
#                         base_url = request.build_absolute_uri('/')                        
#                         image_url = base_url + 'api/' + filename 
#                         qr_code_data = read_qr_code(image_path)
#                         if qr_code_data is not None:
#                             try:
#                                 medications = Medication.objects.filter(qr_code=qr_code_data)
#                                 if medications.exists():
#                                     medication = medications.first()
#                                     if medication.type == 'أصلي':
#                                         message = 'المنتج أصلي'
#                                     elif medication.type == 'تهريب':
#                                         message = 'المنتج مهرب'
#                                     else:
#                                         message = 'حالة غير معروفة'
#                                     return render(request, 'pages/result.html', {'name': medication.name, 'category': medication.category.name, 'message': message , 'image_path': image_url})
#                                 else:
#                                     message = 'المنتج مهرب'
#                                     return render(request, 'pages/result.html', {'name': "غير معروف", 'category':  "غير معروف", 'message': message , 'image_path': image_url})
#                             except Medication.DoesNotExist:
#                                 message = 'المنتج مهرب'
#                                 return render(request, 'pages/result.html', {'name':  "غير معروف", 'category':  "غير معروف", 'message': message , 'image_path': image_url})
#                         else:
#                             messages.error(request, 'العملية فشلت')
#                             return redirect(request.META.get('HTTP_REFERER'))
#                     else:
#                         messages.error(request, 'الملف المرسل ليس صورة')
#                         return redirect(request.META.get('HTTP_REFERER'))
#                 except OSError:
#                     messages.error(request, 'الملف المرسل ليس صورة صحيحة')
#                     return redirect(request.META.get('HTTP_REFERER'))
#             else:
#                 raise ValueError('لا يوجد ملف في الطلب')
#         else:
#             raise ValueError('طريقة الطلب غير مدعومة')
#     except Exception as e:
#         messages.error(request, str(e))
#         return redirect(request.META.get('HTTP_REFERER'))

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    decoded_objects = decode(image)

    if len(decoded_objects) > 0:
        qr_code_data = decoded_objects[0].data.decode("utf-8")
        return qr_code_data
    else:
        return None
    
    
def check(request):
    try:
        if request.method == 'POST':
            if 'Images' in request.FILES:                   
                images = request.FILES.getlist('Images')  # استقبال قائمة من الصور
                if len(images) == 6:
                    if images:
                        predictions = []
                        qr_codes = None
                        category = 'غير معرف'
                        name = "غير معرف"
                        message = ''
                        image_path =''
                        for image in images:                
                            file_type = image.content_type
                            if file_type.startswith('image/'):
                                fs = FileSystemStorage()
                                unique_filename = f"{uuid.uuid4().hex}.{image.name.split('.')[-1]}"
                                filename = fs.save(unique_filename, image)
                                image_path = fs.path(filename)
                                prediction = Pharmaceutical_Detection(image_path)
                                qr_code_data = read_qr_code(image_path)                    
                                predictions.append(prediction)
                                qr_codes = qr_code_data if qr_code_data else qr_codes
                            else:
                                raise ValueError('الملف المرسل ليس صورة')

                        medications = Medication.objects.filter(qr_code=qr_codes)
                        max_value = max(predictions)
                        if medications.exists():
                            medication = medications.first()
                            if medication.type == 'أصلي':
                                message = 'المنتج أصلي'
                            elif medication.type == 'تهريب':
                                message = 'المنتج مهرب'                    
                            category = medication.category.name
                            name = medication.name

                        elif max_value > 0.6:
                            message = 'المنتج أصلي'

                        elif max_value < 0.2:
                            message = 'المنتج مهرب'

                        else :
                            message = 'حالة المنتج غير معروفة'

                        base_url = request.build_absolute_uri('/')
                        image_url = base_url + 'api/' + filename  
                        print("max_value" + str(max_value))              
                        return render(request, 'pages/result.html', {
                                'name': name,
                                'category': category,
                                'image_path':image_url,
                                'message': message,
                                })
                else:
                    raise ValueError("عدد الصور يجب ان يكون 6")                
            else:
                raise ValueError("لا يوجد ملف في الطلب")       
        else:
            raise ValueError('طريقه الطلب غير صحيحة')    
    except Exception as e:
        messages.error(request, str(e))
        return redirect(request.META.get('HTTP_REFERER'))
  
    
