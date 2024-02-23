from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Property offer model"


    price = fields.Float()
    status = fields.Selection(
        copy=False,
        string = 'Status',
        selection = [
            ('accepted', 'Accepted'), 
            ('refused', 'Refused')
        ]
    )
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            record.date_deadline = fields.Date.add(fields.Date.context_today(record, timestamp=record.create_date),days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - fields.Date.context_today(record, timestamp=record.create_date)).days

    def action_accept(self):
        for record in self:
            if record.property_id.state == "offer_accepted":
                raise UserError("Another offer was already accepted")
            else:
                record.status = "accepted"
                record.property_id.state = "offer_accepted"
                record.property_id.buyer_id = record.partner_id
                record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.state == "offer_accepted" and record.status == "accepted":
                record.property_id.state = "offer_received"
                record.property_id.buyer_id = None
                record.property_id.selling_price = None
            record.status = "refused"
        return True
