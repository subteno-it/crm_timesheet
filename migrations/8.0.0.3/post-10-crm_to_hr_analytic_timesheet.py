# -*- coding: utf-8 -*-
##############################################################################
#
#    crm_timesheet module for OpenERP, CRM Timesheet
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sylvain Garancher <sylvain.garancher@syleam.fr>
#
#    This file is a part of crm_timesheet
#
#    crm_timesheet is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    crm_timesheet is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import logging
logger = logging.getLogger('crm_timesheet')

__name__ = 'Link hr.analytic.timesheet lines to the good crm models from old crm.analytic.timesheet data'


def migrate(cr, v):
    """
    :param cr: Current cursor to the database
    :param v: version number
    """
    for model_name, table_name, field_name in [
        ('crm.phonecall', 'crm_phonecall', 'phonecall_id'),
        ('crm.lead', 'crm_lead', 'lead_id'),
    ]:
        logger.info('Migrate %s analytic data' % model_name)
        cr.execute("SELECT hr_analytic_timesheet_id, res_id FROM crm_analytic_timesheet WHERE model = %%s AND res_id NOT IN (SELECT id FROM %s);" % table_name, (model_name,))
        for data in cr.fetchall():
            if data[0]:
                logger.warning('The hr.analytic.timesheet ID %d is linked to a nonexistent %s ID %d' % (data[0], model_name, data[1]))
        cr.execute("DELETE FROM crm_analytic_timesheet WHERE model = %%s AND res_id NOT IN (SELECT id FROM %s);" % table_name, (model_name,))
        cr.execute("""UPDATE hr_analytic_timesheet
                   SET %s = crm_analytic_timesheet.res_id
                   FROM (
                       SELECT hr_analytic_timesheet_id, res_id
                       FROM crm_analytic_timesheet
                       WHERE model = %%s
                   ) crm_analytic_timesheet
                   WHERE hr_analytic_timesheet.id = crm_analytic_timesheet.hr_analytic_timesheet_id;""" % field_name, (model_name,))
        logger.info('%d lines affected' % cr.rowcount)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
