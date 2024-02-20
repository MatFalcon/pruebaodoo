from odoo import api, fields, models
import datetime

class EstateModel(models.Model):
    _name = "estate.property.offer"
    _description = "Estate/Property/Offer"

    price = fields.Float(required=True)
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused")
    ])
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline", inverse="_inverse_deadline")

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date is None:
                record.date_deadline = record.create_date.add(days=record.validity)
            else:
                record.date_deadline = datetime.date.today() + datetime.timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            delta = record.date_deadline - record.create_date.date()
            record.validity = delta.days 
