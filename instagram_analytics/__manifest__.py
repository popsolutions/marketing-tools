# -*- coding: utf-8 -*-
{
    'name': "Instagram Analytics",
    'summary': """Instagram Analytics""",
    'description': """
        Monitor Instagram Accounts and get data from the posts 
        in order to measure the engagement with the Brand
    """,
    'author': "POP Solutions",
    'website': "http://www.popsolutions.co",
    'category': 'Marketing',
    'version': '0.1',
    'depends': ['social_network_analytics_base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/sna_instagram_post_views.xml',
        'views/sna_instagram_config_views.xml',
        'data/ir_cron_sna_instagram_config.xml'
    ],
}