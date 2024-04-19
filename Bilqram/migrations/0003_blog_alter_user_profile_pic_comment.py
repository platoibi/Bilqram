# Generated by Django 5.0.4 on 2024-04-19 16:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Bilqram', '0002_alter_content_id_alter_user_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Bilqram.content')),
            ],
            bases=('Bilqram.content',),
        ),
        migrations.AlterField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(upload_to='Bilqram/Images/Profile_Pictures'),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('content_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='Bilqram.content')),
                ('parblog', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Bilqram.blog')),
            ],
            bases=('Bilqram.content',),
        ),
    ]
