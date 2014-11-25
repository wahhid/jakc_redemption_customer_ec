from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

class rdm_customer_config(osv.osv):
    _name = 'rdm.customer.config'
    _description = 'Redemption Customer Config'
    
    def get_customer_config(self, cr, uid, context=None):
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            return self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context)
        else:
            return None
            
    _columns = {
        'enable_referal' : fields.boolean('Enable Referal'),
        'referal_point': fields.integer('Referal Point'),
        'expired_duration': fields.integer('Expired Duration'),
        'state': fields.boolean('Status'),
    }
    _defaults = {
        'enable_referal': lambda *a: False,
        'referal_point': lambda *a: 0,
        'expired_duration': lambda *a: 0,
        'state': lambda *a: True,
        
    }
rdm_customer_config()

class rdm_customer_config_settings(osv.osv_memory):
    _name = 'rdm.customer.config.settings'
    _inherit = 'res.config.settings'
    _columns = {
        'enable_referal': fields.boolean('Enable Referal'),
        'referal_point': fields.integer('Referal Point'),
        'expired_duration': fields.integer('Expired Duration'),
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
        customer_config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        enable_referal=config.enable_referal
        self.pool.get('rdm.customer.config').write(cr, uid, customer_config_ids, {'enable_referal': enable_referal})

    def get_default_referal_point(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            referal_point = self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context).referal_point
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            referal_point = 0
        return {'referal_point': referal_point}
    
    def set_default_referal_point(self, cr, uid, ids, context=None):
        customer_config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        referal_point=config.referal_point
        self.pool.get('rdm.customer.config').write(cr, uid, customer_config_ids, {'referal_point': referal_point})
        
        
    def get_default_expired_duration(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            expired_duration = self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context).expired_duration
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            expired_duration = 0
        return {'expired_duration': expired_duration}
    
    def set_default_expired_duration(self, cr, uid, ids, context=None):
        customer_config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        expired_duration=config.expired_duration
        self.pool.get('rdm.customer.config').write(cr, uid, customer_config_ids, {'expired_duration': expired_duration})
