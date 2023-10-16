# Generated by Django 3.2.18 on 2023-06-26 13:15

import django.contrib.postgres.indexes
import django.contrib.postgres.search
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("giftcard", "0018_metadata_index"),
    ]

    operations = [
        migrations.AddField(
            model_name="giftcard",
            name="search_index_dirty",
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name="giftcard",
            name="search_vector",
            field=django.contrib.postgres.search.SearchVectorField(
                blank=True, null=True
            ),
        ),
        migrations.RunSQL(
            """
            ALTER TABLE giftcard_giftcard
            ALTER COLUMN search_index_dirty
            SET DEFAULT true;
            """,
            migrations.RunSQL.noop,
        ),
    ]