from odoo import models, fields, api

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float()
    status = fields.Selection(
        copy=False,
        selection=[
            ('accepted', 'Accepted'),
            ('refused', 'Refused')
        ]
    )
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline_date", inverse="_inverse_deadline_date" ,string="Deadline")

    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)

    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = record.create_date if record.create_date else fields.Date.today()
            initial_date = fields.Date.to_date(initial_date)
            record.validity = (record.date_deadline - initial_date).days
