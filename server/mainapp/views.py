from django.http.response import JsonResponse
from rest_framework.views import APIView

from .utils import recv_music_data, send_music_data, send_profile_data
from core.throttle import throttle


class Uploads(APIView):
    throttle_classes = [throttle]

    def post(self, request, **kwargs) -> JsonResponse:
        """Receiving user uploaded data via POST requests

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Receiving Data API")

        data = recv_music_data(request, **kwargs)

        return data


class Posts(APIView):
    throttle_classes = [throttle]

    def get(self, request, **kwargs) -> JsonResponse:
        """Sending user data when hit with GET requests

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Sending Data API")

        data = send_music_data(request, **kwargs)

        return data


class Profile(APIView):
    throttle_classes = [throttle]

    def get(self, request, **kwargs):
        """Sending specific user data when hit with GET requests

        Args:
            request ([type])

        Returns:
            JsonResponse
        """

        print("Sending Profile Data API")

        data = send_profile_data(request, **kwargs)

        return data
