# Generated by Django 4.2.6 on 2023-10-23 14:48

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("olt", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="usuario",
            name="setor",
            field=models.CharField(
                choices=[("NOC", "NOC"), ("TECNICO", "Técnico")],
                default="TECNICO",
                max_length=10,
            ),
        ),
        migrations.AlterField(
            model_name="usuario",
            name="ativo",
            field=models.BooleanField(default=False),
        ),
    ]
