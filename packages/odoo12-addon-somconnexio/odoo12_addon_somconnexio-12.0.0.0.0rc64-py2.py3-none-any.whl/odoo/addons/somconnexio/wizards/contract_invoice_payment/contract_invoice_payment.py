from odoo import api, fields, models, _
import base64
from odoo.exceptions import UserError
import csv


class ContractInvoicePayment(models.TransientModel):
    _name = 'contract.invoice.payment.wizard'
    data = fields.Binary("Upload file")

    @api.multi
    def run_wizard(self):
        decoded_data = base64.b64decode(self.data)
        f = (line.strip() for line in decoded_data.decode('utf-8').split('\n'))
        fr = csv.DictReader(f)
        errors = []
        for row in fr:
            invoice = self.env['account.invoice'].search(
                [('name', '=', row['Invoice number'])]
            )
            if not invoice:
                errors.append(_(
                    "The invoice {} has not be found".format(row['Invoice number'])
                ))
                continue
            contract = self.env['contract.contract'].search(
                [('code', '=', row['Subscription code'])]
            )
            if not contract:
                errors.append(_(
                    "The contract {} has not be found".format(row['Subscription code'])
                ))
                continue
            invoice.payment_term_id = contract.payment_term_id
            invoice.payment_mode_id = contract.payment_mode_id
            invoice.mandate_id = contract.mandate_id
        if errors:
            raise UserError('\n'.join(errors))
        return True
