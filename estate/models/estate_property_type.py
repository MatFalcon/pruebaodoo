from odoo import models, fields, api


class PropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"

    name = fields.Char(string='Name',
                       required=True,
                       help='This is the estate property type.')

    _sql_constraints = (
        ('unique_name', 'UNIQUE(name)',
         'Type name should be unique'),
    )

    property_ids = fields.One2many("estate.property", "property_type_id")

    sequence = fields.Integer()
    _order = "sequence, name"

    offer_ids = fields.One2many("estate.property.offer", "property_type_id")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)
