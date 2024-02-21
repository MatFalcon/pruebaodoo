from odoo import models, fields


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "real estate property tag"

    name = fields.Char(required=True)

    _sql_constraints = [
        ("unique_name", "unique( name )", "Property tag must be unique.")
    ]
