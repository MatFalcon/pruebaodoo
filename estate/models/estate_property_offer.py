from odoo import fields, models, api, exceptions
from odoo.tools.float_utils import float_is_zero


class EstateOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Offer for estate."
    _order = "price desc"

    price = fields.Float(string="Price")

    status = fields.Selection(
        string="Status",
        copy=False,
        selection=[("accepted", "Accepted"), ("refused", "Refused")],
        readonly=True)

    partner_id = fields.Many2one("res.partner", string="Buyer", required=True)

    property_id = fields.Many2one("estate.property", string="Property", required=True)

    property_state = fields.Selection(related="property_id.state")

    validity = fields.Integer(
        default=7,
        string="Validity",
        readonly=False,)

    date_deadline = fields.Date(
        default=fields.Date.today(),
        string="Deadline Date",
        compute="_compute_deadline_date",
        inverse="_compute_validity_time")

    _sql_constraints = [("check_price", "CHECK(price > 0)", "The offer price should be positive.")]

    @api.depends("validity")
    def _compute_deadline_date(self):
        for offer in self:
            offer.date_deadline = fields.Date.add(
                offer.create_date or fields.Date.today(),
                days=offer.validity)

    @api.onchange("date_deadline")
    def _compute_validity_time(self):
        for offer in self:
            delta = offer.date_deadline - fields.Date.to_date(offer.create_date or fields.Date.today())
            offer.validity = delta.days

    @api.constrains("price")
    def _check_min_offer_price(self):
        for offer in self:
            if float_is_zero(offer.price, 2):
                raise exceptions.ValidationError("The price cannot be null.")
            if offer.price < offer.env["estate.property"].search([("id", "=", offer.property_id.id)]).expected_price * 0.9:
                raise exceptions.ValidationError("The offer price must be greater than 90% of the expected price.")

    def _set_offer_status(self):
        for offer in self.env["estate.property.offer"].search([("property_id", "=", self.property_id.id)]):
            if offer.id != self.id:
                offer.status = "refused"

    def accept_offer(self):
        self.status = "accepted"
        id = self.property_id
        self.env["estate.property"].search([("id", "=", id.id)]).buyer_id = self.partner_id
        self.env["estate.property"].search([("id", "=", id.id)]).selling_price = self.price
        self.env["estate.property"].search([("id", "=", id.id)]).state = "offer_accepted"
        self._set_offer_status()
        return True

    def refuse_offer(self):
        self.status = "refused"
        return True
