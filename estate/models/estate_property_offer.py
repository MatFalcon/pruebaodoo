from dateutil.relativedelta import relativedelta
from odoo import api, fields, models


class PropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer Model"

    price = fields.Float('Price')
    status = fields.Selection(
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        copy=False
    )
    partner_id = fields.Many2one('res.partner', required=True)
    property_id = fields.Many2one('estate.property', required=True)
    validity = fields.Integer('Validity', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_date_deadline', inverse='_inverse_date_deadline')

    @api.depends('validity')
    def _compute_date_deadline(self):
        for record in self:
            create_date = fields.Datetime.today()
            if record.create_date:
                create_date = record.create_date
            record.date_deadline = create_date + relativedelta(days=record.validity)

    def _inverse_date_deadline(self):
        for record in self:
            record.validity = (record.date_deadline - record.create_date.date()).days
