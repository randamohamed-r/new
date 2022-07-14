
#from tensorflow.python import tf2
from fileinput import filename
import numpy as np
from keras.models import load_model
import tensorflow as tf
from keras.utils import np_utils 
#import Dapi1
from .models_api import *
from keras.preprocessing import image




def prepare(img_path):
    img = tf.keras.utils.load_img(img_path, target_size=(256, 256))
    print(img)
    x = tf.keras.utils.img_to_array(img)
    x = x/255
    return np.expand_dims(x, axis=0)
    
disease_class=['جرب التفاح',
   'العفن الأسود في التفاح',
   'صدأ  التفاح  والأرز',
   'البياض الدقيقي على الكرز',
   'تبقع الأوراق الرمادي في الذرة',
   'صدأ الذرة الشائع',
   'اللفحة الورقية الشمالية في الذرة',
   'عفن العنب الأسود',
   'مرض الإسكا ( الحصبة السوداء) في العنب',
   'لا يوجد معلومات',
   'إخضرار الحمضيات في البرتقال',
   'التبقع البكتيري في الخوخ ',
   'التبقع البكتيري على الفلفل',
   'اللفحة المبكرة في البطاطس',
   'اللفحة المتأخرة في البطاطس',
   'البياض الدقيقي على الكوسة',
   'احتراق الأوراق الزاوي في الفراولة',
   'التبقع البكتيري في الطماطم',
   'اللفحة المبكرة في الطماطم',
   'اللفحة المتأخرة في الطماطم',
   'تعفن أوراق الطماطم',
   'التبقع السبتوري للأوراق في الطماطم',
   'العنكبوت (الاكاروس) في الطماطم',
   'بقعة الهدف في الطماطم ( Tomato Target Spot )',
   'فيروس تجعد واصفرار اوراق الطماطم',
   'فيروس فسيفساء الطماطم',
]

fruit_class= ['الفول',
  'البروكلي',
  'الكرنب',
  'الجزر',
  'القرنبيط',
  'الخيار',
  'لم يتم العثور على ناتج',
  'الفلفل',
  'البطاطس',
  'الفجل',
  'الطماطم',
  'الاقحوان',
  'الهندباء',
  'التفاح',
  'الموز',
  'البرتقال',
  'دوار الشمس']

healthy_class=['التفاح',
 'التوت البري',
 'الكرز',
 'الذره',
 'العنب',
 'لم يتم الحصول على ناتج',
 'الخوخ',
 'الفلفل',
 'البطاطس',
 'توت العليق',
 'فول الصويا',
 'الفراولة',
 'الطماطم']

def disease_model(image):
    model=load_model('model_diseases.h5')
    
    result = model.predict([prepare(image)])  ##هنا بحط باث الصوره
    p=np.amax(result)
    if p < 0.95:
        output= 'لم يتم الحصول على ناتج'
    else:
        output= disease_class[np.argmax(result)]
        return(output)
#################################################

def fruit_model(image):
    model=load_model('model_fruits.h5')
    
    result = model.predict([prepare(image)])  ##هنا بحط باث الصوره
    p=np.amax(result)
    if p < 0.95:
        output= 'لم يتم الحصول على ناتج'
    else:
        output= fruit_class[np.argmax(result)]
        return(output)
#################################################

"""def healthy_model(image):
    model=load_model('model_healthy(3).h5')
   
    result = model.predict([prepare(image)])  ##هنا بحط باث الصوره
    p=np.amax(result)
    if p < 0.95:
        output= 'لم يتم الحصول على ناتج'
    else:
        output= healthy_class[np.argmax(result)]
        return(output)
"""
 




#result = 
#disease('some_image.jpg')
#print(result)