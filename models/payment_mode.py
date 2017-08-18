# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class payment_mode(osv.osv):

    _name = "payment.mode"
    _description = "Mode de payement"

    _columns = {
        'code': fields.char('Code', size=8),
        'name': fields.char('Type', size=64),
        'ref': fields.char('Reference', size=64),
        }
payment_mode()
