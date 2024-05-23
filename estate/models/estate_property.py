from odoo import api, fields, models
from odoo.tools.date_utils import add


class EstateProperty(models.Model):
    _name = 'estate.property'
    _description = "estate properties"

    name = fields.Char("Title", required=True)
    description = fields.Text("Description")
    postcode = fields.Integer("Postcode")
    date_availability = fields.Date(
        "Available from", copy=False, default=add(fields.Date.today(), months=3)
    )
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(
        string="Garden Orientation",
        selection=[
            ('north', "North"),
            ('south', "South"),
            ('east', "East"),
            ('west', "West"),
        ],
    )
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string="State",
        selection=[
            ('new', "New"),
            ('offer_received', "Offer Received"),
            ('offer_accepted', "Offer Accepted"),
            ('sold', "Sold"),
            ('canceled', "Canceled"),
        ],
        required=True,
        default='new',
        copy=False,
    )

    property_type_id = fields.Many2one('estate.property.type', string="Property Types")
    user_id = fields.Many2one('res.users', string="Salesperson", default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string="Buyer", copy=False)
    tag_ids = fields.Many2many('estate.property.tag', string="Tags")
    offer_ids = fields.One2many('estate.property.offer', inverse_name="property_id")

    total_area = fields.Integer(string="Total Area (sqm)", compute='_compute_total_area')
    best_price = fields.Float(string="Best Offer", compute='_compute_best_price')

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_price(self):
        for record in self:
            record.best_price = max(record.offer_ids.mapped('price'), default=0)

    @api.onchange('garden')
    def _onchange_garden(self):
        self.garden_area, self.garden_orientation = (10, 'north') if self.garden else (0, None)
