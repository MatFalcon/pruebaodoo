from odoo import fields, models


class users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many(
        comodel_name="estate.property",
        inverse_name="salesperson_id",
        domain=[("state", "in", ["new", "offer_received"])],
    )
