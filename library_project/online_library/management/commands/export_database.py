from django.core.management.base import BaseCommand
from django.apps import apps
from django.db import models
import os
import datetime

class Command(BaseCommand):
    help = 'Exports all database tables to a text file'

    def handle(self, *args, **options):
        # Get all models from the online_library app
        app_models = apps.get_app_config('online_library').get_models()
        
        # Create output file
        output_file = os.path.join(os.getcwd(), 'database_export.txt')
        
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(f"DATABASE EXPORT - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write("=" * 80 + "\n\n")
            
            # Process each model
            for model in app_models:
                model_name = model.__name__
                f.write(f"TABLE: {model_name}\n")
                f.write("-" * 80 + "\n")
                
                # Get all fields for the model
                fields = [field for field in model._meta.fields]
                field_names = [field.name for field in fields]
                
                # Write header
                f.write(" | ".join(field_names) + "\n")
                f.write("-" * 80 + "\n")
                
                # Get all records
                records = model.objects.all()
                
                if not records:
                    f.write("No records found.\n")
                else:
                    # Write each record
                    for record in records:
                        row = []
                        for field in fields:
                            value = getattr(record, field.name)
                            # Format datetime fields
                            if isinstance(value, datetime.datetime):
                                value = value.strftime('%Y-%m-%d %H:%M:%S')
                            elif isinstance(value, datetime.date):
                                value = value.strftime('%Y-%m-%d')
                            # Convert to string and truncate if too long
                            value_str = str(value)
                            if len(value_str) > 50:
                                value_str = value_str[:47] + "..."
                            row.append(value_str)
                        f.write(" | ".join(row) + "\n")
                
                f.write("\n\n")
            
            f.write("END OF DATABASE EXPORT\n")
        
        self.stdout.write(self.style.SUCCESS(f"Database exported to {output_file}"))
