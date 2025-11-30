from django.db import migrations


def generate_default_records(apps, schema_editor):
    activity = apps.get_model('contact', 'Activity')
    activity_type = apps.get_model('contact', 'ActivityType')
    db_alias = schema_editor.connection.alias

    """
    Add Default Activity Type records for member_id=0
    """
    activity_type.objects.using(db_alias).create(name='Collaborations', member_id=0)
    activity_type.objects.using(db_alias).create(name='Communications', member_id=0)
    activity_type.objects.using(db_alias).create(name='Events', member_id=0)
    activity_type.objects.using(db_alias).create(name='Expert Support', member_id=0)
    activity_type.objects.using(db_alias).create(name='Storytelling', member_id=0)

    """
    Add Default Activity records for member_id=0
    """

    """
    1. Adding Activities for Collaborations Activity Type
    """
    collaborations = activity_type.objects.using(db_alias).get(name='Collaborations', member_id=0)
    activity.objects.using(db_alias).create(
        activity_type=collaborations,
        name='Public',
        properties='{"organisation": "string", "description": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=collaborations,
        name='Private',
        properties='{"organisation": "string", "description": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=collaborations,
        name='Community',
        properties='{"organisation": "string", "description": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=collaborations,
        name='Other',
        properties='{"organisation": "string", "description": "string"}',
    )

    """
    2. Adding Activities for Communication Activity Type
    """
    communications = activity_type.objects.using(db_alias).get(name='Communications', member_id=0)
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Print Media Advertisement',
        properties='{"name_of_publication": "string", "page_number": "integer", "cost": "money"}',
    )
    properties = '{"name_of_publication": "string", "page_number": "integer", "column_height": "float", '
    properties += '"column_width": "float","image_height": "float", "image_width": "float", "eav": "money"}'
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Print Media Press Coverage',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Radio Advertisement',
        properties='{"station": "string", "show": "string", "cost": "money"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Radio Interview',
        properties='{"station": "string", "show": "string", "duration": "integer", "eav": "money"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Radio Mention',
        properties='{"station": "string", "show": "string", "duration": "integer", "eav": "money"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='TV Advertisement',
        properties='{"station": "string", "show": "string", "duration": "integer", "eav": "money"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Billboard',
        properties='{"number": "integer", "locations": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Road Sign',
        properties='{"number": "integer", "locations": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Vehicle Branding',
        properties='{"number": "integer", "locations": "string"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Website',
        properties='{"unique_number_of_visits": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Marketing Material',
        properties='{"number_of_items_produced": "integer", "number_of_items_distributed": "integer"}',
    )
    properties = '{"members": "integer", "sent": "integer", "opens": "integer", "shares": "integer", '
    properties += '"clicks": "integer"}'
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Newsletter',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Phone Call',
        properties='{"outgoing_calls": "integer", "incoming_calls": "integer"}',
    )
    properties = '{"number": "integer", "endorser_name": "string", "organisation": "string", "date": "datetime", '
    properties += '"medium": "string", "note": "string"}'
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Endorsement',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Facebook',
        properties='{"posts": "integer", "likes": "integer", "reach": "integer", "engagement": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Twitter',
        properties='{"tweets": "integer", "followers": "integer", "impressions": "integer", "mentions": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='LinkedIn',
        properties='{"connections": "integer", "discussions": "integer", "likes": "integer", "comments": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Youtube',
        properties='{"videos": "integer", "views": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Pinterest',
        properties='{"pins": "integer", "repins": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Google+',
        properties='{"views": "integer"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=communications,
        name='Instagram',
        properties='{"posts": "integer", "likes": "integer", "tags": "integer"}',
    )

    """
    3. Adding Activities for Event Activity Type
    """
    events = activity_type.objects.using(db_alias).get(name='Events', member_id=0)
    properties = '{"date": "datetime", "location": "string", "number": "integer", "trade_stand": "boolean", '
    properties += '"speaker_slot": "boolean"}'
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Seminar',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Workshop',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Training',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Networking',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Exhibition',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Conference',
        properties=properties,
    )
    activity.objects.using(db_alias).create(
        activity_type=events,
        name='Other',
        properties=properties,
    )

    """
    4. Adding Activities for Expert Support Activity Type
    """
    expert_support = activity_type.objects.using(db_alias).get(name='Expert Support', member_id=0)
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Phone Call',
        properties='{"number": "integer", "document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Email',
        properties='{"number": "integer", "document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Site Visit',
        properties='{"number": "integer", "document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Audit',
        properties='{"number": "integer", "document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Technical Guidance Document',
        properties='{"number": "integer", "document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=expert_support,
        name='Technical Intervention',
        properties='{"number": "integer", "document": "file"}',
    )

    """
    5. Adding Activities for Storytelling Activity Type
    """
    storytelling = activity_type.objects.using(db_alias).get(name='Storytelling', member_id=0)
    activity.objects.using(db_alias).create(
        activity_type=storytelling,
        name='Audio',
        properties='{"document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=storytelling,
        name='Video',
        properties='{"document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=storytelling,
        name='Transcript',
        properties='{"document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=storytelling,
        name='Animation',
        properties='{"document": "file"}',
    )
    activity.objects.using(db_alias).create(
        activity_type=storytelling,
        name='Other',
        properties='{"document": "file"}',
    )


def reverse_func(apps, schema_editor):  # pragma: no cover
    activity = apps.get_model('contact', 'Activity')
    activity_type = apps.get_model('contact', 'ActivityType')
    db_alias = schema_editor.connection.alias

    """
    Remove Default Activity and Activity Type records for member_id=0 in case error occurs above
    """

    types_to_delete = activity_type.objects.using(db_alias).filter(
        member_id=0,
        name__in=['Collaborations', 'Communications', 'Events', 'Expert Support', 'Storytelling'],
    )
    activity.objects.using(db_alias).filter(activity_type__in=types_to_delete).delete()
    types_to_delete.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(generate_default_records, reverse_func),
    ]
