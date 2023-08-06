from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='Heading',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, related_name='djangocms_headings_heading', serialize=False, to='cms.cmsplugin')),
                ('heading', models.CharField(choices=[('h1', 'h1'), ('h2', 'h2'), ('h3', 'h3'), ('h4', 'h4'), ('h5', 'h5'), ('h6', 'h6')], default='h2', max_length=2)),
                ('text', models.CharField(max_length=200)),
                ('css_classes', models.CharField(blank=True, max_length=100)),
                ('html_id', models.SlugField(blank=True, max_length=100)),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
    ]
