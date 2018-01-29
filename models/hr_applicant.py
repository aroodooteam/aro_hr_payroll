# -*- coding: utf-8 -*-

from openerp.osv import fields, osv
import datetime

class hr_applicant(osv.osv):
    _inherit = 'hr.applicant'
    def _get_salary(self, cr, uid, ids, name, arg, context={}):
        result = {}
        net=0
        param_obj=self.pool.get('hr.payroll_ma.parametres')
        param_ids=param_obj.search(cr,uid,[])
        param_ids=param_obj.browse(cr,uid,param_ids)
        for param in param_ids:
            if not param.salary_on_index:
                return False
            else:
                index_value=param.index
        for payroll in self.browse(cr, uid, ids, context):
            for index in payroll.job_id.categ_id.index_ids:
                result[payroll.id] = index.index*173.33*index_value/5
                break
        return result

    _columns = {
        'salary_index':fields.function(_get_salary,method=True, type='float',digits=(16, 2), string='Salaire Indicatif'),

    }
