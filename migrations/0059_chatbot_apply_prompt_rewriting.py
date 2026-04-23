from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0058_supported_models'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='apply_prompt_rewriting',
            field=models.BooleanField(default=False),
        ),
    ]
