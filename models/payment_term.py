# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class payment_term(osv.osv):

    _name = "payment.term"
    _description = "Mode de Reglement"

    def _get_default_rate(self, cr, uid, arg, context=None):
        terms = self.search(cr, uid,
                            [('employee_id', '=', context['employee_id'])],
                            context=None)
        terms = self.browse(cr, uid, terms, context=None)
        rate = 100
        for term in terms:
            rate = rate - term.rate
        return rate

    _columns = {
        # 'name':fields.selection(
        # [('virement', 'Virement'), ('cheque', 'Cheque'),
        # ('espece', 'Espece'), ], 'Mode De Reglement'),
        'name': fields.many2one('payment.mode', 'Mode De Reglement'),
        'employee_id': fields.many2one('hr.employee', 'Employe'),
        'bank_account_id': fields.many2one('res.partner.bank', 'RIB'),
        'bank_id': fields.related('bank_account_id', 'bank',
                                  relation='res.bank', type='many2one',
                                  string='Banque', readonly=True),
        # 'bank_account_number':fields.char('Numero de compte', size=64),
        'amount': fields.float('Montant'),  # il faut mettre une contrainte
        # pour empecher l'utilisteur de mettre total de taux > 100%
        'rate': fields.float('Taux'),  # rate a ete changer en montant donc
        # faut modifier la contrainte de taux = 100%
        'state': fields.selection(
            (('open', 'Actif'), ('cancel', 'Inactif')),
            'Etat'),
        }
    _defaults = {
        'state': 'open',
        # 'rate': lambda self, cr, uid,
        # context: self._get_default_rate(cr,uid,fields,context=context),
        }
payment_term()
