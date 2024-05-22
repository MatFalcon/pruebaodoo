{
    "name": "Real Estate",
    "version": "1.0",
    "depends": ["base"],
    "author": "Louis Travaux",
    "category": "Category",
    "description": """
    Description text
    """,
    "installable": True,
    "application": True,
    "license": "LGPL-3",
    # data files always loaded at installation
    "data": [
        "security/ir.model.access.csv",
        "views/estate_property_views.xml",
        "views/estate_menus.xml",
    ],
    # # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/demo_data.xml',
    # ],
}
