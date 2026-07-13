# views.py (zaktualizowane z DRF i serializerami)
from rest_framework import generics, status
from rest_framework.views import APIView
from collections import Counter
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import get_authorization_header
from firebase_admin import auth as firebase_auth
from django.shortcuts import get_object_or_404
import requests
from django.http import JsonResponse
from google.cloud import aiplatform
import urllib.parse
from rest_framework.exceptions import ValidationError
from rest_framework import permissions
import logging
from decimal import Decimal
from collections import Counter

logger = logging.getLogger(__name__)

from .models import (
    DimStudent, DimTeacher, DimParent,
    FactWritingDataset, FactTeacherSurveyDataset,
    FactShapesDataset, FactEmotionsDataset, FactAutismTeacherSurveyDataset
)
from .serializers import (
    DimStudentSerializer, DimTeacherSerializer, DimParentSerializer,
    FactWritingDatasetSerializer, FactShapesDatasetSerializer,
    FactEmotionsDatasetSerializer, FactAutismTeacherSurveyDatasetSerializer,
    FactTeacherSurveyDatasetSerializer
)

# === CREATE (POST) ===
class TeacherCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DimTeacher.objects.all()
    serializer_class = DimTeacherSerializer

class ParentCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DimParent.objects.all()
    serializer_class = DimParentSerializer

class WritingDataCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactWritingDataset.objects.all()
    serializer_class = FactWritingDatasetSerializer

class ShapesDataCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactShapesDataset.objects.all()
    serializer_class = FactShapesDatasetSerializer

class EmotionsDataCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactEmotionsDataset.objects.all()
    serializer_class = FactEmotionsDatasetSerializer

class AutismSurveyCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactAutismTeacherSurveyDataset.objects.all()
    serializer_class = FactAutismTeacherSurveyDatasetSerializer

class TeacherSurveyCreateView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactTeacherSurveyDataset.objects.all()
    serializer_class = FactTeacherSurveyDatasetSerializer

# === LIST (GET) ===

# Returns the teacher ID based on the authenticated user's email
class GetTeacherIDView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        email = getattr(request.user, "email", None)
        if not email:
            return Response({"error": "Brak emaila w tokenie"}, status=400)
        try:
            teacher = DimTeacher.objects.get(email=email)
            return Response({"teacher_id": teacher.teacher_id})
        except DimTeacher.DoesNotExist:
            return Response({"error": "Nauczyciel nie znaleziony"}, status=404)



