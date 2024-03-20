from odoo import fields, models, api, exceptions

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate Property Offer"

    price = fields.Float(string="Price")
    status = fields.Selection([
        ("accepted", "Accepted"),
        ("refused", "Refused"),
    ], copy=False, string="Status")

    partner_id = fields.Many2one(string="Buyer", comodel_name="res.partner", required=True)
    property_id = fields.Many2one(string="Property", comodel_name="estate.property", required=True)
    validity = fields.Integer(string="Offer Validity (days)", default=7)
    date_deadline = fields.Date(string="Deadline", compute="_compute_deadline_date", inverse="_inverse_deadline_date")

    @api.depends("validity", "create_date")
    def _compute_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.date_deadline = fields.Date.add(initial_date, days=record.validity)

    def _inverse_deadline_date(self):
        for record in self:
            initial_date = fields.Date.to_date(record.create_date) if record.create_date else fields.Date.today()
            record.validity = (record.date_deadline - initial_date).days

    def action_set_accepted_state(self):
        for record in self:
            if self._is_valid_deal(record.property_id.state):
                raise exceptions.UserError(message="Can't accept/reject offer on a closed deal!!")
            
            if record.property_id.buyer_id:
                raise exceptions.UserError(message="This property has a buyer already!!")

            record.property_id.buyer_id = record.partner_id
            record.property_id.state = 'offer_accepted'
            record.status = 'accepted'
            record.property_id.selling_price = record.price
        return True

    def action_set_rejected_state(self):
        for record in self:
            if self._is_valid_deal(record.property_id.state):
                raise exceptions.UserError(message="Can't accept/reject offer on a closed deal!!")
            
            if record.property_id.buyer_id == record.partner_id and record.property_id.selling_price == record.price:
                record.property_id.buyer_id = None
                record.property_id.state = 'new'
                record.property_id.selling_price = 0
            
            record.status = 'refused'
        return True
    
    def _is_valid_deal(self, status):
        return status in ['sold', 'canceled']
