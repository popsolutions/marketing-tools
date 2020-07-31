# -*- coding: utf-8 -*-
{
    'name': "POP Missions",

    'summary': """
        Módulo de missões do aplicativo Goop 2020""",

    'description': """
        Módulo de missões do aplicativo Goop criado pela POPSOLUTIONS
    """,

    'author': "POPSOLUTIONS",
    'contributors': [
        'Jaqueline Passos <jaqueline.passos@popsolutions.co>',
        'Jonathas',
    ],
    'website': "http://www.popsolutions.co",

    'category': 'Marketing',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base', 'purchase'],

    # always loaded
    'data': [
        'security/missions_security.xml',        
        'security/ir.model.access.csv',
        'views/missions_views.xml',
        'views/measurements_views.xml',
        'data/products.xml',
        'data/ir_sequence_data.xml',
    ],
    'installable': True,
    'application': True,
}