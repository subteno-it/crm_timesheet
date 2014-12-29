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


class crm_lead(models.Model):
    _inherit = 'crm.lead'

    analytic_account_id = fields.Many2one('account.analytic.account', 'Analytic Account', ondelete='cascade', default='get_default_analytic')
    timesheet_ids = fields.One2many('hr.analytic.timesheet', 'lead_id', 'Messages')

    @api.one
    def get_default_analytic(self):
        """
        Gives id of analytic for this case
        """
        return self.env['crm.analytic.timesheet.configuration'].search([('model', '=', self._name)]).analytic_account_id.id

    @api.multi
    def _onchange_partner_id(self, partner_id, email=False):
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
                'partner_address_id': False,
                'email_from': False,
                'phone': False,
                'analytic_account_id': False,
            }}

        partner = self.env['res.partner'].browse(partner_id)
        address = partner.address_get(['contact'])
        data = {'partner_address_id': address['contact']}
        data.update(self.onchange_partner_address_id(address['contact'])['value'])
        for timesheet in partner.crm_analytic_ids:
            if timesheet.crm_model_id.model == self._name:
                data['analytic_account_id'] = timesheet.analytic_account_id.id

        return {'value': data}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
