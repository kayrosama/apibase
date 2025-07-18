import logging
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from users.apis.serializers import UserRegisterSerializer, UserSerializer, UserUpdateSerializer
from users.models import User

logger = logging.getLogger('user_apis_view')


class RegisterView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.username != 'elta':
            logger.warning(f"RegisterView_post :: {request.user.username} :: Authorized :: No tienes permisos para registrar usuarios.")
            return Response({"detail": "No tienes permisos para registrar usuarios."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            logger.info(f"RegisterView_post :: {request.user.username} :: Authorized :: Usuario registrado con exito.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"RegisterView_post :: {request.user.username} :: errores de validacion :: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user_id = request.query_params.get('id')
        all_users = request.query_params.get('all_users')

        if user_id:
            if request.user.username != 'elta':
                logger.warning(f"xxx :: {request.user.username} :: Unauthorized :: No tienes permisos para ver informacion de otros usuarios.")
                return Response({"detail": "No tienes permisos para ver otros usuarios."}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(id=user_id)
                serializer = UserSerializer(user)
                logger.info(f"xxx :: {request.user.username} :: Authorized :: Obtiene informacion del usuario con ID {user_id}")
                return Response(serializer.data)
            except User.DoesNotExist:
                logger.error(f"xxx :: {request.user.username} :: Authorized :: Usuario con ID {user_id} no encontrado")
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)

        elif all_users:
            if request.user.username != 'elta':
                logger.warning(f"xxx :: {request.user.username} :: Unauthorized :: No tienes permisos para ver informacion de todos los usuarios.")
                return Response({"detail": "No tienes permisos para ver todos los usuarios."}, status=status.HTTP_403_FORBIDDEN)
            users = User.objects.filter(is_superuser=False)
            serializer = UserSerializer(users, many=True)
            logger.info(f"xxx :: {request.user.username} :: Authorized :: Obtiene informacion de todos los usuarios.")
            return Response(serializer.data)

        else:
            serializer = UserSerializer(request.user)
            logger.info(f"xxx :: {request.user.username} :: Authorized :: Obtiene su propia informaicon.")
            return Response(serializer.data)

    def put(self, request):
        user_id = request.data.get('id')
        
        if user_id:
            if request.user.username != 'elta':
                logger.warning(f"UserView_put :: {request.user.username} :: Unauthorized :: No tienes permisos para actualizar otros usuarios.")
                return Response({"detail": "No tienes permisos para actualizar otros usuarios."}, status=status.HTTP_403_FORBIDDEN)
            try:
                user = User.objects.get(id=user_id)
                serializer = UserUpdateSerializer(user, data=request.data, partial=True)
                if serializer.is_valid(raise_exception=True):
                    serializer.save()
                    logger.info(f"UserView_put :: {request.user.username} :: Authorized :: Actualizo la informacion del usuario con ID {user_id}")
                    return Response(serializer.data)
                logger.error(f"UserView_put :: {request.user.username} :: Authorized :: Errores de validación al actualizar la informacion del usuario con ID {user_id}: {serializer.errors}")
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            except User.DoesNotExist:
                logger.error(f"UserView_put :: {request.user.username} :: Authorized :: Usuario con ID {user_id} no encontrado")
                return Response({"detail": "Usuario no encontrado."}, status=status.HTTP_404_NOT_FOUND)
        else:
            user = User.objects.get(id=request.user.id)
            serializer = UserUpdateSerializer(user, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                logger.info(f"UserView_put :: {request.user.username} :: Authorized :: Actualizo su propio perfil")
                return Response(serializer.data)
            logger.error(f"UserView_put :: {request.user.username} :: Authorized :: Errores de validacion al actualizar su propio perfil: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        if request.user.username != 'elta':
            logger.warning(f"UserView_patch :: {request.user.username} :: Unauthorized :: No tienes permisos para actualizar la informacion de los usuarios.")
            return Response({"detail": "No tienes permisos para actualizar usuarios."}, status=status.HTTP_403_FORBIDDEN)

        updates = request.data  # Se espera una lista de objetos con id y campos a actualizar
        if not isinstance(updates, list):
            logger.error(f"UserView_patch :: {request.user.username} :: Authorized :: Se espera una losta de usuarios a actualizar.")
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