class StudentDetailView(generics.RetrieveUpdateAPIView):
    queryset = DimStudent.objects.all()
    serializer_class = DimStudentSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        user_email = self._get_user_email_from_token(request)
        if isinstance(user_email, Response):
            return user_email  # błąd tokena

        # Pobierz studenta
        try:
            student = DimStudent.objects.get(pk=student_id)
        except DimStudent.DoesNotExist:
            return Response({"detail": "Student not found."}, status=404)

        # Próbuj jako nauczyciel
        try:
            teacher = DimTeacher.objects.get(email=user_email)
        except DimTeacher.DoesNotExist:
            teacher = None

        if teacher:
            if student.class_name != teacher.class_name:
                return Response({"detail": "Access denied (teacher)."}, status=403)
        else:
            # Próbuj jako rodzic
            try:
                parent = DimParent.objects.get(email=user_email)
            except DimParent.DoesNotExist:
                return Response({"detail": "User not found (neither teacher nor parent)."}, status=404)

            if student.parent_id != parent.id:
                return Response({"detail": "Access denied (parent)."}, status=403)

        serializer = DimStudentSerializer(student)
        return Response(serializer.data)


    def patch(self, request, *args, **kwargs):
        student_id = kwargs.get("student_id")
        user_email = self._get_user_email_from_token(request)
        if isinstance(user_email, Response):
            return user_email

        try:
            teacher = DimTeacher.objects.get(email=user_email)
        except DimTeacher.DoesNotExist:
            return Response({"detail": "Teacher not found."}, status=404)

        try:
            student = DimStudent.objects.get(pk=student_id)
        except DimStudent.DoesNotExist:
            return Response({"detail": "Student not found."}, status=404)

        if (student.class_name != teacher.class_name):
            return Response({"detail": "Access denied."}, status=403)

        data = request.data.copy()
        data['class_name'] = teacher.class_name

        serializer = DimStudentSerializer(student, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def _get_user_email_from_token(self, request):
        auth_header = get_authorization_header(request).split()
        if not auth_header or auth_header[0].lower() != b'bearer':
            return Response({"detail": "Missing or invalid token header"}, status=401)

        try:
            decoded_token = firebase_auth.verify_id_token(auth_header[1].decode())
            return decoded_token.get("email")
        except Exception:
            return Response({"detail": "Invalid Firebase token"}, status=401)

class TeacherListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DimTeacher.objects.all()
    serializer_class = DimTeacherSerializer

class ParentListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = DimParent.objects.all()
    serializer_class = DimParentSerializer

class WritingDatasetListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactWritingDataset.objects.all()
    serializer_class = FactWritingDatasetSerializer

class ShapesDatasetListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactShapesDataset.objects.all()
    serializer_class = FactShapesDatasetSerializer

class EmotionsDatasetListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactEmotionsDataset.objects.all()
    serializer_class = FactEmotionsDatasetSerializer

class AutismSurveyListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactAutismTeacherSurveyDataset.objects.all()
    serializer_class = FactAutismTeacherSurveyDatasetSerializer

class TeacherSurveyListView(generics.ListAPIView):
    permission_classes = [permissions.AllowAny]
    queryset = FactTeacherSurveyDataset.objects.all()
    serializer_class = FactTeacherSurveyDatasetSerializer

@api_view(['GET'])
def get_parent_email_by_student(request, student_id):
    student = get_object_or_404(DimStudent, pk=student_id)
    parent = student.parent

    if not parent.email:
        return Response({'detail': 'Email not found for parent.'}, status=status.HTTP_404_NOT_FOUND)

    return Response({'parent_email': parent.email})

    

from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import logging
_vertex_endpoint = None


def get_vertex_endpoint():
    global _vertex_endpoint

    if _vertex_endpoint is None:
        from google.cloud import aiplatform

        # Inicjalizacja Vertex AI - wykonaj to tylko raz przy starcie
        aiplatform.init(project="psychological-app-a359c", location="europe-central2")
        # Endpoint do modelu emotions
        vertex_endpoint = aiplatform.Endpoint(
            endpoint_name="projects/psychological-app-a359c/locations/europe-central2/endpoints/43404321018085376"
        )
        # Endpoint do modelu shapes
        vertex_shapes_endpoint = aiplatform.Endpoint(
            endpoint_name="projects/psychological-app-a359c/locations/europe-central2/endpoints/592843475557285888"  
        )
        # Endpoint do modelu questionnaires
        vertex_questionnaires_endpoint = aiplatform.Endpoint(
            endpoint_name="projects/psychological-app-a359c/locations/europe-central2/endpoints/608606074253082624"
        )

    return _vertex_endpoint


class PredictEmotionsView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, student_id):
        try:
            raw_data = FactEmotionsDataset.objects.filter(student_id=student_id).values("happy", "angry", "sad", "time")
            instances = [
                [row["happy"], row["angry"], row["sad"], float(row["time"])]
                for row in raw_data
            ]
            prediction_response = get_vertex_endpoint().predict(instances=instances)
            return Response({"predictions": prediction_response.predictions}, status=200)

        except requests.exceptions.RequestException as e:
            logging.error(f"Błąd pobierania danych: {e}")
            return Response({"error": "Błąd pobierania danych z lokalnego API."}, status=502)

        except ValueError as e:
            logging.error(f"Błąd dekodowania JSON: {e}")
            return Response({"error": "Niepoprawny format danych JSON."}, status=400)

        except Exception as e:
            logging.exception("Niespodziewany błąd podczas predykcji.")
            return Response({"error": f"Wystąpił błąd serwera: {str(e)}"}, status=500)


