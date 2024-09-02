import csv
import os
from django.core.management.base import BaseCommand
from member.models import School

class Command(BaseCommand):
    help = 'Import schools from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file')

    def handle(self, *args, **options):
        csv_file = options['csv_file']
        if not os.path.isfile(csv_file):
            self.stderr.write(self.style.ERROR(f'File not found: {csv_file}'))
            return

        try:
            with open(csv_file, 'r', encoding='utf-8') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    city = row['시도명']
                    school_type = row['학교종류명']
                    school_name = row['학교명']
                    
                    # Ensure data is not duplicated
                    if not School.objects.filter(city=city, school_type=school_type, school_name=school_name).exists():
                        School.objects.create(city=city, school_type=school_type, school_name=school_name)
                
            self.stdout.write(self.style.SUCCESS(f'Successfully imported schools from {csv_file}'))
        except Exception as e:
            self.stderr.write(self.style.ERROR(f'Error: {str(e)}'))
