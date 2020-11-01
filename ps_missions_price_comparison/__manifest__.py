# -*- coding: utf-8 -*-
{
    'name': "POP Missions Price Comparison",

    'summary': """
        Include a new type of mission called "Price Comparison" """,

    'description': """
        With this module you can create a Mission Type name Product Comparisson and
        link together with other similar products and visualize their prices and further analysis"
    """,

    'author': "POPSOLUTIONS",
    'contributors': [
        'Jaqueline Passos <jaqueline.passos@popsolutions.co>',
        'Victor Inojosa <vijoin@gmail.com>',
        'Marcos Mendez <marcos.foto@gmail.com>',
    ],
    'website': "http://www.popsolutions.co",

    'category': 'Marketing',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['ps_missions_product'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/measurements_views.xml',
        'views/missions_views.xml',
        'data/products.xml',
    ],
    'installable': True,
    'application': False,
}