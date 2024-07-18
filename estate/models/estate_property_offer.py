from odoo import fields, models, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'Estate Property Offer'
    _sql_constraints = [
        ('price_positive', 'CHECK (price > 0)', 'Price should be positive'),
    ]
    _order = 'price desc'

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[('accepted', "Accepted"), ('rejected', "Rejected")],
        copy=False,
    )
    partner_id = fields.Many2one('res.partner', string="Partner ID", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)
    validity = fields.Integer(string="Validity", default=7)
    date_deadline = fields.Date(string="Date Deadline", compute='_compute_date_deadline',
                                inverse='_inverse_date_deadline')
    property_type_id = fields.Many2one(related='property_id.property_type_id', string="Property Type", store=True)

    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(record.create_date, days=record.validity)
            else:
                record.date_deadline = fields.Date.add(fields.Date.today(), days=record.validity)

    @api.onchange('date_deadline')
    def _inverse_date_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept_offer(self):
        for record in self:
            # Check if there are other offers already accepted
            offers = record.property_id.offer_ids
            sold = False
            for offer in offers:
                if offer.status == 'accepted':
                    sold = True

            if sold:
                raise UserError("There are other offers already accepted")

            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.status = 'accepted'

        return True

    def action_refuse_offer(self):
        for record in self:
            record.property_id.selling_price = record.price
            record.property_id.buyer_id = record.partner_id
            record.status = 'rejected'
        return True
