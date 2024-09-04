# community/member/management/commands/import_schools.py

from django.core.management.base import BaseCommand
import csv
from member.models import School

class Command(BaseCommand):
    help = 'Import schools from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='The path to the CSV file')

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        
        # CSV 파일 열기 및 데이터 읽기
        with open(csv_file, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                # School 모델에 데이터 추가
                School.objects.create(
                    city=row['시도명'],
                    school_type=row['학교종류명'],
                    school_name=row['학교명']
                )
        
        self.stdout.write(self.style.SUCCESS('Successfully imported schools'))
