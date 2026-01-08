
from odoo import fields, models, api,_

SERVER_TYPE = [
    ('containerized', "Containerized Instance"),
]

HOST_SERVER = [
    ('self', "Self (Same Server)"),
    ('remote', "Remote Server"),
]

DB_SERVER = [
    ('self', "Self (Same Server)"),
    ('remote', "Remote Server"),
]
DB_SCHEME = [
    ('create', "Database creation"),
    ('clone', "Database cloning"),
]

class SaasClientServer(models.Model):
    _name = 'saas.client.server'

    server_id = fields.Many2one('saas.server',string="Saas Server")
    saas_client_id = fields.Many2one('saas.client',string="Saas Client")
    name = fields.Char(string="Plan",related='server_id.name')
    server_type = fields.Selection(
        selection=SERVER_TYPE,
        string="Type",
        required=True,
        default="containerized",
        readonly=True,related='server_id.server_type')
    host_server = fields.Selection(
        selection=HOST_SERVER,
        string="Host Server",
        required=True,
        default="self" ,related='server_id.host_server')
    db_server = fields.Selection(
        selection=DB_SERVER,
        string="Database Host Server",
        required=True,
        default="self",related='server_id.db_server')
    max_clients = fields.Integer(
        string="Maximum Allowed Clients",
        default="10",
        required=True,related='server_id.max_clients')
    total_clients = fields.Integer(
        compute='_compute_total_clients',
        string="No. Of Clients",related='server_id.total_clients')
    db_creation_scheme = fields.Selection(
        selection=DB_SCHEME,
        string="Database Scheme",
        default="create",related='server_id.db_creation_scheme')
    db_host = fields.Char(string="Database Host", default="localhost",related='server_id.db_host')
    db_port = fields.Char(string="Database Port", default="5432",related='server_id.db_port')
    db_user = fields.Char(string="Database Username",related='server_id.db_user')
    db_pass = fields.Char(string="Database Password",related='server_id.db_pass')