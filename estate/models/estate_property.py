from odoo import fields, models, api, exceptions
from odoo.tools import relativedelta

class EstateProperty(models.Model):
    # Table meta-data
    _name = "estate.property"
    _description = "Estate Property"

    # Table relations
    # Many2one or One2Many
    property_type_id = fields.Many2one(string="Property Type", comodel_name="estate.property.type")
    salesperson_id = fields.Many2one(string="Salesperson", comodel_name="res.users", default=lambda self: self.env.user)
    buyer_id = fields.Many2one(string="Buyer", comodel_name="res.partner", copy=False)
    # Many2Many
    tag_ids = fields.Many2many(string="Tags", comodel_name="estate.property.tag")
    # One2Many
    offer_ids = fields.One2many(string="Offers", comodel_name="estate.property.offer", inverse_name="property_id")
    
    #Table attributes
    name = fields.Char(string="Name", required=True)
    description = fields.Text(string="Description")
    postcode = fields.Char(string="Postcode")
    date_availability = fields.Date(default=lambda self: fields.Date.today() + relativedelta(months=3), copy=False, string="Available From")
    expected_price = fields.Float(required=True, string="Expected Price")
    selling_price = fields.Float(readonly=True, copy=False, string="Selling Price")
    active = fields.Boolean(default=True, string="Active")

    bedrooms = fields.Integer(default=2, string="Bedrooms")
    living_area = fields.Integer(string="Living Area (sqm)")
    facades = fields.Integer(string="Facades")
    garage = fields.Boolean(string="Garage")
    garden = fields.Boolean(string="Garden")
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection([
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')
    ], string="Garden Orientation")
    state = fields.Selection([
        ('new', 'New'),
        ('offer_received', 'Offer Received'),
        ('offer_accepted', 'Offer Accepted'),
        ('sold', 'Sold'),
        ('canceled', 'Canceled')
    ], default='new', required=True, copy=False, string="State")
    
    # Computed columns
    total_area = fields.Integer(string="Total Area (sqm)", compute="_compute_total_area")
    best_offer = fields.Float(string="Best Offer", compute="_compute_best_offer")

    @api.depends('living_area', 'garden_area')
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends('offer_ids.price')
    def _compute_best_offer(self):
        for record in self:
            record.best_offer = max(record.mapped('offer_ids.price'), default=0.0)

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_set_sold_state(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError(message="Already a canceled property")
            if record.state == 'sold':
                raise exceptions.UserError(message="Already a sold property")
            
            record.state = 'sold'
        return True

    def action_set_cancel_state(self):
        for record in self:
            if record.state == 'canceled':
                raise exceptions.UserError(message="Already a canceled property")
            if record.state == 'sold':
                raise exceptions.UserError(message="A sold property can't be canceled")
            
            record.state = 'canceled'
        return True
