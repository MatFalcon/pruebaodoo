# -*- coding: utf-8 -*-

from odoo import models, fields


class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate module"

    name = fields.Char(required=True)
    description = fields.Text()
    postcode = fields.Char()
    date_availability = fields.Date("Available from", default=fields.Date().add(fields.Date().today(), months=3),
                                    copy=False)
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(string='Garden Orientation',
                                          selection=[('north', 'North'), ('south', 'South'), ('east', 'East'),
                                                     ('west', 'West')])
    active = fields.Boolean('Active', default=False)
    state = fields.Selection(string='State', default='new', copy=False, required=True,
                             selection=[('new', 'New'), ('offer received', 'Offer Received'),
                                        ('offer accepted', 'Offer Accepted'), ('sold', 'Sold'),
                                        ('canceled', 'Canceled')])
