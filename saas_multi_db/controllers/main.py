# -*- coding: utf-8 -*-

import hashlib
import hmac
import logging
from random import sample
from string import ascii_letters, digits
import string
import random
import psycopg2
import sys
import werkzeug
from contextlib import closing
import logging
_logger = logging.getLogger(__name__)
import os
import time
import shutil
import subprocess
from datetime import datetime, timedelta
import xmlrpc.client

from odoo import api, http, registry, SUPERUSER_ID, _
from odoo.http import request

class SaasMultiDB2(http.Controller):

    @http.route('/try/package', type="http", auth="user", website=True)
    def saas_package(self, **kw):
        """Webpage that let's a user select a template database / package"""

        template_databases = request.env['saas.template.database'].search([])
        return http.request.render('saas_multi_db.saas_choose_package', {'template_databases': template_databases})

    @http.route('/try/details', type="http", auth="public", website=True)
    def saas_info(self, **kw):
        """Webpage for users to enter details about thier saas setup"""

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value

        template_database = request.env['saas.template.database'].browse(int(values['templatedb']))
        return http.request.render('saas_multi_db.saas_submit', {'template_database': template_database, 'countries': request.env['res.country'].search([]) })

    @http.route('/vuente/saas/login', type="http", auth="public", website=True)
    def vuente_saas_login(self, **kwargs):
        """Login form for Saas Users"""
        return http.request.render('saas_multi_db.vuente_saas_login', {})

    @http.route('/vuente/saas/login/process', type="http", auth="public", website=True)
    def vuente_saas_login_process(self, **kw):
        """Login form process for Saas Users"""

        values = {}
        for field_name, field_value in kw.items():
            values[field_name] = field_value

        redirect_url = ""

        if request.env['saas.database'].sudo().search_count([ ('login','=', values['login']) ]) > 0:
            saas_database = request.env['saas.database'].sudo().search([ ('login','=', values['login']) ])[0]
            redirect_url = "http://" + saas_database.name + ".vuente.com/saas/client/login?user=" + values['login'] + "&password=" + values['password']
        else:
            redirect_url = "/vuente/saas/login"

        return werkzeug.utils.redirect(redirect_url)

    @http.route('/saas/createdb', type="http", auth="public")
    def saas_create_datadb(self, **kwargs):
        """Creates and sets up the new database"""

        values = {}
        for field_name, field_value in kwargs.items():
            values[field_name] = field_value

        email = values["email"]
        password = values["password"]
        system_name = values["system_name"]
        person_name = values["firstname"] + " " + values["lastname"]
        demo = False

        if system_name.isalnum() == False:
            return "Only AlphaNumeric characters allowed"

        if len(system_name) > 30:
            return "Max system name length of 30 exceeded"

        system_name = system_name.replace(" ","")
        system_name = system_name.lower()

        #Get the template database
        template_database = request.env['saas.template.database'].sudo().browse(int(values["package"]))
        chosen_template = template_database.database_name

        if request.env['saas.database'].sudo().search_count([('name', '=', system_name)]) > 0:
            return "This system name has already been used"

        #The page the user is first redirected towards
        if template_database.saas_server_id:
            template_database.saas_server_id.address
            redirect_url = "http://" + system_name + "." + template_database.saas_server_id.address
        else:
            vhost = "successmadeeasier.com"
            redirect_url = "http://" + system_name + "." + vhost

        #Create SAAS Partner
        partner = request.env['res.partner'].sudo().create({'firstname':values['firstname'], 'lastname':values['lastname'] , 'email':email, 'saas_partner': True, 'saas_database': system_name, 'mobile': values['mobile'], 'country_id': int(values['country_id']), 'saas_url': redirect_url, 'saas_password': password})

        ref_email = ""
        if "ref_email" in values:
            ref_email = values['ref_email']

        #Add this database to the saas list
        ftp_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        admin_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        
        request.env['saas.database'].sudo().create({'ref_email': ref_email, 'name':system_name, 'invoice_id': template_database.invoice_id.id, 'partner_id': partner.id, 'login': email, 'password': password, 'template_database_id': template_database.id, 'plan_price': template_database.monthly_price, 'url':redirect_url, 'ftp_password': ftp_password, 'max_size': template_database.max_size, 'saas_server_id': template_database.saas_server_id.id, 'admin_password': admin_password})

        if template_database.saas_server_id:
            saas_server = template_database.saas_server_id
            url = "http://" + saas_server.address
            db = saas_server.database_name
            username = saas_server.admin_username
            password = saas_server.admin_password

            #Login
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

            my_port = models.execute_kw(db, uid, password, 'saas.slave', 'create_new_instance',[self,chosen_template, system_name, person_name, email, password])

            return werkzeug.utils.redirect(template_database.redirect_url)

            request.env.cr.commit()

        if template_database.redirect_url:
            return werkzeug.utils.redirect(template_database.redirect_url)
        else:
            return werkzeug.utils.redirect(redirect_url)