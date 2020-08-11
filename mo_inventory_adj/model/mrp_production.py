# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from datetime import datetime
from dateutil.relativedelta import relativedelta

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from odoo.tools import float_compare, float_round
from odoo.addons import decimal_precision as dp

class MrpProduction(models.Model):
    _inherit = 'mrp.production'

    def action_open_MO_inventory_adjustment(self):
        line_ids = []
        result = {
            'view_type': 'form',
            "view_mode": 'form',
            'res_model': 'stock.inventory',
            'type': 'ir.actions.act_window',
            # 'target': 'new'
            }
        for mrp in self:
            if mrp.move_raw_ids:
                for line in mrp.move_raw_ids.filtered(lambda x: x.state != 'cancel'):
                    if line_ids and line.product_id.id not in (x[2]['product_id'] for x in line_ids):
                        self.env.cr.execute("""SELECT sum(quantity) as product_qty
                        FROM stock_quant
                        LEFT JOIN product_product
                        ON product_product.id = stock_quant.product_id
                        WHERE stock_quant.product_id = %s and stock_quant.location_id = %s""", (line.product_id.id, line.location_id.id))
                        record = self.env.cr.dictfetchone()
                        line_dict = {
                                        'product_id': line.product_id.id,
                                        'product_uom_id': line.product_uom.id,
                                        'location_id': line.location_id.id,
                                        'theoretical_qty': record['product_qty'],
                                        'product_qty': record['product_qty']
                                    }
                        line_ids.append((0, 0, line_dict))
                    if not line_ids:
                        self.env.cr.execute("""SELECT sum(quantity) as product_qty
                        FROM stock_quant
                        LEFT JOIN product_product
                        ON product_product.id = stock_quant.product_id
                        WHERE stock_quant.product_id = %s and stock_quant.location_id = %s""", (line.product_id.id, line.location_id.id))
                        record = self.env.cr.dictfetchone()
                        line_dict = {
                                        'product_id': line.product_id.id,
                                        'product_uom_id': line.product_uom.id,
                                        'location_id': line.location_id.id,
                                        'theoretical_qty': record['product_qty'],
                                        'product_qty': record['product_qty']
                                    }
                        line_ids.append((0, 0, line_dict))
        view_id = self.env['ir.model.data'].get_object_reference('stock', 'view_inventory_form')[1]
        if view_id:
            result['view_id'] = [view_id]
        res_id = self.env['stock.inventory'].search([('name', '=', self.name), ('state', '=', 'confirm')])
        if res_id:
            result['res_id'] = res_id.id
        else:
            result['context'] = {
                            'default_name': self.name,
                            'default_location_id': self.move_raw_ids[0].location_id.id,
                            'default_filter': 'partial',
                            'default_state': 'confirm',
                            'default_line_ids': line_ids,
                            }
        return result
