import datetime

from odoo import models, fields, api
from odoo.exceptions import UserError


class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "real estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string="Status",
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        help="The status determines if the offer has been accepted or refused",
        copy=False,
    )
    partner_id = fields.Many2one("res.partner", string="Partner", required=True)
    property_id = fields.Many2one("estate.property", string="Property", required=True)
    validity = fields.Integer(string="Validity (days)", default=7)
    date_deadline = fields.Date(
        string="Deadline",
        compute="_compute_date_deadline",
        inverse="_inverse_date_deadline",
    )
    property_type_id = fields.Many2one(
        related="property_id.property_type_id", store=True
    )

    _sql_constraints = [
        (
            "check_price",
            "CHECK(price > 0)",
            "The offer price must be a positive number",
        )
    ]

    @api.model
    def create(self, vals):
        property = self.env["estate.property"].browse(vals["property_id"])
        if property.state in ("canceled", "offer accepted", "sold"):
            raise UserError(
                "Offer cannot be created for this property due to the property's status"
            )
        if property.best_price >= vals["price"]:
            raise UserError(
                "Offer cannot have a price lower than any of the existing offers"
            )

        property.state = "offer received"
        return super().create(vals)

    @api.depends("validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Date.today()
            record.date_deadline = create_date + datetime.timedelta(
                days=record.validity
            )

    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date.date() or fields.Date.today()
            record.validity = (record.date_deadline - create_date).days

    def accept_offer(self):
        for record in self:
            property = record.property_id
            if property.state == "sold":
                raise UserError("Property already sold")

            record.status = "accepted"
            property.state = "sold"
            property.selling_price = record.price
            property.buyer_id = record.partner_id
        return True

    def reject_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("Offer has already been accepted")
            record.status = "refused"
        return True
