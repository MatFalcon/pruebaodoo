from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate Property Tag"

    name = fields.Char(string="Name", required=True)

    # db Constraint
    _sql_constraints = [('unique_tag_name', 'unique(name)', 'The tag name must be unique!')]
