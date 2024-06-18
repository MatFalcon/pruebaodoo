from odoo import _, fields, models


class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Property Tags"
    _order = "name"
    _sql_constraints = [
        ("check_unique_name", "unique (name)", _("All property tag must be unique")),
    ]

    name = fields.Char("Tag", required=True)
    color = fields.Integer()
