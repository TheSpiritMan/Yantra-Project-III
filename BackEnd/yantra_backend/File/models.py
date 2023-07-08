from django.db import models
import uuid
import magic
from django.core.exceptions import ValidationError
from django.utils.timezone import now

def validate_csv_file(value):
    file_mime = magic.from_buffer(value.read(), mime=True)
    if file_mime != 'text/csv':
        raise ValidationError('Only CSV files are allowed.')

class File(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField()
    csv_file = models.FileField(upload_to='csv_files/', validators=[validate_csv_file])
    result_file = models.FileField(upload_to='result_files/', validators=[validate_csv_file], null = True)
    date = models.DateTimeField(default=now, editable=False)
    
    class Meta:
        db_table = 'user_file'

    def __str__(self):
        return f"File ID: {self.id}, User ID: {self.user_id}"