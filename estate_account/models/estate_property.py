from odoo import Command, models


class EstateProperty(models.Model):
    _inherit = "estate.property"

    def sold_property(self):
        for estate in self:
            self.env['account.move'].create(
                {
                    'partner_id': estate.buyer_id.id,
                    'move_type': 'out_invoice',
                    'invoice_line_ids': [
                        Command.create({
                            "name": estate.name,
                            "quantity": 0.06,
                            "price_unit": estate.selling_price,
                        }),
                        Command.create({
                            "name": "Administrative fees",
                            "quantity": 1,
                            "price_unit": 100,
                        })
                    ]
                }
            )
        return super().sold_property()
