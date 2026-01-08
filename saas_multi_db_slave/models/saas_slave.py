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

import odoo
import odoo.http as http
from odoo.http import request
from odoo import SUPERUSER_ID
from odoo import api, fields, models        
import subprocess

class SaasSlave(models.Model):

    _name = "saas.slave"

    name = fields.Char(string="Name")

    def create_new_instance(self, db_original_name, system_name, person_name, email, password):
        ftp_password = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8))
        #Execute the external script that clones the template instance
        # os.system("sudo /odoo/odoonewinstance "+ system_name +" " + db_original_name + " " + ftp_password)
        cmd = "sudo /odoo/odoonewinstance %s %s %s" % (system_name, db_original_name, ftp_password)
        print('>XXXXxcmd', cmd)
        output = subprocess.check_output(cmd, shell=True)
        #Connect to the new database
        db = odoo.sql_db.db_connect(system_name)

        #Create new registry
        registry = odoo.modules.registry.Registry(system_name)

        #Update the saas user's name, email, login and password
        with registry.cursor() as cr:
            env = api.Environment(cr, SUPERUSER_ID, {})

            saas_user = env['ir.model.data'].get_object('saas_multi_db_client', 'saas_user')
            saas_user.write({'name':person_name, 'email':email, 'login':email, 'password':password})
            cr.commit()

        self.env.cr.commit()

        return True

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