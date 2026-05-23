# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0059_chatbot_apply_prompt_rewriting'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='rewrite_prompt',
            field=models.CharField(max_length=10000, null=True),
        ),
    ]
