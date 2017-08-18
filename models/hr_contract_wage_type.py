# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class hr_contract_wage_type(osv.osv):
    _name = 'hr.contract.wage.type'
    _description = 'Wage Type'
    _columns = {
        'name': fields.char('Wage Type Name', size=50,
                            required=True, select=True),
        'period_id': fields.many2one('hr.contract.wage.type.period',
                                     'Wage Period', required=True),
        'type': fields.selection(
            [('gross', 'Gross'), ('net', 'Net')], 'Type', required=True),
        'factor_type': fields.float('Factor for hour cost',
                                    digits=(12, 4), required=True,)}
    _defaults = {
        'type': 'gross',
        'factor_type': 1.8
    }
hr_contract_wage_type()
