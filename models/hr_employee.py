# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import time
import logging
logger = logging.getLogger(__name__)


class hr_employee(osv.osv):
    _inherit = 'hr.employee'

    def _get_latest_contract(self, cr, uid, ids, field_name,
                             args, context=None):
        res = {}
        obj_contract = self.pool.get('hr.contract')
        for emp in self.browse(cr, uid, ids, context=context):
            contract_ids = obj_contract.search(
                cr, uid, [('employee_id', '=', emp.id)],
                order='date_start', context=context)
            if contract_ids:
                res[emp.id] = contract_ids[-1:][0]
            else:
                res[emp.id] = False
        return res

    def _get_visibility(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        for emp in self.browse(cr, uid, ids, context=context):
            visible = False
            if emp.user_id.id == uid:
                visible = True
            elif emp.parent_id.user_id.id == uid:
                visible = True
            else:
                group_ids = self.pool.get('res.users').browse(
                    cr, uid, uid, context=context).groups_id
                group_user_id = self.pool.get("ir.model.data").get_object_reference(cr, uid, 'base', 'group_hr_user')[1]
                if group_user_id in [group.id for group in group_ids]:
                    visible = True
                else:
                    group_user_id = self.pool.get("ir.model.data").get_object_reference(cr, uid, 'base', 'group_hr_manager')[1]
                    if group_user_id in [group.id for group in group_ids]:
                        visible = True
            res[emp.id] = visible
        return res

    def _get_children(self, cr, uid, ids, field_name, arg, context):
        employees = self.browse(cr, uid, ids)
        res = {}
        for employee in employees:
            count = 0
            for child in employee.children_ids:
                count += 1
            res[employee.id] = count
        return res

    def _get_chargefam(self, cr, uid, ids, field_name, arg, context):
        employees = self.browse(cr, uid, ids)
        res = {}
        for employee in employees:
            count = 0
            for child in employee.children_ids:
                ages = child.age.split()
                if len(ages) > 1:
                    if int(ages[0][:-1]) < 21:
                        count += 1
            res[employee.id] = count
        return res

    def _get_date_start(self, cr, uid, ids, field_name, arg, context):
        employees = self.browse(cr, uid, ids)
        res = {}
        for employee in employees:
            if not employee.contract_ids:
                res[employee.id] = '1900-01-01'
                continue
            for contract in employee.contract_ids:
                res[employee.id] = contract.date_start
                break
        return res

    def name_get(self, cr, uid, ids, context=None):
        # if not len(ids):
        #    return []
        res = []
        for employee in self.browse(cr, uid, ids, context=context):
            p_name = employee.name
            if employee.matricule:
                p_name = '[' + employee.matricule + '] ' + p_name
            res.append((employee.id, p_name))
        return res

    def _get_is_birthday(self, cr, uid, ids, field_name, args, context=None):
        res = {}
        this_week = time.strftime('%W')
        for emp in self.browse(cr, uid, ids):
            if not emp.birthday:
                res[emp.id] = False
            elif time.strftime('%W', time.strptime(emp.birthday, '%Y-%m-%d')) == this_week:
                res[emp.id] = True
            else:
                res[emp.id] = False
        return res

    def _search_is_birthday(self, cr, uid, obj, name, args,
                            domain=None, context=None):
        res = []
        ids = self.search(cr, uid, [('active', '=', True)])
        for emp in self.browse(cr, uid, ids):
            for flds, operator, value in args:
                if not value and not emp.is_birthday:
                    res.append(emp.id)
                if value and emp.is_birthday:
                    res.append(emp.id)
        return [('id', 'in', res)]

    _columns = {
        'visible': fields.function(_get_visibility, method=True,
                                   string='Visible', type='boolean'),
        'matricule': fields.char('Matricule', size=64),
        'cin': fields.char('CIN', size=64),
        'date': fields.function(_get_date_start, method=True,
                                string='Date Embauche', type='date'),
        # 'date': fields.date(
        # 'Date entree',
        # help='''Cette date est requipe pour le
        # calcule de la prime d' anciennete'''),
        'anciennete': fields.boolean(
            'Prime anciennete',
            help='Est ce que cet employe benificie de la prime d\'anciennete'),
        'mode_reglement': fields.selection(
            [('virement', 'Virement'), ('cheque', 'Cheque'),
             ('espece', 'Espece')], 'Mode De Reglement'),
        'payment_term_id': fields.one2many('payment.term', 'employee_id',
                                           'Mode de Paiement'),
        'bank': fields.char('Banque', size=128),
        'compte': fields.char('Compte bancaire', size=128),
        # 'chargefam' : fields.integer('Nombre de personnes a charge'),
        'chargefam': fields.function(_get_chargefam, method=True,
                                     type='float'),
        'logement': fields.float('Abattement Fr Logement'),
        'affilie': fields.boolean(
            'Affilie',
            help='Est ce qu on va calculer les cotisations pour cet employe'),
        'address_home': fields.char('Adresse Personnelle', size=128),
        'address': fields.char('Adresse Professionnelle', size=128),
        'phone_home': fields.char('Telephone Personnel', size=128),
        'licexpiry': fields.char('Lic Expiry', size=128),
        'licenseno': fields.char('Lic No', size=128),
        'licensetyp': fields.char('Lic Type', size=128),
        'manager': fields.boolean('Is a Manager'),
        'medic_exam': fields.date('Medical Examination Date'),
        'place_of_birth': fields.char('Place of Birth', size=30),
        'cin_date': fields.date('Date CIN'),
        'cin_place': fields.char('Lieu CIN', size=30),
        # 'children': fields.integer('Number of Children'),
        'children': fields.function(_get_children, method=True, type='float'),
        'vehicle': fields.char('Company Vehicle', size=64),
        'vehicle_distance': fields.integer('Home-Work Distance',
                                           help="In kilometers"),
        'contract_ids': fields.one2many('hr.contract', 'employee_id',
                                        'Contracts'),
        'contract_id': fields.function(_get_latest_contract, method=True,
                                       string='Contract', type='many2one',
                                       relation="hr.contract",
                                       help='Latest contract of the employee'),
        'contract_type_id': fields.related('contract_id', 'type_id',
                                           string='Contrat', type='many2one',
                                           relation='hr.contract.type',
                                           readonly=1),
        'aptitude_job': fields.float(u'Aptitude/Poste'),
        'qualification_job': fields.float('Qualification/Poste'),
        'training_job': fields.float('Formation/Poste'),
        'is_birthday': fields.function(_get_is_birthday, method=True,
                                       type='boolean',
                                       fnct_search=_search_is_birthday),
    }
    _defaults = {
        # 'chargefam' : lambda * a: 0,
        'logement': lambda * a: 0,
        'anciennete': lambda * a: 'True',
        'affilie': lambda * a: 'True',
        'date': lambda * a: time.strftime('%Y-%m-%d'),
        'mode_reglement': lambda * a: 'virement'
    }

    def name_search(self, cr, user, name, args=None, operator='ilike',
                    context=None, limit=80):
        """Search by bank code in addition to the standard search"""
        results = super(hr_employee, self).name_search(
            cr, user, name, args=args, operator=operator,
            context=context, limit=limit)
        ids = self.search(cr, user, [('matricule', operator, name)],
                          limit=limit, context=context)
        # Merge the results
        results = list(set(results + self.name_get(cr, user, ids, context)))
        return results

    def name_search2(self, cr, user, name='', args=None, operator='ilike',
                     context=None, limit=100):
        if not args:
            args = []
        if not context:
            context = {}
        ids = []
        if name:
            ids = self.search(cr, user, [('matricule', '=', name)] + args,
                              limit=limit, context=context)
        if not ids:
            ids = self.search(cr, user, [('name', operator, name)] + args,
                              limit=limit, context=context)
        return self.name_get(cr, user, ids, context=context)


hr_employee()
