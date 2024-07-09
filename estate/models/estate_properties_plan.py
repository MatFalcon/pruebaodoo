from odoo import api, fields, models
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError


class propertiesPlan(models.Model):
    _name = "estate.property"
    _description = "Real Estate Properties Plan"

    name = fields.Char("Name", required=True)
    description = fields.Text("Description")
    postcode = fields.Char("Postcode")
    date_availability = fields.Date("Available Date", copy=False, default=fields.Datetime.today() + relativedelta(months=3))
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    buyer = fields.Char("Buyer", copy=False)
    total_area = fields.Integer("Total Area (sqm)", compute="_compute_total_area")
    best_price = fields.Float("Best Price", compute="_compute_best_price")
    sales_person = fields.Many2one(
        'res.users',
        default=lambda self: self.env.user or False,
        string="Sales Person"
    )
    garden_orientation = fields.Selection(
        string='Garden Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Select the direction to filter the options",
    )
    active = fields.Boolean("Active", default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('offer_received', 'Offer Received'), ('offer_accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Select the state of your property.",
        default='new'
    )
    property_type_id = fields.Many2one(
        comodel_name="estate.property.type",
        inverse_name="property_id",
        string="Property Type"
    )
    tag_ids = fields.Many2many(
        comodel_name="estate.property.tag",
        string="Property Tags"
    )
    offer_ids = fields.One2many(
        comodel_name="estate.property.offer",
        inverse_name="property_id",
        string=""
    )

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids')
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange('garden')
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_mark_sold(self):
        if self.state == 'canceled':
            raise UserError("Canceled Properties cannot be Sold")
        else:
            self.state = 'sold'
        return True

    def action_mark_canceled(self):
        if self.state == 'sold':
            raise UserError("Sold Properties cannot be Canceled")
        else:
            self.state = 'canceled'
        return True