class PredictShapesView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, student_id):
        try:
            # 1. Pobierz dane z bazy dla konkretnego studenta
            raw_data = FactShapesDataset.objects.filter(student_id=student_id).values("correct", "time")

            # 2. Mapa correct na float
            correct_mapping = {
                6: 1.00,
                5: 0.95,
                4: 0.85,
                3: 0.70,
                2: 0.45,
                1: 0.20,
                0: 0.00
            }

            # 3. Przekształć dane na instancje wejściowe modelu
            instances = [
                [correct_mapping.get(row.get("correct", 0), 0.0), float(row.get("time", 0.0))]
                for row in raw_data
            ]

            if not instances:
                return Response({"error": "Brak danych kształtów dla tego studenta."}, status=404)

            # 4. Wywołaj endpoint modelu
            prediction_response = get_vertex_endpoint().predict(instances=instances)

            # 5. Funkcja konwertująca Decimal na float
            def convert_decimals(obj):
                if isinstance(obj, list):
                    return [convert_decimals(i) for i in obj]
                elif isinstance(obj, dict):
                    return {k: convert_decimals(v) for k, v in obj.items()}
                elif isinstance(obj, Decimal):
                    return float(obj)
                else:
                    return obj

            cleaned_predictions = convert_decimals(prediction_response.predictions)

            return Response({"predictions": cleaned_predictions}, status=200)

        except Exception as e:
            logging.exception("Błąd podczas predykcji kształtów.")
            return Response({"error": f"Wystąpił błąd serwera: {str(e)}"}, status=500)


class PredictQuestionnaire1View(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, student_id):
        try:
            question_keys = [f"q{i}" for i in range(1, 17)]
            data = FactAutismTeacherSurveyDataset.objects.filter(student_id=student_id).values(*question_keys).first()
            if not data:
                return Response({"error": "No data for given student"}, status=404)

            instance = [[data.get(k, 0) or 0 for k in question_keys]]
            prediction_response = get_vertex_endpoint().predict(instances=instance)
            return Response({"predictions": prediction_response.predictions}, status=200)

        except requests.exceptions.RequestException as e:
            logging.error(f"Błąd pobierania danych: {e}")
            return Response({"error": "Błąd pobierania danych z lokalnego API."}, status=502)

        except ValueError as e:
            logging.error(f"Błąd dekodowania JSON: {e}")
            return Response({"error": "Niepoprawny format danych JSON."}, status=400)

        except Exception as e:
            logging.exception("Niespodziewany błąd podczas predykcji.")
            return Response({"error": f"Wystąpił błąd serwera: {str(e)}"}, status=500)
        

class PredictQuestionnaire2View(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, student_id):
        try:
            question_keys = [f"q{i}" for i in range(1, 17)]
            data = FactTeacherSurveyDataset.objects.filter(student_id=student_id).values(*question_keys).first()
            if not data:
                return Response({"error": "No data for given student"}, status=404)

            instance = [[data.get(k, 0) or 0 for k in question_keys]]
            prediction_response = get_vertex_endpoint().predict(instances=instance)
            return Response({"predictions": prediction_response.predictions}, status=200)

        except requests.exceptions.RequestException as e:
            logging.error(f"Błąd pobierania danych: {e}")
            return Response({"error": "Błąd pobierania danych z lokalnego API."}, status=502)

        except ValueError as e:
            logging.error(f"Błąd dekodowania JSON: {e}")
            return Response({"error": "Niepoprawny format danych JSON."}, status=400)

        except Exception as e:
            logging.exception("Niespodziewany błąd podczas predykcji.")
            return Response({"error": f"Wystąpił błąd serwera: {str(e)}"}, status=500)


