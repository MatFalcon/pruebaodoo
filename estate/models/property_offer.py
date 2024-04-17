from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from datetime import date

class PropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offers"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')]
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity", "create_date")
    def _compute_deadline(self):
        for offer in self:
            if offer.create_date:
                offer.date_deadline = offer.create_date + relativedelta(days=offer.validity)
            else:
                offer.date_deadline = date.today() + relativedelta(days=offer.validity)

    def _inverse_deadline(self):
        for offer in self:
            offer.validity = (offer.date_deadline - offer.create_date.date()).days