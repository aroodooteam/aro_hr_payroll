# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class hr_contract_type(osv.osv):
    _name = 'hr.contract.type'
    _description = 'Contract Type'
    _columns = {
        'name': fields.char('Contract Type', size=32, required=True),
    }
hr_contract_type()
