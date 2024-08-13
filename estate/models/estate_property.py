from odoo import models , fields

class EstateProperty(models.Model):

    _name="estate.property"
    _description="Estate property"

    name = fields.Char('Name' ,required=True)
    description = fields.Text('Description')
    postcode = fields.Char('Postcode')
    date_availability = fields.Date('Date Availability')
    expected_price = fields.Float('Expected Price',required=True)
    selling_price = fields.Float('Selling Price')
    bedrooms = fields.Integer('Bedrooms')
    living_area = fields.Integer('Living Area')
    facades = fields.Integer('Facades')
    garage = fields.Boolean('Garage')
    garden = fields.Boolean('Garden')
    garden_area = fields.Integer('Garden Area ')
    garden_orientation = fields.Selection(
        [('North', 'North'), ('South', 'South'), ('East', 'East'), ('West', 'West')],
        'Garden Orientation')