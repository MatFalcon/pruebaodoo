from odoo import fields, models, api


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate."

    price = fields.Float(string="Price")

    status = fields.Selection(
            string="Status",
            copy=False,
            selection=[("accepted", "Accepted"), ("refused", "Refused")])

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    property_id = fields.Many2one(
            "estate.property", string="Property", required=True)

    validity = fields.Integer(
            default=7,
            string="Validity",
            inverse="_getValidityTime")

    date_deadline = fields.Date(
            default=fields.Date.today(),
            string="Deadline Date",
            compute="_getDeadlineDate")

    @api.depends("validity", "date_deadline")
    def _getDeadlineDate(self):
        for record in self:
            record.date_deadline = fields.Date.add(
                    record.create_date,
                    days=record.validity)
