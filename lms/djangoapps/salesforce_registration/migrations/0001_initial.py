# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'SalesforceDomainEntry'
        db.create_table('salesforce_registration_salesforcedomainentry', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('category', self.gf('django.db.models.fields.CharField')(default='', max_length=255)),
            ('domain', self.gf('django.db.models.fields.CharField')(default='', unique=True, max_length=255)),
        ))
        db.send_create_signal('salesforce_registration', ['SalesforceDomainEntry'])


    def backwards(self, orm):
        # Deleting model 'SalesforceDomainEntry'
        db.delete_table('salesforce_registration_salesforcedomainentry')


    models = {
        'salesforce_registration.salesforcedomainentry': {
            'Meta': {'object_name': 'SalesforceDomainEntry'},
            'category': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '255'}),
            'domain': ('django.db.models.fields.CharField', [], {'default': "''", 'unique': 'True', 'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['salesforce_registration']