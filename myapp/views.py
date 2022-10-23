from django.shortcuts import render
from .forms import ImageForm
from .models import Image
import os
from tokenize import String
import cv2
import easyocr
# from DataPreprocessing import DataPProcess
import re
import cohere
from cohere.classify import Example


def DataPProcess(data):
    data = re.sub(r'https?://[^ ]+', '', data)
    data = re.sub(' +', ' ', data)

    data = re.sub(r'@[^ ]+', '', data)

    data = re.sub(r'#', '', data) 

    data = re.sub(r'([A-Za-z])\1{2,}', r'\1', data)

    data = re.sub(r' 0 ', 'zero', data)
    data = re.sub(r'[^A-Za-z ]', '', data)

    data = data.lower() #Lower casing
    # tokens = word_tokenize(data)
    # for token in tokens: 
    #     if token in stopwords.words('english'):
    #         tokens.remove(token)
    # print(tokens)
    return data

def identify(testtxt):
    # testtxt = "life is like riding a bicycle to keep your balance you must keep moving albert einstein"
    co = cohere.Client('SWNcF7UPyIJhRbZYT6IQsgpySycWUQ0Wj2JnmEsH')
    response = co.classify(
    model='66c45e0f-9156-4f63-a7a4-419d1ca6658e-ft',
    inputs=[testtxt])
    max_lable=""
    max_confidence = 0
    for i in response.classifications[0].confidence:
        if i.confidence >= max_confidence:
            max_lable = i.label
            max_confidence = i.confidence
    return max_lable,max_confidence

reader = easyocr.Reader(['en'])

def main(img):
    output_list = reader.readtext(img)
    output_text = ""
    for i in output_list:
        output_text = output_text +" "+ i[1]
    text = DataPProcess(output_text)
    result_lable,result_confidence = identify(text)
    os.system('cls')
    print(f"Content: {text}")
    print(f"Category: {result_lable}")
    output = {"content":text,"category":result_lable}
    return output

# main("test01.png")


def home(request):
 img = Image.objects.all()
 count=0
 for i in img:
    count = count+1
 if count>0:
    img.delete()
    for directory, subdirectory,filenames in os.walk("media/myimage"):
        for filename in filenames:
            target = directory +"/"+ filename
            os.remove(target)  
 if request.method == "POST":
  form = ImageForm(request.POST, request.FILES)
  if form.is_valid():
   form.save()
#    img = Image.objects.all()

 form = ImageForm()
 target = ""
 context = dict()
 context["content"] = ""
 context["category"] = ""
 for directory, subdirectory,filenames in os.walk("media/myimage"):
  for filename in filenames:
    target = directory +"/"+ filename
    img = Image.objects.all()
    context = main(target)
    # os.remove(target)
 

 return render(request, 'myapp/home.html',{'form':form,"content":context["content"],"category":context["category"],"img":img})