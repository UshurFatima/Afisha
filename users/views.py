from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from .serializers import (UserCreateSerializer, UserAuthSerializer,
                          ConfirmCodeSerializer)
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import ConfirmCode
from random import choices
import smtplib
import string


@api_view(['POST'])
def authorization_api_view(request):
    serializer = UserAuthSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user = authenticate(**serializer.validated_data)
    if user and user.is_active:
        token, _ = Token.objects.get_or_create(user=user)
        return Response(data={'key': token.key})

    return Response(status=status.HTTP_401_UNAUTHORIZED,
                    data={'error': 'User credentials are wrong'})


# create function confirm_api_view (принимает код и проверяет его,
# меняет is_active на тру)
@api_view(['POST'])
def confirm_api_view(request):
    serializer = ConfirmCodeSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    user_id = serializer.validated_data['user_id']
    code = serializer.validated_data['code']
    db = ConfirmCode.objects.get(user_id=user_id)
    db_code = db.code

    if code == db_code:
        user = db.user
        user.is_active = True
        user.save()
        return Response(status=status.HTTP_200_OK,
                        data={'message': 'User was activated successfully'})
    return Response(status=status.HTTP_400_BAD_REQUEST,
                    data={'error': 'The code is incorrect'})


@api_view(['POST'])
def registration_api_view(request):
    serializer = UserCreateSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    password = serializer.validated_data['password']

    user = User.objects.create_user(username=username, email=email,
                                    password=password, is_active=False)

    # Create code (6-symbol)
    code = ''.join(choices(string.digits + string.ascii_letters, k=6))
    ConfirmCode.objects.create(user_id=user.id, code=code)
    print(code)

    try:
        smtp = smtplib.SMTP('smtp.gmail.com', 587)

        smtp.starttls()

        smtp.login("fatimaconfirmcode@gmail.com", "fatimadadakamama_007")

        message = code

        smtp.sendmail(from_addr="fatimaconfirmcode@gmail.com", to_addrs=user.email, msg=message)

        smtp.quit()
        print("Email sent successfully!")

    except Exception as ex:
        print("Something went wrong....", ex)

    return Response(status=status.HTTP_201_CREATED,
                    data={'user_id': user.id})
