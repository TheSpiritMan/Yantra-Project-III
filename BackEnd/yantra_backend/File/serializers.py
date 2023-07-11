from rest_framework import serializers
from .models import File
from django.conf import settings
import pickle
import pandas as pd
import numpy as np


class FileSerializer(serializers.ModelSerializer):
    class Meta:
        model = File
        fields = ['id','date', 'csv_file', 'result_file']
        read_only_fields = ['id']


# AI Deployed and Predict Result
def predict_class(id):
    try:
        _file = File.objects.get(id=id)
        local_csv = pd.read_csv(_file.csv_file)
        model = pickle.load(open(settings.MODEL_PATH,'rb'))
        result_predict = model.predict(local_csv)

        # Create New Dataframe with "Class" Column
        class_df = pd.DataFrame({'Class': result_predict})
        local_csv_with_class = pd.concat([local_csv, class_df], axis=1)
        
        value_counts = local_csv_with_class['Class'].value_counts()
        counts = {
            '0': value_counts[0],
            '1': value_counts[1]
        }
        return counts, local_csv_with_class
    except Exception as e:
        print(str(e))