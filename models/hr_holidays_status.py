# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class hr_holidays_status(osv.osv):
    _inherit = "hr.holidays.status"
    _description = 'Holidays'
    _columns = {
        'payed': fields.boolean('paye', required=False),
    }
    _defaults = {
        'payed': lambda * args: True
    }
hr_holidays_status()
