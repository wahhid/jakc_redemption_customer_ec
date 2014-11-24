from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)


class rdm_customer_config(osv.osv):
    _name = 'rdm.customer.config'
    _description = 'Redemption Customer Config'
    _columns = {
        'enable_referal' : fields.boolean('Enable Referal'),
        'state': fields.boolean('Status'),
    }
    _defaults = {
        'enable_referal': lambda *a: False,
        'state': lambda *a: True,
    }
rdm_customer_config()

class rdm_customer_config_settings(osv.osv_memory):
    _name = 'rdm.customer.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'enable_referal': fields.boolean('Enable Referal'),
    }
    _defaults = {
        'enable_referal': False,
    }

    def get_default_enable_referal(self, cr, uid, fields, context=None):
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            enable_referal = self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context).enable_referal
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            enable_referal = False
        return {'enable_referal': enable_referal}


    def set_default_enable_referal(self, cr, uid, ids, context=None):
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        enable_referal=config.enable_referal
        self.pool.get('rdm.customer.config').write(cr, uid, ids, {'enable_referal': enable_referal})
