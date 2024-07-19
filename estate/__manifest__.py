{
    'name': "real-estate",
    'version': "1.0",
    'depends': ["base"],
    'author': "Dhruv",
    'category': "Real Estate/Brokerage",
    'application': True,
    'installable': True,
    'description': """
    Module for the practice and getting knowledge in the technicality
    """,
    'images': ['static/description/thumbnail.png'],
    'data': [
        'data/templates/estate.property.type.csv',
        'security/security.xml',
        'security/ir.model.access.csv',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tag_views.xml',
        'views/res_users_views.xml',
        'views/res_config_settings_views.xml',
        'views/estate_menus.xml',
    ],
    'demo': [
        'demo/demo_data.xml',
    ],
    'license': 'AGPL-3',
}
