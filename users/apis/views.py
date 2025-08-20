from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.apis.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from users.models import User


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.username != 'elta':
            return Response({"detail": "No tienes permisos para registrar usuarios."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyTokenView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        auth = JWTAuthentication()
        try:
            validated_token = auth.get_validated_token(request.headers.get('Authorization').split()[1])
            user = auth.get_user(validated_token)
            return Response({'detail': 'Token válido', 'user': user.username}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_403_FORBIDDEN)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('id')
        all_users = request.query_params.get('all_users')

        if user_id:
            if request.user.username != 'elta':
                return Response({"detail": "No tienes permisos para ver otros usuarios."}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        elif all_users:
            if request.user.username != 'elta':
                return Response({"detail": "No tienes permisos para ver todos los usuarios."}, status=status.HTTP_403_FORBIDDEN)
            users = User.objects.filter(is_superuser=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        else:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

    def put(self, request):
        user_id = request.data.get('id')
        
        if user_id:
            if request.user.username != 'elta':
                return Response({"detail": "No tienes permisos para actualizar otros usuarios."}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(id=user_id)
                serializer = UserUpdateSerializer(user, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    return Response(serializer.data)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = User.objects.get(id=request.user.id)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.user.username != 'elta':
            return Response({"detail": "No tienes permisos para actualizar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        updates = request.data  # Se espera una lista de objetos con id y campos a actualizar
        if not isinstance(updates, list):
            return Response({"detail": "Se espera una lista de usuarios a actualizar."}, status=status.HTTP_400_BAD_REQUEST)

        resultados = []
        for item in updates:
            user_id = item.get("id")
            if not user_id:
                resultados.append({"id": None, "status": "Faltó el ID"})
                continue

            try:
                user = User.objects.get(id=user_id, is_superuser=False)
                serializer = UserUpdateSerializer(user, data=item, partial=True)
                if serializer.is_valid():
                    serializer.save()
                    resultados.append({"id": user_id, "status": "Actualizado"})
                else:
                    resultados.append({"id": user_id, "status": "Error de validación", "errors": serializer.errors})
            except User.DoesNotExist:
                resultados.append({"id": user_id, "status": "No encontrado"})

        return Response(resultados, status=status.HTTP_200_OK)
