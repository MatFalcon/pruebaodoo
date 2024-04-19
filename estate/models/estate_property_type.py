from odoo import fields, models  # type: ignore


class EstatePropertyType(models.Model):
    _name = "estate_property_type"
    _description = "estate property type"

    name = fields.Char(string="Type", required=True)
    property_ids = fields.One2many("estate_property", "estate_property_type_id")

    _sql_constraints = [
                     ('unique_name',
                      'unique(name)',
                      'Choose another value - it has to be unique!')
    ]
