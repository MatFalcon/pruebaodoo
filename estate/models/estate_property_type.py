from odoo import fields, models


class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate property type"
    _sql_constraints = [
        (
            "unique_property_type",
            "UNIQUE(name)",
            "The property type must be unique",
        )
    ]

    name = fields.Char("Title", required=True)
