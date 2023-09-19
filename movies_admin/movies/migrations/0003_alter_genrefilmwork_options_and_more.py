# Generated by Django 4.2.5 on 2023-09-19 20:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_filmwork_person_alter_genre_description_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='genrefilmwork',
            options={'verbose_name': 'Жанр кинопроизведения', 'verbose_name_plural': 'Жанры кинопроизведения'},
        ),
        migrations.AlterModelOptions(
            name='personfilmwork',
            options={'verbose_name': 'Участник кинопроизведения', 'verbose_name_plural': 'Участники кинопроизведения'},
        ),
        migrations.AlterField(
            model_name='personfilmwork',
            name='role',
            field=models.CharField(choices=[('actor', 'Аctor'), ('director', 'Director'), ('writer', 'Writer')], default='actor', max_length=8, verbose_name='Роль'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['title'], name='title_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['rating'], name='rating_idx'),
        ),
        migrations.AddIndex(
            model_name='filmwork',
            index=models.Index(fields=['creation_date'], name='creation_date_idx'),
        ),
        migrations.AddIndex(
            model_name='genre',
            index=models.Index(fields=['name'], name='name_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work'], name='film_work_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['genre'], name='genre_idx'),
        ),
        migrations.AddIndex(
            model_name='genrefilmwork',
            index=models.Index(fields=['film_work', 'genre'], name='filmwork_genre_idx'),
        ),
        migrations.AddIndex(
            model_name='person',
            index=models.Index(fields=['full_name'], name='full_name_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['person'], name='person_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['film_work'], name='filmwork_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['person', 'film_work'], name='person_filmwork_idx'),
        ),
        migrations.AddIndex(
            model_name='personfilmwork',
            index=models.Index(fields=['role'], name='role_idx'),
        ),
    ]
