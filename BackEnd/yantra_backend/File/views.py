from rest_framework.views import APIView
from rest_framework.response import Response
from .models import File
from .serializers import FileSerializer

class FileUploadAPIView(APIView):
    def post(self, request):
        try:
            serializer = FileSerializer(data=request.data)
            if serializer.is_valid():
                user_id = request.user.id
                serializer.validated_data['user_id'] = user_id

                _file = serializer.save()
                return Response({'message': 'File Uploaded Successfully', 'File ID': _file.id},status=201)
            return Response(serializer.errors, status=400)
        except Exception as e:
            return Response({'message': str(e)}, status=500)