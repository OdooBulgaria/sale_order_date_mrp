from openerp.osv import fields, osv
from openerp import api
from openerp.tools.translate import _
from datetime import datetime,timedelta
from openerp.tools import  DEFAULT_SERVER_DATETIME_FORMAT

class sale_order_line(osv.osv):
    _inherit = 'sale.order.line'
    
    def _calc_date(self, cr, uid, ids, name, arg, context=None):
        res = {}
        
        for object in self.browse(cr,uid,ids,context):
            list = []
            if object.mo_id:
                lead_time = object.mo_id.location_src_id.company_id.manufacturing_lead or 0
                if object.mo_id.workcenter_lines:
                    for line in object.mo_id.workcenter_lines:
                        list.append(line.date_planned_end)
                    date = datetime.strptime(max(list), DEFAULT_SERVER_DATETIME_FORMAT)
                    date = date +timedelta(days=lead_time)
                    res.update({object.id:date.strftime(DEFAULT_SERVER_DATETIME_FORMAT)})
        return res
    
    _columns = {
                'expected_date':fields.function(_calc_date,type="datetime",string = 'Expected Date of Completion'),
                'mo_id':fields.many2one('mrp.production','Manufacturing Order',readonly=True)
                }
    
    
