from odoo import models, fields, api
from datetime import timedelta
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):

    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = 'price desc'

    price = fields.Float(string='Price', required=True)
    status = fields.Selection(string='Status',
                              selection=[
                                  ('accepted', 'Accepted'),
                                  ('refused', 'Refused')]
                              )
    partner_id = fields.Many2one(
        comodel_name="res.partner", string="Partner", copy=False, required=True)
    property_id = fields.Many2one(
        comodel_name="estate.property", string="Property")
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline date", compute="_compute_deadline", inverse="_inverse_deadline")
    property_type_id = fields.Many2one(
        comodel_name='estate.property.type',
        string='Property Type',
        store=True,
        related='property_id.property_type_id',
    )

    _sql_constraints = [
        ('check_price', 'CHECK(price >= 0)',
         'The offer price must be positive.')
    ]

    @api.depends("create_date", "validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date:
                record.date_deadline = record.create_date + \
                    timedelta(days=record.validity)
            else:
                record.date_deadline = fields.datetime.now() + timedelta(days=record.validity)

    @api.depends("create_date", "date_deadline")
    def _inverse_deadline(self):
        for record in self:
            if record.create_date:
                record.validity = (record.date_deadline -
                                   record.create_date.date()).days
            else:
                record.validity = (record.date_deadline -
                                   fields.date.today()).days

    def action_accept(self):
        self.status = 'accepted'
        self.property_id.selling_price = self.price
        self.property_id.partner_id = self.partner_id
        self.property_id.state = 'offer accepted'

    def action_refuse(self):
        self.status = 'refused'

    @api.model
    def create(self, vals):
        property_id = vals.get('property_id')
        price = vals.get('price')
        current_property = self.property_id.browse(property_id)
        current_property.state = 'offer received'

        existing_offers = current_property.offer_ids
        if existing_offers:
            max_amount = max(existing_offers.mapped('price'))
            if price < max_amount:
                raise UserError(
                    "The offer amount cannot be lower than an existing offer.")
        return super().create(vals)
