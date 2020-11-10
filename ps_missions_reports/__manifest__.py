# Copyright 2020 - TODAY, POPSOLUTIONS
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    'name': 'POP Missions Reports',
    'description': """
        Módulo de missões do aplicativo Goop 2020 - Relatórios""",
    'description': """
        Módulo de relatórios de missões do aplicativo Goop criado pela POPSOLUTIONS""",
    'version': '12.0.1.0.0',
    'license': 'AGPL-3',
    'author': 'POPSOLUTIONS',
    'website': 'https://popsolutions.co',
    'depends': [
        'ps_missions_price_comparison',
        'web_view_google_map',
    ],
    'data': [
        'security/pops_measurement_price_comparison_report.xml',
        'report/pops_measurement_price_comparison_report.xml',
    ],
}
