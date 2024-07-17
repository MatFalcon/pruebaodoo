{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base'],
    'author': "GAJA",
    'category': 'Category',
    'description': """
    Hell Hoo
    """,
    # data files always loaded at installation
    'data': [
        'data/estate.property.type.csv',
        'security/ir.model.access.csv',
        'views/estate_property_tag_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_type_views.xml',
        'views/res_users_views.xml',
        'views/estate_menus.xml',
        'views/res_config_settings_views.xml',
    ],
    # data files containing optionally loaded demonstration data
    'demo': [
        'demo/estate_demo_data_views.xml'
    ],
    "images": ["static/description/new.png"],
    'application': True,
    'license': 'AGPL-3',
}
