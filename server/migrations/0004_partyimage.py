# Generated by Django 2.1.7 on 2020-04-18 15:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('server', '0003_auto_20190405_1948'),
    ]

    operations = [
        migrations.CreateModel(
            name='PartyImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resize', models.IntegerField(choices=[(32, 32), (64, 64), (128, 128), (256, 256)], null=True)),
                ('negate', models.CharField(choices=[('red', 'red'), ('green', 'green'), ('blue', 'blue')], max_length=8, null=True)),
                ('n_frames', models.IntegerField(choices=[(6, 6), (8, 8), (10, 10), (12, 12), (16, 16), (20, 20), (24, 24), (30, 30), (32, 32)], null=True)),
                ('replace_color', models.CharField(max_length=16, null=True)),
                ('delay', models.IntegerField(choices=[(2, 2), (4, 4), (6, 6), (8, 8), (10, 10), (12, 12), (16, 16), (20, 20)], default=6, null=True)),
                ('fuzz', models.IntegerField(choices=[(0, 0), (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), (11, 11), (12, 12), (13, 13), (14, 14), (15, 15), (16, 16), (17, 17), (18, 18), (19, 19), (20, 20), (21, 21), (22, 22), (23, 23), (24, 24), (25, 25), (26, 26), (27, 27), (28, 28), (29, 29), (30, 30), (31, 31), (32, 32), (33, 33), (34, 34), (35, 35), (36, 36), (37, 37), (38, 38), (39, 39), (40, 40), (41, 41), (42, 42), (43, 43), (44, 44), (45, 45), (46, 46), (47, 47), (48, 48), (49, 49)], default=3, null=True)),
                ('sourceimage', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='server.SourceImage')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]