# -*- coding: utf-8 -*-
##############################################################################
#
#    crm_timesheet module for OpenERP, CRM Timesheet
#    Copyright (C) 2011 SYLEAM Info Services (<http://www.Syleam.fr/>)
#              Sebastien LANGE <sebastien.lange@syleam.fr>
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

from openerp import models, api, fields


class crm_phonecall(models.Model):
    _inherit = 'crm.phonecall'

    analytic_account_id = fields.Many2one('account.analytic.account', string='Analytic Account', ondelete='cascade', default='get_default_analytic')
    timesheet_ids = fields.One2many('hr.analytic.timesheet', 'phonecall_id', string='Messages')

    @api.one
    def get_default_analytic(self):
        """
        Gives id of analytic for this case
        """
        return self.env['crm.analytic.timesheet.configuration'].search([('model', '=', self._name)]).analytic_account_id.id

    @api.multi
    def on_change_partner_id(self, partner_id):
        """This function returns value of partner address based on partner
        @param self: The object pointer
        @param cr: the current row, from the database cursor,
        @param uid: the current user’s ID for security checks,
        @param ids: List of case IDs
        @param part: Partner's id
        @email: Partner's email ID
        """
        if not partner_id:
            return {'value': {
                'email_from': False,
                'phone': False,
                'analytic_account_id': False,
            }}
        partner = self.env['res.partner'].browse(partner_id)
        values = {
            'partner_phone': partner.phone,
            'partner_mobile': partner.mobile,
        }
        if not partner.is_company and partner.parent_id:
            partner = partner.parent_id
        for timesheet in partner.crm_analytic_ids:
            if timesheet.crm_model_id.model == self._name:
                values['analytic_account_id'] = timesheet.analytic_account_id.id

        return {'value': values}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
