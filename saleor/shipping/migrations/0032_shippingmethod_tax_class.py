# Generated by Django 4.0.7 on 2022-09-14 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("tax", "0001_initial"),
        ("shipping", "0031_alter_shippingmethodtranslation_language_code"),
    ]

    operations = [
        migrations.AddField(
            model_name="shippingmethod",
            name="tax_class",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="shipping_methods",
                to="tax.taxclass",
            ),
        ),
    ]
