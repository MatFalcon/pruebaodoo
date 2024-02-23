from odoo import api, fields, models
from odoo.exceptions import UserError, ValidationError
from odoo.tools import float_compare, float_is_zero


class Property(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    _sql_constraints = (
        ('positive_expected_price', 'CHECK(expected_price > 0)',
         'Expected price should be positive'),

        ('positive_selling_price', 'CHECK(selling_price >= 0)',
         'Selling price should be positive'),
    )

    name = fields.Char(
        string='Name',
        required=True,
        help='This is the name of the estate property.',
        index=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date(
        default=fields.Date.add(fields.Date.today(), months=3),
        copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer(string="Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[
        ('north', 'North'),
        ('south', 'South'),
        ('east', 'East'),
        ('west', 'West')])
    active = fields.Boolean(default=True)
    state = fields.Selection(
        required=True,
        copy=False,
        default='new',
        selection=[
            ('new', 'New'),
            ('received', 'Offer Received'),
            ('accepted', 'Offer Accepted'),
            ('sold', 'Sold'),
            ('canceled', 'Canceled'),
        ])
    total_area = fields.Integer(
        compute="_compute_total_area",
        string="Total Area (sqm)")
    best_price = fields.Float(compute="_compute_best_price")
    property_type_id = fields.Many2one("estate.property.type", string="Type")
    salesman_id = fields.Many2one(
        "res.users",
        string="Salesman",
        default=lambda self: self.env.user)
    buyer_id = fields.Many2one("res.partner", copy=False, readonly=True)
    property_tag_ids = fields.Many2many("estate.property.tag")
    offer_ids = fields.One2many("estate.property.offer", "property_id")

    @api.onchange("garden")
    def _onchange_garden(self):
        if (self.garden):
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if len(record.offer_ids) > 0:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0

    def sell(self):
        for record in self:
            if record.state == 'canceled':
                raise UserError('Canceled property cannot be sold')
            else:
                record.state = 'sold'
        return True

    def cancel(self):
        for record in self:
            if record.state == 'sold':
                raise UserError('Sold property cannot be canceled')
            else:
                record.state = 'canceled'
        return True

    @api.constrains('selling_price', 'expected_price')
    def _check_selling_price(self):
        for record in self:
            if float_compare(record.selling_price, record.expected_price * 0.9, precision_digits=3) < 0 and not float_is_zero(record.selling_price, precision_digits=3):
                raise ValidationError(
                    "Selling price cannot be < 90% of the expected price")

    @api.ondelete(at_uninstall=False)
    def _unlink_if_valid_state(self):
        if any(not (record.state in ['new', 'canceled']) for record in self):
            raise UserError(
                "Cannot delete a Property which is not New or Canceled")
