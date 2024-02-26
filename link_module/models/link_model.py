from odoo import models, Command

class LinkModel(models.Model):
    _inherit = "estate.property"

    def sold_action(self):
        for record in self:
            self.env["account.move"].create(
            {
                'partner_id': record.buyer_id.id,
                'move_type': 'out_invoice',
                'invoice_line_ids': [
                    Command.create({
                        "name": record.name,
                        "quantity": 1,
                        "price_unit": record.selling_price * 0.06
                    }),
                    Command.create({
                        "name": "Administrative fees",
                        "quantity": 1,
                        "price_unit": 100
                    })
                ]
            }
        )
        return super().sold_action()
    