# -*- coding: utf-8 -*-
import logging
_logger = logging.getLogger(__name__)
import zipfile
import os
from os import walk
from contextlib import closing
import shutil
import datetime
import json
import tempfile
import base64

import openerp
from openerp import api, fields, models

class SaasServer(models.Model):

    _name = "saas.server"
    _description = "Saas Server"

    name = fields.Char(string="Name", help="Human meaningful name")
    address = fields.Char(string="Hostname", help="URL of the slave server without http or www")
    database_name = fields.Char(string="Database Name", help="Name of the SaaS Slave database", default="saas_slave")
    admin_username = fields.Char(string="Admin Username")
    admin_password = fields.Char(string="Admin Password")