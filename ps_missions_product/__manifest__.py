# Copyright 2020 - TODAY, POPSOLUTIONS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'POP Missions Product',
    'summary': """
        Módulo de missões do aplicativo Goop 2020 - Produtos""",
    'description': """
        Módulo de produtos de missões do aplicativo Goop criado pela POPSOLUTIONS""",
    'version': '12.0.1.0.0',
    'category': 'Marketing',
    'license': 'AGPL-3',
    'author': 'POPSOLUTIONS',
    'contributors': [
        'Marcel Savegnago <marcel.savegnago@gmail.com>',
    ],
    'website': 'http://www.popsolutions.co',
    'depends': [
        'ps_missions',
    ],
    'data': [
        'security/pops_product_packaging_type.xml',
        'views/pops_product_packaging_type.xml',
        'security/pops_product_category.xml',
        'views/pops_product_category.xml',
        'security/pops_product_brand.xml',
        'views/pops_product_brand.xml',
        'security/pops_product.xml',
        'views/pops_product.xml',
    ],
    'demo': [
    ],
}
