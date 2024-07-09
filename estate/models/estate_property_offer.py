from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import timedelta


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float(string='Price')
    status = fields.Selection(string='Status', selection=[('accepted', 'Accepted'), ('refused', 'Refused')], copy=False)
    partner_id = fields.Many2one("res.partner", string='Partner', required=True)
    property_id = fields.Many2one("estate.property", string='Property', required=True)
    validity = fields.Integer(string='Validity', default=7)
    date_deadline = fields.Date(string='Date deadline', compute="_compute_date_deadline", inverse="_inverse_date_deadline", store=True)

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.validity:
                current_date = fields.Date.today()
                expiration_date = current_date + timedelta(days=record.validity)
                record.date_deadline = expiration_date
            else:
                record.date_deadline = fields.Date.today()

    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline:
                current_date = fields.Date.today()
                validity_days = (record.date_deadline - current_date).days
                record.validity = validity_days
            else:
                record.validity = 0

    def action_accept(self):
        if not self.property_id.buyer:
            self.status = "accepted"
            self.property_id.selling_price = self.price
            self.property_id.buyer = self.partner_id
        else:
            raise UserError("Offer is already accepted")

    def action_refuse(self):
        self.property_id.buyer = ''
        self.status = "refused"
