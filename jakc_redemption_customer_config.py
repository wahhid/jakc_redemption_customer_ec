from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

class rdm_customer_config(osv.osv):
    _name = 'rdm.customer.config'
    _description = 'Redemption Customer Config'
    
    def get_config(self, cr, uid, context=None):
        ids = self.search(cr, uid, [('state','=', True),], context=context)
        if ids:
            return self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context)
        else:
            return None
            
    _columns = {
        'enable_referal' : fields.boolean('Enable Referal'),
        'referal_point': fields.integer('Referal Point'),
        'expired_duration': fields.integer('Expired Duration'),
        'duplicate_email': fields.boolean('Duplicate Email'), 
        'duplicate_social_id': fields.boolean('Duplicate Social ID'),
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
        'duplicate_email': fields.boolean('Duplicate Email'), 
        'duplicate_social_id': fields.boolean('Duplicate Social ID'),
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
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        enable_referal=config.enable_referal
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'enable_referal': enable_referal})

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
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        referal_point=config.referal_point
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'referal_point': referal_point})
        
        
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
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        expired_duration=config.expired_duration
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'expired_duration': expired_duration})
        
    def get_default_duplicate_email(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            duplicate_email = self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context).duplicate_email
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            duplicate_email = False
        return {'duplicate_email': duplicate_email}
    
    def set_default_duplicate_email(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        duplicate_email=config.duplicate_email
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'duplicate_email': duplicate_email})
        
    
    def get_default_duplicate_social_id(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            duplicate_social_id = self.pool.get('rdm.customer.config').browse(cr, uid, uid, context=context).duplicate_social_id
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            duplicate_social_id = False
        return {'duplicate_social_id': duplicate_social_id}
    
    def set_default_duplicate_social_id(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        duplicate_social_id=config.duplicate_social_id
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'duplicate_social_id': duplicate_social_id})
