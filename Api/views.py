from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from .serializers import UsersSerializer
from .models import Users
import google.generativeai as genai
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class UsersViewSet(viewsets.ViewSet):
    def create(self, request):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'msg' : 'Data has been created',
                'status' : True
                })
        return Response({
            'msg' : serializer.errors,
            'status' : False
        }) 

    def list(self, request):
        queryset = Users.objects.all()
        serializer = UsersSerializer(queryset, many = True)
        return Response({
            "msg":serializer.data,
            "status":True
            })       


class AI_ChatbootViewSet(viewsets.ViewSet):
    def create(self, request):
        try:
            message = request.data.get("message")

            if not message:
                return Response({"error": "message required"})

            # 🔑 Gemini API key
            genai.configure(api_key="Enter your api key") #Hide my api 

            models = genai.list_models()

            for m in models:
                print(m.name)

        
            model = genai.GenerativeModel("gemini-2.5-flash")

            # AI response
            response = model.generate_content(message)

            return Response({
                "reply": response.text
            })

        except Exception as e:
            return Response({
                "error": str(e)
            })          
