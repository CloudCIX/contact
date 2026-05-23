# Generated manually
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0060_chatbot_rewrite_prompt'),
    ]

    operations = [
        migrations.AddField(
            model_name='chatbot',
            name='maximum_conversation_turn',
            field=models.IntegerField(default=0),
        ),
    ]
