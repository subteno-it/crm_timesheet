# -*- coding: utf-8 -*-
##############################################################################
#
#    crm_timesheet module for openerp, CRM timesheet
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
#    copyright (c) 2011 syleam info services (<http://www.syleam.fr/>)
#              sebastien lange <sebastien.lange@syleam.fr>
#
#    this file is a part of crm_timesheet
#
#    crm_timesheet is free software: you can redistribute it and/or modify
#    it under the terms of the gnu general public license as published by
#    the free software foundation, either version 3 of the license, or
#    (at your option) any later version.
#
#    crm_timesheet is distributed in the hope that it will be useful,
#    but without any warranty; without even the implied warranty of
#    merchantability or fitness for a particular purpose.  see the
#    gnu affero general public license for more details.
#
#    you should have received a copy of the gnu affero general public license
#    along with this program.  if not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, fields


class crm_analytic_timesheet_configuration(models.Model):
    _name = 'crm.analytic.timesheet.configuration'
    _description = 'CRM Timesheet Default Values'

    name = fields.Char(size=64, required=True, help='Name of this parameter, use in partner')
    model = fields.Char(size=128, required=True, help='Model of OpenERP, eg: crm.lead')
    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='cascade', required=True, help='Analytic account by default for the model indicated')

    _sql_constraints = [
        ('model_uniq', 'unique (model)', 'The model of the OpenERP must be unique !'),
    ]

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
