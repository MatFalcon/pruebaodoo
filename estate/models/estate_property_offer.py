from odoo import api, fields, models
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Properties Offers defined"

    price = fields.Float(string="Price")
    status = fields.Selection(string="Status", selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string="Partner Id", required=True)
    property_id = fields.Many2one("estate.property", string="Property Id", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline", inverse="_inverse_deadline", store=True)

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = datetime.now() + timedelta(days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.date_deadline:
                record.validity = relativedelta(record.date_deadline, datetime.now()).days
            else:
                record.validity = 0
