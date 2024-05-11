import csv
import os
from pathlib import Path
from typing import Any

from django.core.management import BaseCommand
from django.contrib import auth


class Command(BaseCommand):
    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_dir_path = os.path.join(Path(__file__).resolve().parent, 'csvs')

        comments_path = os.path.join(csv_dir_path, 'comments.csv')
        posts_path = os.path.join(csv_dir_path, 'posts.csv')
        users_path = os.path.join(csv_dir_path, 'users.csv')
        
        comments = self._read_csv_file(comments_path)
        posts    = self._read_csv_file(posts_path)
        users    = self._read_csv_file(users_path)
        self._insert_user_data(auth.get_user_model(), users)


    def _read_csv_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            data = [row for row in csv.DictReader(f)]
        f.close()
        return data

    def _insert_user_data(self, user_model, user_data: dict):
        insert_list = []
        for row in user_data:
            new = user_model(**row)
            new.set_password(raw_password='12345678')
            insert_list.append(new)
        user_model.objects.bulk_create(insert_list)
