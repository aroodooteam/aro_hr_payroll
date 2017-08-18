# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class hr_contract(osv.osv):
    _inherit = 'hr.contract'
    _description = 'Employee Contract'

    _columns = {
        'name': fields.char('Contract Reference', size=32, required=True),
        'employee_id': fields.many2one('hr.employee', 'Employee',
                                       required=True),
        'department_id': fields.related('employee_id', 'department_id',
                                        type='many2one',
                                        relation='hr.department',
                                        string='Department',
                                        readonly=True),
        'type_id': fields.many2one('hr.contract.type', 'Contract Type',
                                   required=True),
        'job_id': fields.many2one('hr.job', 'Job Title'),
        'date_start': fields.date('Start Date', required=True),
        'date_end': fields.date('End Date'),
        'trial_date_start': fields.date('Trial Start Date'),
        'trial_date_end': fields.date('Trial End Date'),
        'working_hours': fields.many2one('resource.calendar',
                                         'Working Schedule'),
        'wage_type_id': fields.many2one('hr.contract.wage.type',
                                        'Wage Type', required=False),
        'wage': fields.float('Wage', digits=(16, 2), required=True),
        'advantages': fields.text('Advantages'),
        'advantages_net': fields.float('Net Advantages Value', digits=(16, 2)),
        'advantages_gross': fields.float('Gross Advantages Value',
                                         digits=(16, 2)),
        'notes': fields.text('Notes'),
        'salary_clause': fields.char('Clause specifique pour le salaire',
                                     size=64),
        'working_days_per_month': fields.integer('jours travailles par mois'),
        'hour_salary': fields.float('salaire Heure'),
        'monthly_hour_number': fields.float('Nombre Heures par mois'),
        # 'cotisation': fields.many2one('hr.payroll_ma.cotisation.type',
        # 'Type cotisations', required=True),
        # 'rubrique_ids': fields.one2many('hr.payroll_ma.ligne_rubrique',
        # 'id_contract', 'Les rubriques'),
        'assiduite': fields.boolean('Assuidite')
    }
    _defaults = {
        'working_days_per_month': lambda * a: 26,

    }

    # function used for hr_payroll
    """
    def net_to_brute(self, cr, uid, ids, context={}):
        id_contract = ids[0]
        contract = self.pool.get('hr.contract').browse(cr, uid, id_contract)
        salaire_base = contract.wage
        cotisation = contract.cotisation
        personnes = contract.employee_id.chargefam
        params = self.pool.get('hr.payroll_ma.parametres')
        objet_ir = self.pool.get('hr.payroll_ma.ir')
        id_ir = objet_ir.search(cr, uid, [])
        liste = objet_ir.read(cr, uid, id_ir,
                              ['debuttranche', 'fintranche', 'taux', 'somme'])
        ids_params = params.search(cr, uid, [])
        dictionnaire = params.read(cr, uid, ids_params[0])
        abattement = personnes * dictionnaire['charge']
        base = 0
        salaire_brute = salaire_base
        trouve = False
        trouve2 = False
        while(trouve is False):
            salaire_net_imposable = 0
            cotisations_employee = 0
            for cot in cotisation.cotisation_ids:
                if cot.plafonee and salaire_brute >= cot.plafond:
                    base = cot.plafond
                else:
                    base = salaire_brute
                cotisations_employee += base * cot['tauxsalarial'] / 100
            fraispro = salaire_brute * dictionnaire['fraispro'] / 100
            if fraispro < dictionnaire['plafond']:
                salaire_net_imposable = salaire_brute - fraispro
                salaire_net_imposable -= cotisations_employee
            else:
                salaire_net_imposable = salaire_brute - dictionnaire['plafond']
                salaire_net_imposable -= cotisations_employee
            for tranche in liste:
                if (salaire_net_imposable >= tranche['debuttranche']/12) \
                   and (salaire_net_imposable < tranche['fintranche']/12):
                    taux = (tranche['taux'])
                    somme = (tranche['somme']/12)
            ir = (salaire_net_imposable - (somme*12))*taux/100 - abattement
            if (ir < 0):
                ir = 0
            salaire_net = salaire_brute - cotisations_employee - ir
            if (int(salaire_net) == int(salaire_base) and not trouve2):
                trouve2 = True
                salaire_brute -= 1
            if (round(salaire_net, 2) == salaire_base):
                trouve = True
            elif not trouve2:
                salaire_brute += 0.5
            elif trouve2:
                salaire_brute += 0.01

        self.write(cr, uid, [contract.id], {'wage': round(salaire_brute, 2)})
        return True
    """
hr_contract()
