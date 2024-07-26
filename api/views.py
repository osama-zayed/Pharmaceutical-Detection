from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import IntegrityError
from django.contrib.auth import authenticate
from rest_framework.response import Response
from django.core.files.storage import FileSystemStorage
from pages.models import Medication , Rating 
from django.contrib.auth import authenticate
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
import cv2
import numpy as np
from keras.models import load_model
import os
import uuid
from pyzbar.pyzbar import decode

@api_view(['POST'])
def login_view(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)

    if user is not None:
        token = Token.objects.create(user=user)    
        request.session['token'] = token
        request.session.save()

        return Response({'token': token})
    else:
        return Response({'message': 'فشل تسجيل الدخول'})  

@api_view(['POST'])
def create_account(request):
    username = request.data.get('username')
    password = request.data.get('password')
    confirm_password = request.data.get('confirm_password')
    email = request.data.get('email')

    if not username or not password or not confirm_password or not email:
        return Response({"Status": False, 'message': 'اسم المستخدم وكلمة المرور وتأكيد كلمة المرور والبريد الإلكتروني مطلوبة'})

    if password != confirm_password:
        return Response({"Status": False, 'message': 'كلمة المرور وتأكيد كلمة المرور غير متطابقتين'})

    try:
        validate_email(email)
    except ValidationError:
        return Response({"Status": False, 'message': 'عنوان البريد الإلكتروني غير صحيح'})

    try:
        user = User.objects.create_user(username=username, password=password, email=email)

        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({"Status": True, 'message': 'تم إنشاء الحساب بنجاح', 'token': token.key})
        else:
            return Response({"Status": False, 'message': 'فشل في المصادقة'})

    except IntegrityError:
        return Response({"Status": False, 'message': 'اسم المستخدم موجود بالفعل'})
    except Exception as e:
        return Response({"Status": False, 'message': str(e)})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    data = {
        'username': user.username,
        'email': user.email,
    }
    return Response({"Status": True, 'message': 'بيانات المستخدم المسجل دخوله', 'data': data})

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    token = Token.objects.get(user=request.user)
    token.delete()
    return Response({"Status": True, 'message': 'تم تسجيل الخروج بنجاح'})    



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def check(request):
    try:
        # image = request.FILES.get('file')
        images = request.FILES.getlist('Images')  # استقبال قائمة من الصور
    
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
                message = 'الختم موجود المنتج اصلي'
                
            elif max_value < 0.2:
                message = 'المنتج مهرب لايوجد ختم'
                
            else :
                message = 'حالة المنتج غير معروفة'
                
            base_url = request.build_absolute_uri('/')
            image_url = base_url + 'api/' + filename  
            print("max_value" + str(max_value))              
            data = {
                    "Status": True,
                    'name': name,
                    'category': category,
                    'image_path':image_url,
                    'message': message,
                    }
            return Response(data) 
        else:
            raise ValueError('لا يوجد قائمة من الصور في الطلب')
    except Exception as e:
        data = {
            "Status": False,
            'error': str(e)
        }
        return Response(data)
  
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def add_rating(request): 
    stars = request.data.get('stars')
    comment = request.data.get('comment')
    try:
        stars = int(stars)
        if stars < 1 or stars > 5:
            raise ValueError("Invalid stars value")
    except (ValueError, TypeError):
        data = {
            "Status": False, 
            'message': 'قيمة التقييم غير صحيحة.'
        }
        return Response(data)
    
    try:                                
        rating = Rating(stars=stars, comment=comment,user = request.user)
        rating.save()
        data = {
            "Status": True, 
            'message': 'تمت العملية بنجاح!'
        }
        return Response(data)        
    except Exception as e:
        data = {
            "Status": False, 
            'message': 'حدث خطأ أثناء إضافة التقييم.'
        }
        return Response(data)

def read_qr_code(image_path):
    image = cv2.imread(image_path)
    decoded_objects = decode(image)
    if len(decoded_objects) > 0:
        qr_code_data = decoded_objects[0].data.decode("utf-8")
        return qr_code_data
    else:
        return None
    
def Pharmaceutical_Detection(image_path):
    model_path = os.path.join(os.path.dirname(__file__), 'pharmaceutical_detection_model.h5')
    model = load_model(model_path)
    image = cv2.imread(image_path)
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image_size = (224, 224)
    resized_image = cv2.resize(gray_image, image_size)
    input_image = np.expand_dims(resized_image, axis=-1)  
    input_image = np.repeat(input_image, 3, axis=-1)  
    prediction = model.predict(np.expand_dims(input_image, axis=0))
    return prediction[0][0]