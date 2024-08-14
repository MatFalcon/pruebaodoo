{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'description': """ Estate module """,
    'data': ['security/ir.model.access.csv',
             'views/estate_property_views.xml',
             'views/estate_menus.xml',
             'views/estate_property_type_views.xml',
             'views/estate_property_tag_views.xml',
             'views/estate_property_offer_views.xml'],
    'installable': True,
    'application': True,
    'sequence': -1,
    'license': 'LGPL-3'
}
