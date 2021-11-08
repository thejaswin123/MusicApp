from rest_framework import status
from django.http import response

from .errors import InvalidUserCredentialsError, UserDoesNotExistError, UserExistsError
from . import Token_Auth, User_Auth


def register_user(request, **kwargs) -> response.JsonResponse:
    """Handles data when user registers through POST requests

    Args:
        request
        **kwargs

    Returns:
        response.JsonResponse
    """
    try:
        print("POST REQUEST REGISTER")
        print("Request Object DATA:", request.data)

        name = request.data.get("Name")
        email = request.data.get("Email")
        password = request.data.get("Password")

        print(name, email, password)

        User_Auth.insert_user(name, email, password)
        uid = User_Auth.get_uid(email)
        payload = {"id": uid}

        token = Token_Auth.generate_token(
            payload=payload, expiry=1, get_refresh=True, refresh_exipry=12
        )
        return response.JsonResponse(
            data={
                "access_token": token["access_token"],
                "refresh_token": token["refresh_token"],
            },
            status=status.HTTP_200_OK,
        )

    except UserExistsError as uee:
        return response.JsonResponse(
            {"error": str(uee), "auth_status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except UserDoesNotExistError as udne:
        return response.JsonResponse(
            {"error": str(udne), "auth_status": False},
            status=status.HTTP_404_NOT_FOUND,
        )
    except Exception as e:
        print(e)
        return response.JsonResponse(
            {
                "error": "Error Occured While Receiving Registration Data",
                "auth_status": False,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def login_user(request, **kwargs) -> response.JsonResponse:
    """Handles data when user Logs In through POST requests

    Args:
        request
        **kwargs

    Returns:
        response.JsonResponse
    """
    try:
        print("POST REQUEST LOGIN")
        print("Request Object DATA:", request.data)

        email = request.data.get("Email")
        password = request.data.get("Password")

        print(email, password)

        if User_Auth.check_hash(email, password):
            uid = User_Auth.get_uid(email)
            payload = {"id": uid}

            token = Token_Auth.generate_token(
                payload=payload, expiry=1, get_refresh=True, refresh_exipry=12
            )
            return response.JsonResponse(
                data={
                    "access_token": token["access_token"],
                    "refresh_token": token["refresh_token"],
                },
                status=status.HTTP_200_OK,
            )

    except UserDoesNotExistError as udne:
        return response.JsonResponse(
            {"error": str(udne), "auth_status": False},
            status=status.HTTP_404_NOT_FOUND,
        )
    except InvalidUserCredentialsError as ice:
        return response.JsonResponse(
            {"error": str(ice), "auth_status": False},
            status=status.HTTP_400_BAD_REQUEST,
        )
    except Exception as e:
        print(e)
        return response.JsonResponse(
            {
                "error": "Error Occured While Receiving Registration Data",
                "auth_status": False,
            },
            status=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


def reset_pwd(request, **kwargs) -> response.JsonResponse:
    """Handles data when user resets password through POST requests

    Args:
        request
        **kwargs

    Returns:
        response.JsonResponse
    """
    print("POST REQUEST RESET PASSWORD")
    print("Request Object DATA:", request.data)
