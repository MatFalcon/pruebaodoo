from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "Estate property Type"
    name = fields.Char(required=True)
    _sql_constraints = [
        ('check_unique', 'UNIQUE(name)',
         'Value must be unique.')
    ]