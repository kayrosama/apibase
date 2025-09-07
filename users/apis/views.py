from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication

from core_auth.permissions import IsZetaRoleOrReadOnly
from core_auth.decorators import role_permission, rate_limit_log 
from users.apis.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from core_auth.models import User


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]

    @rate_limit_log(key='ip', rate='5/m', block=True)
    @role_permission(required_roles=['admin'], allow_self=False)
    def post(self, request):
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
            return Response({'detail': 'Token válido', 'email': user.email}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': 'Token inválido o expirado'}, status=status.HTTP_403_FORBIDDEN)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('id')
        all_users = request.query_params.get('all_users')

        if user_id:
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                return Response(serializer.data)
            except User.DoesNotExist:
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        elif all_users:
            users = User.objects.filter(is_superuser=False)
            serializer = UserSerializer(users, many=True)
            return Response(serializer.data)

        else:
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

    @rate_limit_log(key='ip', rate='5/m', block=True)
    @role_permission(required_roles=['admin', 'sysoper'], allow_self=False, restrict_role_change=True)
    def put(self, request):
        user_id = request.data.get('id')

        if user_id:
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

    @rate_limit_log(key='ip', rate='5/m', block=True)
    @role_permission(required_roles=['admin', 'sysoper'], allow_self=False, restrict_role_change=True)
    def patch(self, request):
        updates = request.data  # Se espera una lista de objetos con id y campos a actualizar
        if not isinstance(updates, list):
            return Response({"detail": "Se espera una lista de usuarios a actualizar."}, status=status.HTTP_400_BAD_REQUEST)

        resultados = []
        for item in updates:
            user_id = item.get("id")
            if not user_id:
                resultados.append({"id": None, "status": "Faltó el ID"})
                continue

            # Validación para evitar que el admin modifique su propio rol
            if str(request.user.id) == str(user_id) and 'role' in item:
                resultados.append({"id": user_id, "status": "No puedes modificar tu propio rol"})
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
