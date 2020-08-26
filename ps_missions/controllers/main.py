from odoo.http import Controller, route, request


class Oper(Controller):

    @route('/oper/credits', type='json', auth='user')
    def get_oper_credits_route(self, **params):
        """Return a JSON with the available credits for the Oper
        This credit is taken from all open vendor invoices"""

        if 'id' in params:
            oper_id = params.get('id')
            oper_credits = request.env['res.partner'].browse(oper_id).debit
            data = {'status': 200, 'response': {'oper_credits': oper_credits}, 'message': 'Success'}
            return data
