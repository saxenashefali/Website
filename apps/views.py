from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from docType.docType import detect_class
from rest_framework.renderers import TemplateHTMLRenderer
from django.shortcuts import get_object_or_404
from apps.forms import docTypeForm
import re
from bs4 import BeautifulSoup
import string
from django.http import JsonResponse

class docTypeView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'doctype.html'

    def clean_text(self, text):
        sentence = text.lower()
            
        # remove emails
        sentence = re.sub(r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", '', sentence)

        # remove mentions
        sentence = re.sub(r"@[A-Za-z0-9]+","", sentence)
        
        # Remove html
        sentence = BeautifulSoup(sentence, 'lxml').get_text().strip()
        
        # Remove URL
        sentence = re.sub(r'https?://\S+|www\.\S+', '', sentence)
            
        # Removing punctutation, string.punctuation in python consists of !"#$%&\'()*+,-./:;<=>?@[\\]^_
        sentence = sentence.translate(str.maketrans('', '', string.punctuation))
        
        # Remove non-alphabetic characters
        sentence = re.sub(r'[^a-zA-Z ]', '', sentence)

        return sentence

    def get(self, request):
        form = docTypeForm()
        print(form.as_p())
        return Response({'form': form, 'button': 'true'})

    def post(self, request):
        text = self.clean_text(request.data["text"])
        
        if 'api' in request.data:
            return Response({'class':detect_class(text)})
        return JsonResponse({'class':detect_class(text)})