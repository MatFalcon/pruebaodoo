from odoo import fields, models


class FreightType(models.Model):
    _name = 'freight.type'
    _description = 'Freight Type Model'
    _inherits = {'port.city': 'freight_type_id'}

    freight_type_id = fields.Many2one('port.city')
