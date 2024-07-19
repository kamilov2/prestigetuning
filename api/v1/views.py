from django.shortcuts import redirect
from rest_framework.views import APIView


class HomePageAPIView(APIView):
    def get(self, request):
        return redirect('')


