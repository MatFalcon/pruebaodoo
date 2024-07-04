from odoo import models, fields
from datetime import date, timedelta


class Estate(models.Model):
    _name = "estate.property"
    _description = "Estate Property Plans"

    name = fields.Char("Property Name", required=True)
    description = fields.Text("Property Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date(
        "Date Availibility",
        default=lambda self: date.today() + timedelta(days=90),
        copy=False,
    )
    expected_price = fields.Float("Expected Price", required=True)
    sellig_price = fields.Float(
        "Selling Price", readonly=True, copy=False
    )
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
        string="State",
        selection=[
            ("new", "New"),
            ("offer received", "Offer Received"),
            ("offer accepted", "Offer Accepted"),
            ("sold", "Sold"),
            ("canceled", "Canceled"),
        ],
        required=True,
        copy=False,
        default="new",
    )
