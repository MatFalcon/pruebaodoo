from odoo import api, fields, models
from odoo.exceptions import UserError
from odoo.tools.date_utils import add
from odoo.tools.translate import _


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "description"
    _order = "price desc"

    price = fields.Float("Price")
    status = fields.Selection(
        copy=False,
        string="Status",
        selection=[
            ('accepted', "Accepted"),
            ('refused', "Refused"),
        ],
    )
    partner_id = fields.Many2one('res.partner', string="Partner", required=True)
    property_id = fields.Many2one(
        'estate.property',
        string="Property",
        required=True,
    )
    property_type_id = fields.Many2one(
        related='property_id.property_type_id', string="Property Type", store=True
    )

    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute='_compute_deadline', inverse="_inverse_deadline")

    _sql_constraints = [
        (
            'check_offer_price',
            'CHECK(price > 0)',
            'An offer price must be strictly positive.',
        )
    ]

    @api.depends('validity', 'create_date')
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = add(record.create_date, days=record.validity)
            else:
                record.date_deadline = add(fields.Date.today(), days=record.validity)

    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline - record.create_date.date()).days
            else:
                record.validity = (record.date_deadline - fields.Date.today()).days

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.update({'buyer': self.partner_id, 'selling_price': self.price})
        for record in self.property_id.offer_ids:
            if record != self:
                record.status = 'refused'

        return True

    def action_refuse(self):
        self.status = 'refused'
        self.property_id.update({'buyer': None, 'selling_price': 0.00001})

        return True

    @api.model
    def create(self, vals):
        property = self.env['estate.property'].browse(vals['property_id'])

        if any([vals['price'] < offer.price for offer in property.offer_ids]):
            raise UserError(_("Offer cannot be cheaper than existing ones."))

        property.state = 'offer_received'

        return super().create(vals)
