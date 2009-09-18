# -*- encoding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution	
#    Copyright (C) 2008-2009 Syleam (<http://syleam.fr>). All Rights Reserved
#    $Id$
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from osv import fields, osv
from tools.translate import _
import time
import tools

class crm_case_work(osv.osv):
    _name = 'crm.case.work'
    _description = 'CRM summary work'

    _columns = {
        'case_id': fields.many2one('crm.case', 'Case', ondelete='cascade', required=True),
        'name': fields.char('Work summary', size=128),
        'date': fields.datetime('Date'),
        'hours': fields.float('Time spent'),
        'user_id': fields.many2one('res.users', 'Done by', required=True),
        'hr_analytic_timesheet_id':fields.integer('Related Timeline Id'),
    }

    _defaults = {
        'user_id': lambda obj,cr,uid,context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    _order = "date desc"


    def _get_analytic_account_id(self, cr, uid, vals, context=None):
        """Return account ; try to find it based on case values
            This methode can be overload to remplace account number
        """
        print "DEBUG: get_analytic_account_id(%r, %r)" % (vals, context)
        obj_case = self.pool.get('crm.case').browse(cr, uid, vals['case_id'])
        if not obj_case.section_id.account_id:
            raise osv.except_osv(_('Bad Configuration !'), _('No default analytic account on this section.'))

        out_account_id = obj_case.section_id.account_id.id
        if obj_case.partner_id:
            pa_obj = self.pool.get('res.partner.crm.analytic')
            dm = [
                ('partner_id','=',obj_case.partner_id.id),
                ('section_id','=',obj_case.section_id.id),
            ]
            an_id = pa_obj.search(cr, uid, dm)
            if an_id:
                acc_id = pa_obj.read(cr, uid, an_id[0])
                if acc_id['account_id']:
                    out_account_id = acc_id['account_id'][0]
        return out_account_id


    def _get_analytic_account_name(self, cr, uid, vals, context=None):
        """Return label for line of analytic account (based on case values)
            Actualy prefix with crm.case name
        """
        print "DEBUG: get_analytic_account_name(%r, %r)" % (vals, context)        
        obj_case = self.pool.get('crm.case').browse(cr, uid, vals['case_id'])
        if vals['name']:
            ts_name = '%s: %s' % (obj_case.name[:64], vals['name'][:62])
        else:
            ts_name = case.name[:126] + ' /'
        return ts_name


    def create(self, cr, uid, vals, *args, **kwargs):
        obj = self.pool.get('hr.analytic.timesheet')
        vals_line = {}
#        obj_case = self.pool.get('crm.case').browse(cr, uid, vals['case_id'])
        emp_obj = self.pool.get('hr.employee')
        emp_id = emp_obj.search(cr, uid, [('user_id', '=', vals.get('user_id', uid))])

        if not emp_id:
            raise osv.except_osv(_('Bad Configuration !'),
                 _('No employee defined for this user. You must create one.'))
        emp = self.pool.get('hr.employee').browse(cr, uid, emp_id[0])
        if not emp.product_id:
            raise osv.except_osv(_('Bad Configuration !'),
                 _('No product defined on the related employee.\nFill in the timesheet tab of the employee form.'))

        if not emp.journal_id:
            raise osv.except_osv(_('Bad Configuration !'),
                 _('No journal defined on the related employee.\nFill in the timesheet tab of the employee form.'))

        vals_line['account_id'] = self._get_analytic_account_id(cr, uid, vals)

        a =  emp.product_id.product_tmpl_id.property_account_expense.id
        if not a:
            a = emp.product_id.categ_id.property_account_expense_categ.id
        vals_line['general_account_id'] = a
        vals_line['journal_id'] = emp.journal_id.id

        vals_line['name'] = self._get_analytic_account_name(cr, uid, vals)

        vals_line['user_id'] = vals['user_id']
        vals_line['date'] = vals['date'][:10]
        vals_line['unit_amount'] = vals['hours']
        vals_line['amount'] = 00.0
        timeline_id = obj.create(cr, uid, vals_line, {})

        vals_line['amount'] = (-1) * vals['hours'] * obj.browse(cr, uid, timeline_id).product_id.standard_price
        obj.write(cr, uid,[timeline_id], vals_line, {})
        vals['hr_analytic_timesheet_id'] = timeline_id
        return super(crm_case_work,self).create(cr, uid, vals, *args, **kwargs)


    def write(self, cr, uid, ids, vals, context=None):
        vals_line = {}

        for case in self.pool.get('crm.case.work').browse(cr, uid, ids):
            line_id = case.hr_analytic_timesheet_id
            if line_id:
                obj = self.pool.get('hr.analytic.timesheet')
                if 'name' in vals:
                    vals_line['name'] = self._get_analytic_account_name(cr, uid, vals)
                if 'user_id' in vals:
                    vals_line['user_id'] = vals['user_id']
                if 'date' in vals:
                    vals_line['date'] = vals['date'][:10]
                if 'hours' in vals:
                    vals_line['unit_amount'] = vals['hours']
                    vals_line['amount'] = (-1) * vals['hours'] * obj.browse(cr, uid, line_id).product_id.standard_price
                obj.write(cr, uid, [line_id], vals_line, {})

        return super(crm_case_work,self).write(cr, uid, ids, vals, context)


    def unlink(self, cr, uid, ids, *args, **kwargs):
        for ts in self.pool.get('crm.case.work').browse(cr, uid, ids):
            if ts.hr_analytic_timesheet_id:
                obj = self.pool.get('hr.analytic.timesheet').unlink(cr, uid, [ts.hr_analytic_timesheet_id], *args, **kwargs)
        return super(crm_case_work,self).unlink(cr, uid, ids, *args, **kwargs)

crm_case_work()

class crm_case(osv.osv):
    _name = 'crm.case'
    _inherit = 'crm.case'

    _columns = {
        'timesheet_ids': fields.one2many('crm.case.work', 'case_id', 'Summary Work'),
    }

crm_case()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: