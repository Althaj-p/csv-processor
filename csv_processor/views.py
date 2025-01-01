from django.shortcuts import render
from .models import User
from .serializers import UserSerializer
import csv
from io import StringIO
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

# Django View for rendering the HTML template
def home(request):
    # Fetch existing users from the database
    existing_users = User.objects.all()

    # Render the template and pass the existing users to the context
    return render(request, 'index.html', {
        'existing_users': existing_users
    })

# DRF API View for handling CSV upload
class CSVUploadAPIView(APIView):
    def post(self, request):
        file = request.FILES.get('file')

        # Validate file extension
        if not file or not file.name.endswith('.csv'):
            return Response({"error": "Invalid file type. Only .csv files are allowed."}, status=status.HTTP_400_BAD_REQUEST)

        decoded_file = file.read().decode('utf-8')
        io_string = StringIO(decoded_file)
        reader = csv.DictReader(io_string)

        valid_records = []
        rejected_records = 0
        errors = []
        saved_users = []

        for index, row in enumerate(reader, start=1):
            serializer = UserSerializer(data=row)
            if serializer.is_valid():
                # Check for duplicate email
                if not User.objects.filter(email=serializer.validated_data['email']).exists():
                    valid_records.append(User(**serializer.validated_data))
                    saved_users.append({
                        "email": serializer.validated_data['email'],
                        "name": serializer.validated_data.get('name', 'N/A'),
                        "age": serializer.validated_data.get('age', 'N/A')
                    })
                else:
                    errors.append({
                        "row": index,
                        "email": serializer.validated_data['email'],
                        "error": "Duplicate email."
                    })
                    rejected_records += 1
            else:
                errors.append({
                    "row": index,
                    "email": row.get('email', 'N/A'),
                    "error": serializer.errors
                })
                rejected_records += 1

        # Bulk create valid records
        if valid_records:
            User.objects.bulk_create(valid_records)

        # Return the saved users (those successfully added to the database)
        return Response({
            "valid_records": len(valid_records),
            "rejected_records": rejected_records,
            "saved_users": saved_users,
            "errors": errors
        }, status=status.HTTP_200_OK)