class PredictEnsembleView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, student_id):
        try:
            predictions = []

            # 1. Predict emotions
            raw_emotions = FactEmotionsDataset.objects.filter(student_id=student_id).values("happy", "angry", "sad", "time")
            emotion_instances = [
                [row["happy"], row["angry"], row["sad"], float(row["time"])]
                for row in raw_emotions
            ]
            if emotion_instances:
                emotion_result = get_vertex_endpoint().predict(instances=emotion_instances)
                predictions += [round(p) for p in emotion_result.predictions]

            # 2. Predict shapes
            raw_shapes = FactShapesDataset.objects.filter(student_id=student_id).values("correct", "time")
            correct_mapping = {
                6: 1.00,
                5: 0.95,
                4: 0.85,
                3: 0.70,
                2: 0.45,
                1: 0.20,
                0: 0.00
            }

            # 3. Przekształć dane do formatu oczekiwanego przez model
            shape_instances = [
                [correct_mapping.get(row["correct"],0.0), float(row["time"])]
                for row in raw_shapes
            ]
            
            if shape_instances:
                shape_result = get_vertex_endpoint().predict(instances=shape_instances)
                predictions += [round(p) for p in shape_result.predictions]

            # 3. Predict questionnaire - autism
            question_keys = [f"q{i}" for i in range(1, 17)]
            data_autism = FactAutismTeacherSurveyDataset.objects.filter(student_id=student_id).values(*question_keys).first()
            if data_autism:
                autism_instance = [[data_autism.get(k, 0) or 0 for k in question_keys]]
                autism_result =get_vertex_endpoint().predict(instances=autism_instance)
                predictions += [round(p) for p in autism_result.predictions]

            # 4. Predict questionnaire - ADHD
            data_adhd = FactTeacherSurveyDataset.objects.filter(student_id=student_id).values(*question_keys).first()
            if data_adhd:
                adhd_instance = [[data_adhd.get(k, 0) or 0 for k in question_keys]]
                adhd_result = get_vertex_endpoint().predict(instances=adhd_instance)
                predictions += [round(p) for p in adhd_result.predictions]

            if not predictions:
                return Response({"error": "Brak danych do agregacji predykcji."}, status=404)

            # Majority vote
            counter = Counter(predictions)
            negative_count = counter.get(-1, 0)
            positive_count = counter.get(1, 0)
            total = negative_count + positive_count

            if total == 0:
                score = None  
            else:
                score = negative_count / total

            return Response({
                "predictions": predictions,
                "negative_ratio": score 
            }, status=200)

        except Exception as e:
            logging.exception("Błąd podczas predykcji ensemble.")
            return Response({"error": str(e)}, status=500)

# === POST & GET ===

class StudentListCreateView(generics.ListCreateAPIView):
    serializer_class = DimStudentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        email = getattr(user, "email", None)
        logger.info(f"Email from user: {email}")

        if not email:
            raise ValidationError({"error": "Brak emaila w tokenie"})

        # Spróbuj najpierw jako nauczyciel
        teacher = DimTeacher.objects.filter(email=email).first()
        if teacher:
            return DimStudent.objects.filter(teacher=teacher)

        # Spróbuj jako rodzic
        parent = DimParent.objects.filter(email=email).first()
        if parent:
            return DimStudent.objects.filter(parent=parent)

        # Jeżeli ani jedno, ani drugie
        raise ValidationError({"error": "Użytkownik nie jest nauczycielem ani rodzicem"})

    def perform_create(self, serializer):
        user = self.request.user
        email = getattr(user, "email", None)
        logger.info(f"User in perform_create: {user}")
        logger.info(f"Email from user: {email}")
        if not email:
            raise ValidationError({"error": "Brak emaila w tokenie"})
        try:
            teacher = DimTeacher.objects.get(email=email)
        except DimTeacher.DoesNotExist:
            raise ValidationError({"error": "Nauczyciel nie znaleziony"})
        logger.info(f"Creating student with data: {serializer.validated_data}")
        serializer.save(class_name=teacher.class_name, teacher = teacher)  # Przypisanie nauczyciela i klasy do ucznia

    def get_serializer_context(self):
        context = super().get_serializer_context()
        user = self.request.user
        logger.info(f"User in get_serializer_context: {user}")
        try:
            teacher = DimTeacher.objects.get(email=user.email)
        except DimTeacher.DoesNotExist:
            teacher = None
        context['teacher'] = teacher
        return context

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            logger.error(f"Serializer errors: {serializer.errors}")
            return Response(serializer.errors, status=400)
        self.perform_create(serializer)
        return Response(serializer.data, status=201)


