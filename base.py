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


class res_company(models.Model):
    _inherit = 'res.company'

    crm_time_mode_id = fields.Many2one(
        'product.uom', string='CRM Time Unit',
        help="""This will set the unit of measure used in CRM.
            If you use the timesheet linked to CRM (crm_timesheet module), don't forget to setup the right unit of measure in your employees.""",
    )


class res_partner_crm_analytic(models.Model):
    """
    Define one analytic account by section,
    to disable the analytic account for a section, add line with section and
    not fill the analytic account
    """
    _name = 'res.partner.crm.analytic'
    _description = 'CRM Partner Analytic Account'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True)
    crm_model_id = fields.Many2one('crm.analytic.timesheet.configuration', string='Model', required=True, help='Model of crm')
    analytic_account_id = fields.Many2one(
        'account.analytic.account', string='Analytic Account', ondelete='cascade',
        domain="[('partner_id', '=', partner_id), ('state', '=', 'open')]",
        help='Ananlytic account by default for this model of crm and for this partner',
    )


class res_partner(models.Model):
    _inherit = 'res.partner'

    crm_analytic_ids = fields.One2many('res.partner.crm.analytic', 'partner_id', string='CRM Analytic Account')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
