from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import FileResponse
from .models import File
from .serializers import FileSerializer
from .serializers import predict_class
import tempfile
import os

# from sklearn.model_selection import train_test_split
# from sklearn.preprocessing import StandardScaler
# from sklearn.linear_model import LogisticRegression
# from sklearn.metrics import classification_report
# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import accuracy_score
# from sklearn.metrics import precision_score
# from sklearn.metrics import recall_score
# from sklearn.metrics import f1_score
# from sklearn.tree import export_graphviz
# from sklearn.metrics import roc_auc_score
# from imblearn.under_sampling import RandomUnderSampler
# from imblearn.over_sampling import RandomOverSampler



class FileUploadAPIView(APIView):
    def post(self, request):
        try:
            serializer = FileSerializer(data=request.data)
            if serializer.is_valid():
                user_id = request.user.id
                serializer.validated_data['user_id'] = user_id
                           
                _file = serializer.save()
                class_counts, local_csv_with_class = predict_class(_file.id)

                # Convert the local_csv_with_class DataFrame to a CSV file
                temp_csv_file = tempfile.NamedTemporaryFile(delete=False)
                local_csv_with_class.to_csv(temp_csv_file.name, index=False)

                # Save the temporary CSV file in the result_file field of the File model
                _file.result_file.save(f"result_{_file.id}.csv", temp_csv_file)

                # Close and delete the temporary file
                temp_csv_file.close()
                os.remove(temp_csv_file.name)

                response_data = {
                    'message': 'File Uploaded Successfully',
                    'File ID': _file.id,
                    'date': _file.date,
                    'counts': class_counts
                }
                return Response(response_data,status=200)
            return Response(serializer.errors, status=201)
        except Exception as e:
            return Response({'message': str(e)}, status=500)


class UserFileListAPIView(APIView):
    def get(self, request):
        user_id = request.user.id
        
        files = File.objects.filter(user_id=user_id)
        serializer = FileSerializer(files, many=True)

        return Response(serializer.data)

class FileDownloadAPIView(APIView):
    def get(self, request, file_id):
        try:
            file_obj = File.objects.get(id=file_id, user_id=request.user.id)
            file_path = file_obj.result_file.path
            return FileResponse(open(file_path, 'rb'), as_attachment=True)
        except File.DoesNotExist:
            return Response({'message': 'File Not Found'}, status=201)

class FileDeleteAPIView(APIView):
    def get(self, request, file_id):
        try:
            file_obj = File.objects.get(id=file_id, user_id=request.user.id)
            if file_obj.delete():
                return Response({'message': 'File deleted successfully'}, status=200)
            return Response({'message': 'File Not Found'}, status=201)
        except File.DoesNotExist:
            return Response({'message': 'File Not Found'}, status=201)
        except Exception as e:
            return Response({'message': 'Something is Wrong'}, status=500)