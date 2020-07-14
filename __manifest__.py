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

    'category': 'Uncategorized',
    'version': '0.4',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/missions_security.xml',        
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
}