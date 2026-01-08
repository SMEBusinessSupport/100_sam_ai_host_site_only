# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
import zipfile
import sys
import os
from os import walk
from contextlib import closing
import shutil
import datetime
import json
import tempfile
import base64
import string
import random
import xmlrpc.client
import subprocess

import openerp
from odoo import api, fields, models, registry, SUPERUSER_ID, _

class SaasTemplateDatabase(models.Model):

    _name = "saas.template.database"
    _description = "Preconfigured databases that the website user can select from"""
    _order = "sequence asc"

    @api.model
    def _default_saas_database_model_id(self):
        return self.env['ir.model'].search([('model','=','saas.database')])[0].id

    @api.model
    def _default_saas_database_create_date_field_id(self):
        return self.env['ir.model.fields'].search([('model','=','saas.database'), ('name','=','create_date')])[0].id

    redirect_url = fields.Char(string="Redirect URL")
    sequence = fields.Integer(string="Sequence")
    name = fields.Char(string="Display Name", help="Displayed on the website")
    database_name = fields.Char(string="Database Name", help="The name of the template database in psql")
    image = fields.Binary(string="Image")
    description = fields.Char(string="Description", default="Placeholder description")
    monthly_price = fields.Float(string="Monthly Price", help="The monthly fee the user pays to rent the system")
    create_instance = fields.Boolean(string="Create New Instance")
    invoice_id = fields.Many2one('account.invoice', string="Template Monthly Invoice")
    saas_database_ids = fields.One2many('saas.database', 'template_database_id', string="SAAS Databases")
    auto_backup = fields.Boolean(string="Auto Backup")
    auto_backup_days_to_keep = fields.Integer(string="Auto Backup Days to Keep", default="7")
    max_size = fields.Float(string="Max Size(MB)", default="4096")
    saas_server_id = fields.Many2one('saas.server', string="Saas Server", help="The server which will house the database")
    saas_database_model_id = fields.Integer(string="Saas Database Model ID", default=_default_saas_database_model_id)
    saas_database_create_date_field_id = fields.Integer(string="Saas Database Create Date Field ID", default=_default_saas_database_create_date_field_id)
    automated_actions_ids = fields.Many2many('base.automation', string="Automated Actions")

    @api.model
    def saas_create_database(self):
    
        for draft_database in self.env['saas.database'].search([('state', '=', 'draft')]):
            #Local Create new instance
            db_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
            #os.system("sudo /odoo/odoonewinstance " + draft_database.name +" " + draft_database.template_database_id.database_name + " " + draft_database.ftp_password + " " + db_password)
            cmd = "sudo /odoo/odoonewinstance %s %s %s %s" % (draft_database.name, draft_database.template_database_id.database_name, draft_database.ftp_password, db_password)
            output = subprocess.check_output(cmd, shell=True)

            # script_output = os.popen("sudo /odoo/odoonewinstance " + draft_database.name +" " + draft_database.template_database_id.database_name + " " + draft_database.ftp_password + " " + db_password).read()
            # _logger.error(script_output)

            #Update the saas user's name, email, login and password
            db_registry = registry(draft_database.name)
            with db_registry.cursor() as cr:

                my_env = api.Environment(cr, SUPERUSER_ID, {})

                #Change Saas User Details
                saas_user = my_env['ir.model.data'].get_object('saas_multi_db_client', 'saas_user')
                saas_user.write({'name': draft_database.partner_id.firstname + " " + draft_database.partner_id.lastname, 'email': draft_database.login, 'login': draft_database.login, 'password': draft_database.password})

                #Change Admin Password
                admin_user = my_env['ir.model.data'].get_object('base','user_root')
                admin_user.write({'password': draft_database.admin_password})

                cr.commit()

                draft_database.state = "active"
                
                # Send out email
                saas_new_database_template = self.env['ir.model.data'].sudo().get_object('saas_multi_db', 'saas_new_database')
                saas_new_database_template.send_mail(draft_database.id, True)

    @api.model
    def saas_auto_backup(self):

        for saas_database in self.env['saas.database'].search([]):
            for backup in saas_database.backup_ids:
                if backup.create_date < (datetime.datetime.now() - datetime.timedelta(days=template_database.auto_backup_days_to_keep) ).strftime("%Y-%m-%d %H:%M:%S"):
                    backup.unlink()

            with openerp.tools.osutil.tempdir() as dump_dir:
                try:
                    _logger.error(saas_database.name)
                    db_name = saas_database.name
                    filestore = openerp.tools.config.filestore(db_name)

                    if os.path.exists(filestore):
                        shutil.copytree(filestore, os.path.join(dump_dir, 'filestore'))

                    with open(os.path.join(dump_dir, 'manifest.json'), 'w') as fh:
                        db = openerp.sql_db.db_connect(db_name)
                        with db.cursor() as cr:
                            json.dump(self.dump_db_manifest(cr), fh, indent=4)

                    cmd = ['pg_dump', '--no-owner']
                    cmd.append(db_name)
                    cmd.insert(-1, '--file=' + os.path.join(dump_dir, 'dump.sql'))
                    openerp.tools.exec_pg_command(*cmd)

                    t=tempfile.TemporaryFile()
                    openerp.tools.osutil.zip_dir(dump_dir, t, include_dir=False, fnct_sort=lambda file_name: file_name != 'dump.sql')

                    t.seek(0)

                    save_name = db_name + ' ' +  datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ' Backup'
                    file_name = db_name + ' ' +  datetime.datetime.now().strftime('%Y-%m-%d %H-%M-%S') + '.zip'

                    #attachment = self.env['ir.attachment'].create({'name': save_name, 'mimetype': 'application/zip', 'datas_fname': file_name, 'type': 'binary', 'datas': base64.b64encode( t.read() ) , 'description': 'Automatic backup of ' + db_name + ' ' + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'res_model': 'saas.database', 'res_id':  saas_database.id, 'res_name': save_name, 'saas_database_id': saas_database.id})

                    with open("/opt/backups/" + str(file_name), "wb") as fh:
                        fh.write( t.read() )

                    if saas_database.saas_server_id:
                        _logger.error("saas master remote backup")
                        saas_server = saas_database.saas_server_id
                        url = "http://" + saas_server.address
                        db = saas_server.database_name
                        username = saas_server.admin_username
                        password = saas_server.admin_password

                        #Login
                        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
                        uid = common.authenticate(db, username, password, {})
                        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

                        models.execute_kw(db, uid, password, 'saas.slave', 'saas_database_backup',[self,saas_database.name])		    

                except Exception as e:
                    exc_type, exc_obj, exc_tb = sys.exc_info()
                    _logger.error(e)
                    _logger.error("Line: " + str(exc_tb.tb_lineno) )
                    _logger.error(str(db_name) + " Backup Error")

    @api.model
    def dump_db_manifest(self, cr):
        pg_version = "%d.%d" % divmod(cr._obj.connection.server_version / 100, 100)
        cr.execute("SELECT name, latest_version FROM ir_module_module WHERE state = 'installed'")
        modules = dict(cr.fetchall())
        manifest = {
            'odoo_dump': '1',
            'db_name': cr.dbname,
            'version': openerp.release.version,
            'version_info': openerp.release.version_info,
            'major_version': openerp.release.major_version,
            'pg_version': pg_version,
            'modules': modules,
        }
        return manifest

    @api.model
    def create(self, values):
        sequence=self.env['ir.sequence'].get('sequence')
        values['sequence']=sequence
        return super(SaasTemplateDatabase, self).create(values)

    def save_template(self):
        db_original_name = self.database_name
        db_name = db_original_name + "_clone"

        openerp.sql_db.close_db(db_original_name)
        db = openerp.sql_db.db_connect('postgres')

        with closing(db.cursor()) as cr:
            cr.autocommit(True)     # avoid transaction block
            self._drop_conn(cr, db_original_name)

            #Check if the database already exists
            cr.execute("SELECT datname FROM pg_database WHERE datname = %s",(db_name,))
            if cr.fetchall():
                cr.execute("""DROP DATABASE "%s" """ % (db_name,))

            cr.execute("""CREATE DATABASE "%s" ENCODING 'unicode' TEMPLATE "%s" """ % (db_name, db_original_name))

        from_fs = openerp.tools.config.filestore(db_original_name)
        to_fs = openerp.tools.config.filestore(db_name)

        if os.path.exists(from_fs) and not os.path.exists(to_fs):
            shutil.copytree(from_fs, to_fs)

    def _drop_conn(self, cr, db_name):
        # Try to terminate all other connections that might prevent
        # dropping the database
        try:
            # PostgreSQL 9.2 renamed pg_stat_activity.procpid to pid:
            # http://www.postgresql.org/docs/9.2/static/release-9-2.html#AEN110389
            pid_col = 'pid' if cr._cnx.server_version >= 90200 else 'procpid'

            cr.execute("""SELECT pg_terminate_backend(%(pid_col)s)
                          FROM pg_stat_activity
                          WHERE datname = %%s AND
                                %(pid_col)s != pg_backend_pid()""" % {'pid_col': pid_col},
                       (db_name,))
        except Exception:
            pass