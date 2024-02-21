from odoo import fields, models, api, exceptions


class Estate(models.Model):
    _name = "estate.property"
    _description = "Properties of estate entities."

    active = fields.Boolean(default=True)

    garage = fields.Boolean()

    garden = fields.Boolean()

    name = fields.Char(string="Name", required=True)

    postcode = fields.Char()

    description = fields.Text()

    bedrooms = fields.Integer(default=2)

    living_area = fields.Integer()

    facades = fields.Integer()

    total_area = fields.Integer(
            string="Total Area",
            compute="_compute_total")

    expected_price = fields.Float(required=True, readonly=True, default=99999)

    selling_price = fields.Float(copy=False, readonly=True)

    best_price = fields.Float(compute="_get_max_offer", string="Best Price")

    property_type_id = fields.Many2one("estate.property.type", string="Type")

    date_availability = fields.Date(
            copy=False,
            default=fields.Date.add(fields.Date.today(), months=3))

    garden_orientation = fields.Selection(
            string="Orientation",
            selection=[
                ("north", "North"),
                ("south", "South"),
                ("east", "East"),
                ("west", "West")],
            help="Cardinal orientation of the garden.",)

    state = fields.Selection(
            string='State',
            required=True,
            copy=False,
            default='new',
            selection=[
                ("new", "New"),
                ("offer received", "Offer Received"),
                ("offer accepted", "Offer Accepted"),
                ("sold", "Sold"),
                ("canceled", "Canceled")])

    tag_ids = fields.Many2many("estate.property.tag", string="Tags")

    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)

    salesperson = fields.Many2one(
            "res.users",
            string="Salesperson",
            default=lambda self: self.env.user)

    offer_ids = fields.One2many(
            "estate.property.offer", "property_id", string="Offer")

    garden_area = fields.Integer()

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.garden_area + record.living_area

    @api.depends("offer_ids")
    def _get_max_offer(self):
        for property in self:
            offers = self.offer_ids.mapped("price")
            max = 0
            for offer in offers:
                if offer > max:
                    max = offer
        property.best_price = max

    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"

    def set_sold_status(self):
        if self.state == "canceled":
            raise exceptions.UserError(
                    "Canceled properties cannot be sold")
            return True
        self.state = "sold"
        return True

    def set_cancel_status(self):
        self.state = "canceled"
        return True
