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

class crm_case_work(osv.osv):
    _name = 'crm.case.work'
    _description = 'CRM summary work'

    _columns = {
        'case_id': fields.many2one('crm.case', 'Case', ondelete='cascade', required=True),
        'name': fields.char('Work summary', size=128),
        'date': fields.datetime('Date'),
        'hours': fields.float('Time spent'),
        'user_id': fields.many2one('res.users', 'Done by', required=True),
    }

    _defaults = {
        'user_id': lambda obj,cr,uid,context: uid,
        'date': lambda *a: time.strftime('%Y-%m-%d %H:%M:%S'),
    }
    _order = "date desc"

crm_case_work()

class crm_case(osv.osv):
    _name = 'crm.case'
    _inherit = 'crm.case'

    _columns = {
        'timesheet_ids': fields.one2many('crm.case.work', 'case_id', 'Summary Work'),
    }

crm_case()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
