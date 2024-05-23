from odoo import fields, models, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare

class EstatePropertyOffer(models.Model):
    _name = 'estate.property.offer'
    _description = 'The property Offer'
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline Date",
        compute='_compute_date_deadline',
        inverse='_inverse_date_deadline',
    )
    price = fields.Float()
    status = fields.Selection(
        [('accepted', "Accepted"), ('refused', "Refused")], copy=False
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one('estate.property', string="Property", required=True)

    _sql_constraints = [
        ('price', 'CHECK(price > 0)', "The price must be strictly positive."),
    ]
    
    @api.depends('create_date', 'validity')
    def _compute_date_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = fields.Date.add(
                    record.create_date, days=record.validity
                )
            else:
                record.date_deadline = fields.Date.add(
                    fields.Date.today(), days=record.validity
                )
    @api.depends('create_date', 'validity')          
    def _inverse_date_deadline(self):
        for record in self:
            if record.date_deadline and record.create_date:
                delta = record.date_deadline - record.create_date.date()
                record.validity = delta.days
            elif record.date_deadline:
                delta = record.date_deadline - fields.Date.today()
                record.validity = delta.days
    def action_accept(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("Cannot accept offers for sold properties.")
            price_dif = float_compare(record.price, 0.9 * record.property_id.expected_price, precision_digits=2)
            if price_dif == -1 :
                raise ValidationError("The selling price cannot be lower than 90% of the expected price.")
            record.status = 'accepted'
            record.property_id.write({
                'state': 'sold',
                'buyer_id': record.partner_id.id,
                'selling_price': record.price
            })
        return True
    def action_refuse(self):
        for record in self:
            if record.property_id.state == 'sold':
                raise UserError("Cannot accept offers for sold properties.")
            record.status = 'refused'
        return True