from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class propertyTag(models.Model):
    _name = "estate.property.offer"
    _description = "Offers for the Real Estate Property"

    price = fields.Float("Price")
    status = fields.Selection(
        string="Status",
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True, string="Partner")
    property_id = fields.Many2one('estate.property', string="Property")
    validity = fields.Integer("Validity (Days)", default=7)
    date_deadline = fields.Date("Deadline", compute="_deadline_date_count", inverse="_inverse_deadline", store=True)

    @api.depends('validity')
    def _deadline_date_count(self):
        current_date = fields.Date.today()
        for record in self:
            record.date_deadline = current_date + relativedelta(days=record.validity)

    def _inverse_deadline(self):
        current_date = fields.Date.today()
        for record in self:
            record.validity = relativedelta(record.date_deadline, current_date).days

    def action_accepted(self):
        if not self.property_id.buyer:
            self.status = 'accepted'
            self.property_id.selling_price = self.price
            self.property_id.buyer = self.partner_id.name
        else:
            raise UserError("Offer has been already Accepted")
        return True

    def action_refused(self):
        if self.property_id.buyer == self.partner_id.name:
            self.property_id.buyer = ''
        self.status = 'refused'
        return True
