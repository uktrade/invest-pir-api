# -*- coding: utf-8 -*-
# Generated by Django 1.11.11 on 2018-04-26 17:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('investment_report', '0005_auto_20180426_1647'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='calltoaction',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='calltoaction',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='calltoaction',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='calltoaction',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='calltoaction',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='contact',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='frontpage',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='frontpage',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='frontpage',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='frontpage',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='frontpage',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='killerfacts',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='killerfacts',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='killerfacts',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='killerfacts',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='killerfacts',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='macrocontextbetweencountries',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='macrocontextbetweencountries',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='macrocontextbetweencountries',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='macrocontextbetweencountries',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='macrocontextbetweencountries',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='networkandsupport',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='networkandsupport',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='networkandsupport',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='networkandsupport',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='networkandsupport',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='rdandinnovation',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='rdandinnovation',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='rdandinnovation',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='rdandinnovation',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='rdandinnovation',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='rdandinnovationcasestudy',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='rdandinnovationcasestudy',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='rdandinnovationcasestudy',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='rdandinnovationcasestudy',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='rdandinnovationcasestudy',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='sectorinitiatives',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sectorinitiatives',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='sectorinitiatives',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='sectorinitiatives',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='sectorinitiatives',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='sectoroverview',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='sectoroverview',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='sectoroverview',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='sectoroverview',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='sectoroverview',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='servicesofferedbydit',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='servicesofferedbydit',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='servicesofferedbydit',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='servicesofferedbydit',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='servicesofferedbydit',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='talentandeducationbysector',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='talentandeducationbysector',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='talentandeducationbysector',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='talentandeducationbysector',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='talentandeducationbysector',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='talentandeducationgeneric',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='talentandeducationgeneric',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='talentandeducationgeneric',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='talentandeducationgeneric',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='talentandeducationgeneric',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='testimonials',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='testimonials',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='testimonials',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='testimonials',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='testimonials',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='ukbusinessinfo',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ukbusinessinfo',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='ukbusinessinfo',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='ukbusinessinfo',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='ukbusinessinfo',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='ukgeographicoverview',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ukgeographicoverview',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='ukgeographicoverview',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='ukgeographicoverview',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='ukgeographicoverview',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='ukmarketoverview',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='ukmarketoverview',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='ukmarketoverview',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='ukmarketoverview',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='ukmarketoverview',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='videocasestudy',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='videocasestudy',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='videocasestudy',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='videocasestudy',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='videocasestudy',
            name='submitted',
        ),
        migrations.RemoveField(
            model_name='whoishere',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='whoishere',
            name='date_approved',
        ),
        migrations.RemoveField(
            model_name='whoishere',
            name='date_created',
        ),
        migrations.RemoveField(
            model_name='whoishere',
            name='date_rejected',
        ),
        migrations.RemoveField(
            model_name='whoishere',
            name='submitted',
        ),
        migrations.AddField(
            model_name='calltoaction',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.CallToAction'),
        ),
        migrations.AddField(
            model_name='contact',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.Contact'),
        ),
        migrations.AddField(
            model_name='frontpage',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.FrontPage'),
        ),
        migrations.AddField(
            model_name='killerfacts',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.KillerFacts'),
        ),
        migrations.AddField(
            model_name='macrocontextbetweencountries',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.MacroContextBetweenCountries'),
        ),
        migrations.AddField(
            model_name='networkandsupport',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.NetworkAndSupport'),
        ),
        migrations.AddField(
            model_name='rdandinnovation',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.RDandInnovation'),
        ),
        migrations.AddField(
            model_name='rdandinnovationcasestudy',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.RDandInnovationCaseStudy'),
        ),
        migrations.AddField(
            model_name='sectorinitiatives',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.SectorInitiatives'),
        ),
        migrations.AddField(
            model_name='sectoroverview',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.SectorOverview'),
        ),
        migrations.AddField(
            model_name='servicesofferedbydit',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.ServicesOfferedByDIT'),
        ),
        migrations.AddField(
            model_name='talentandeducationbysector',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.TalentAndEducationBySector'),
        ),
        migrations.AddField(
            model_name='talentandeducationgeneric',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.TalentAndEducationGeneric'),
        ),
        migrations.AddField(
            model_name='testimonials',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.Testimonials'),
        ),
        migrations.AddField(
            model_name='ukbusinessinfo',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.UKBusinessInfo'),
        ),
        migrations.AddField(
            model_name='ukgeographicoverview',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.UKGeographicOverview'),
        ),
        migrations.AddField(
            model_name='ukmarketoverview',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.UKMarketOverview'),
        ),
        migrations.AddField(
            model_name='videocasestudy',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.VideoCaseStudy'),
        ),
        migrations.AddField(
            model_name='whoishere',
            name='active_draft',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='investment_report.WhoIsHere'),
        ),
    ]
