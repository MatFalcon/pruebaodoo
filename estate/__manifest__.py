{
    'name': 'estate',
    'category': 'Real Estate/Brokerage',
    'depends': [
        'base'
    ],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/estate_views.xml',
        'views/estate_menus.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/res_users_views.xml'
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
