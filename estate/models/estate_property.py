from odoo import fields, models
import datetime

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate properties"
    name = fields.Char('Title', required = True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date availability', copy=False, default = datetime.date.today()+ datetime.timedelta(weeks=12))
    expected_price = fields.Float('Expected Price',required = True)
    selling_price = fields.Float('Selling Price', readonly =True, copy = False)
    bedrooms = fields.Integer('Bedrooms', default = 2)
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area')
    garden_orientation = fields.Selection(string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Direction Facing")
    
    active = fields.Boolean('Active', default = True)

    state = fields.Selection(string='State',
        selection=[('new', ' New'), ('offer received ', 'Offer Received'), ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'), ('cancelled', 'Cancelled')],
        help="Property State")