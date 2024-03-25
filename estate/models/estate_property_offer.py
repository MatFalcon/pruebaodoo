from odoo import fields, models, api
from odoo.exceptions import UserError
from datetime import date
from dateutil.relativedelta import relativedelta


class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'An offer for a property'

    price = fields.Float(default=0.0)
    status = fields.Selection([
        ('new', 'New'),
        ('accepted', 'Accepted'),
        ('refused', 'Refused')
    ], default='new', copy=False)

    buyer_id = fields.Many2one('res.partner', string='Buyer', required=True)
    property_id = fields.Many2one('estate.property', string='Property', required=True)

    validity = fields.Integer('Validity (days)', default=7)
    date_deadline = fields.Date('Deadline', compute='_compute_deadline', inverse='_inverse_deadline')

    create_date = fields.Date('Date Created')

    _sql_constraints = [
        ('check_price',
         'CHECK(price > 0)',
         'An offer\'s price must be positive')
    ]

    @api.depends('validity')
    def _compute_deadline(self):
        for record in self:
            record.date_deadline = \
                record.create_date + relativedelta(days=record.validity) \
                    if record.create_date and record.validity != None else None

    def _inverse_deadline(self):
        for record in self:
            if record.create_date and record.date_deadline:
                record.validity = (record.date_deadline - record.create_date).days

    def action_accept(self):
        for record in self:
            if record.property_id.accepted_offer_id.id == record.id:
                continue

            if record.property_id.accepted_offer_id:
                raise UserError('The property already has an accepted offer!')

            record.property_id._accept_offer(record)
            record.status = 'accepted'
        return True

    def action_refuse(self):
        for record in self:
            if record.property_id.accepted_offer_id.id == record.id:
                record.property_id.accepted_offer_id = None

            record.status = 'refused'
        return True
