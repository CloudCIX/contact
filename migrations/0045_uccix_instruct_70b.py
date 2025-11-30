from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0044_contact_cookie_optional_fields_conversation_model'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chatbot',
            name='nn_llm',
            field=models.CharField(
                choices=[
                    ('chatgpt4', 'chatgpt4'),
                    ('deepseek', 'deepseek'),
                    ('uccix_instruct', 'uccix_instruct'),
                    ('uccix_instruct_70b', 'uccix_instruct_70b'),
                ],
                default='deepseek',
                max_length=20,
            ),
        ),
    ]
