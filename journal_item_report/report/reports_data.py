from dateutil.relativedelta import relativedelta

from odoo import models, api
from datetime import date
from datetime import timedelta, datetime


class JournalItemsReport(models.AbstractModel):
    _name = 'report.journal_item_report.journal_item_report_pdf'
    _description = 'Journal Items  Report'

    @api.model
    def _get_report_values(self, docids, data=None):
        val_list = []
        # selected_ids = self.env.context.get('active_ids', [])
        print(self.id)
        selected_records = self.env['account.move.line'].browse(docids)
        print(selected_records)
        for rec in selected_records:
            val_list.append(rec.id)
            print(rec)
        print(val_list)
        return {
            'doc_ids': docids,
            'docs': selected_records,
            'doc_model': 'account.move.line',
            # 'invoices' : invoices
        }
