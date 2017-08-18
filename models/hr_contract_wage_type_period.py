# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)

# Contract wage type period name


class hr_contract_wage_type_period(osv.osv):
    _name = 'hr.contract.wage.type.period'
    _description = 'Wage Period'
    _columns = {
        'name': fields.char('Period Name', size=50,
                            required=True, select=True),
        'factor_days': fields.float('Hours in the period',
                                    digits=(12, 4), required=True,)
    }
    _defaults = {
        'factor_days': 173.33
    }


hr_contract_wage_type_period()

