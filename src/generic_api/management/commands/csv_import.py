import csv
import os
from pathlib import Path
from typing import Any

from django.core.management import BaseCommand
from django.contrib import auth
from ...models import Comment, Post

class Command(BaseCommand):

    def handle(self, *args: Any, **options: Any) -> str | None:
        csv_dir_path = os.path.join(Path(__file__).resolve().parent, 'csvs')

        # user -> post -> comment の順で紐づくため、この順番でないとダメ
        models = (auth.get_user_model(), Post, Comment)
        files  = ('users.csv', 'posts.csv', 'comments.csv')

        for file, model in zip(files, models):
            path = os.path.join(csv_dir_path, file)
            data = self._read_csv_file(path)
            self._insert_data(model, data)

    def _read_csv_file(self, file_path):
        with open(file_path, 'r', encoding='utf-8', newline='') as f:
            data = [row_dict for row_dict in csv.DictReader(f)]
        f.close()
        return data

    def _insert_data(self, model, data: dict):
        insert_list = []
        for row in data:
            new = model(**row)
            if model == auth.get_user_model():
                new.set_password(raw_password='12345678')
            insert_list.append(new)
        model.objects.bulk_create(insert_list)
