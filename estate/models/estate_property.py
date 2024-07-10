from odoo import models, fields, api, exceptions
from datetime import date, timedelta


class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate Property Plans"

    name = fields.Char(required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Date Availibility",
        default=lambda self: date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ("north", "North"),
            ("south", "South"),
            ("east", "East"),
            ("west", "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="Status",
        selection=[
            ("new", "New"),
            ("offer_received", "Offer Received"),
            ("offer_accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("cancelled", "Cancelled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        inverse_name="property_id",
        string="Property Type"
    )
    salesperson_id = fields.Many2one("res.users", string="Sales Person", default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", string="Buyer", copy=False)
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tags",
        string="Property Tag"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string="Property Offer"
    )
    total_area = fields.Integer(compute="_compute_totalarea")
    best_price = fields.Integer("Best Offer", compute="_compute_bestprice")

    @api.depends("living_area", "garden_area")
    def _compute_totalarea(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids")
    def _compute_bestprice(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped("price"), default=0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_cancel(self):
        for record in self:
            if record.state == 'sold':
                raise exceptions.UserError("Cannot cancel a property that is already sold!")
            record.state = 'cancelled'

    def action_sold(self):
        for record in self:
            if record.state == 'cancelled':
                raise exceptions.UserError("Cannot sell a property that is already cancelled!")
            record.state = 'sold'
