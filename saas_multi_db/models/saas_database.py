# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
from datetime import datetime, timedelta
import time

from openerp import api, fields, models
import openerp.http as http
from openerp.http import request
import os
import openerp
import werkzeug.wrappers

class SaasDatabase(models.Model):

    _name = "saas.database"

    ref_email = fields.Char(string="Ref Email")
    saas_server_id = fields.Many2one('saas.server', string="Saas Server", help="The server the database resides on")
    name = fields.Char(string="Database Name", required=True)
    partner_id = fields.Many2one('res.partner', string="Database Partner")
    login = fields.Char(string="Login")
    password = fields.Char(string="Password")
    admin_password = fields.Char(string="Admin Pasword")
    state = fields.Selection([('draft','Draft'), ('active','Active')], default="draft", string="State")
    next_invoice_date = fields.Datetime(string="Next Invoice Date")
    template_database_id = fields.Many2one('saas.template.database', string="Template Database", ondelete="SET NULL")
    plan_price = fields.Float(string="Plan Price", help="The price of the plan at the time of purchase")
    url = fields.Char(string="URL")
    ftp_password = fields.Char(string="FTP Password")
    subscribed = fields.Boolean(string="Subscribed")
    invoice_id = fields.Many2one('account.invoice', string="Template Invoice")
    backup_ids = fields.One2many('ir.attachment', 'saas_database_id', string="Backups")
    database_size = fields.Integer(help="Expressed in bytes")
    database_size_format = fields.Char(string="Database Size", help="Human formatted size of the database")
    directory_size = fields.Integer(help="Expressed in bytes")
    directory_size_format = fields.Char(string="Directory Size", help="Human formatted size of all files in the Odoo directory")
    total_size = fields.Integer(help="Expressed in bytes")
    total_size_format = fields.Char(string="Total Size", help="Human formatted size of the database and Directory")
    max_size = fields.Float(string="Max Size(MB)")
    log_file_content = fields.Text(string="Log File Content")

    def open_log_file(self):
        log_file_path = "/var/log/" + self.name + "/" + self.name + "-server.log"
        log_file_content = open(log_file_path,"r").read()
        self.log_file_content = log_file_content.replace("\x00","")[-100000:]

    @api.model
    def saas_check_storage(self):
        for saas_database in self.env['saas.database'].search([]):

            try:
                # Get database size
                database_name = saas_database.name
                self.env.cr.execute("SELECT pg_database_size(%s)", [database_name])
                database_size = self.env.cr.fetchone()[0]
                saas_database.database_size = database_size
                saas_database.database_size_format = self.format_size(database_size)

                # Get directory size
                odoo_directory = "/opt/" + database_name
                odoo_directory_size = 0
                for dirpath, dirnames, filenames in os.walk(odoo_directory):
                    for f in filenames:
                        fp = os.path.join(dirpath, f)
                        odoo_directory_size += os.path.getsize(fp)

                saas_database.directory_size = odoo_directory_size
                saas_database.directory_size_format = self.format_size(odoo_directory_size)

                # Combine the sizes together
                saas_database.total_size = database_size + odoo_directory_size
                saas_database.total_size_format = self.format_size(database_size + odoo_directory_size)
            except:
                _logger.error("saas storage calc failed")

    def format_size(self, size):
        power = 2**10
        n = 0
        Dic_powerN = {0 : '', 1: 'K', 2: 'M', 3: 'G', 4: 'T'}
        while size > power:
            size /=  power
            n += 1
        return str(int(size)) + Dic_powerN[n]+'B'

    @api.onchange('subscribed')
    def _onchange_subscribed(self):
        if self.subscribed:
            self.next_invoice_date = datetime.utcnow() + timedelta(days=30)
        else:
            self.next_invoice_date = ""

    @api.model
    def invoice_members(self):
        invoice_partners = self.env['saas.database'].search([('subscribed','=', True), ('next_invoice_date', '<=', datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") )])
        #invoice_template = self.env['ir.model.data'].get_object('account', 'email_template_edi_invoice')

        for inv_saas in invoice_partners:
            #Create a new invoice
            invoice_email_template = self.env['ir.model.data'].get_object('account', 'email_template_edi_invoice')
            template_invoice = inv_saas.invoice_id

            #journal_id = self.env['account.journal'].search([('type','=','sale'),('company_id','=',self.env.user.company_id.id)])         
            #new_invoice = self.env['account.invoice'].sudo().create({'partner_id':inv_saas.partner_id.id, 'type':'out_invoice', 'journal_type': 'sale','account_id':journal_id.default_debit_account_id.id})

            #Create the line in the invoice for the system "product"
            #self.env['account.invoice.line'].create({'invoice_id': new_invoice.id, 'account_id': journal_id.default_debit_account_id.id, 'name':inv_saas.template_database_id.name + " System",'quantity':1,'price_unit':inv_saas.plan_price})

            new_invoice = template_invoice.copy()

            #Change the invoice so it to the partner
            new_invoice.partner_id = inv_saas.partner_id.id

            #Validate the invoice
            new_invoice.action_date_assign()
            new_invoice.action_move_create()
            new_invoice.invoice_validate()

            #Email the invoice and pray they pay
            invoice_email_template.send_mail(new_invoice.id, True)

            #Set thier next invoice to be 30 from the previous invoice
            inv_saas.next_invoice_date = datetime.strptime(inv_saas.next_invoice_date,"%Y-%m-%d %H:%M:%S") + timedelta(days=30)

    def saas_database_backup(self):
        backup_folder = "/saas_database_backups"

        #Try to create the directory if it currently doesn't exist
        if not os.path.isdir(backup_folder):
            os.makedirs(backup_folder)

        backup_file_name = '%s-%s' % (self.name, time.strftime('%d_%m_%Y_%H_%M_%S') )
        backup_file_path = os.path.join(backup_folder,backup_file_name)
        backup_format = "zip"

        headers = [
            ('Content-Type', 'application/octet-stream; charset=binary'),
            ('Content-Disposition', self.content_disposition(backup_file_name)),
        ]

        dump_stream = openerp.service.db.dump_db(self.name, None, backup_format)

        response = werkzeug.wrappers.Response(dump_stream, headers=headers, direct_passthrough=True)
        #return response

    def content_disposition(self, filename):
        return self.env['ir.http'].content_disposition(filename)

    def login_to_saas_user(self):
        request.session.authenticate(self.name, self.login, self.password)

        return http.local_redirect('/web/')