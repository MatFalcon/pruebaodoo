{
    'name': "Real Estate",
    'version': '1.0',
    'depends': ['base', 'website'],
    'author': "Vansh",
    'category': 'Real Estate/Brokerage',
    'description': """Find Your property Here""",
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/property_template.xml',
        'report/estate_property_sub_templates.xml',
        'report/estate_property_templates.xml',
        'report/estate_property_reports.xml',
        'views/estate_property_user_views.xml',
        'views/estate_property_offer_views.xml',
        'views/estate_property_type_views.xml',
        'views/estate_property_tags_views.xml',
        'views/estate_property_views.xml',
        'views/estate_property_setting_views.xml',
        'views/estate_menus.xml',
        'data/estate_data.xml',
        "data/estate.property.type.csv",
    ],
    "demo": [
        "demo/demo_estate_property.xml",
    ],
    'images': ['static/description/estate.png'],
    'application': True,
    'installable': True,
    'license': "AGPL-3"
}
