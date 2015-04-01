from openerp.osv import fields, osv
import logging

_logger = logging.getLogger(__name__)

class rdm_customer_config(osv.osv):
    _name = 'rdm.customer.config'
    _description = 'Redemption Customer Config'
    
    def get_config(self, cr, uid, context=None):
        ids = self.search(cr, uid, [('state','=', True),], context=context)
        if ids:
            return self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context)
        else:
            return None
            
    _columns = {
        'enable_new_member': fields.boolean('Enable New Member'),
        'new_member_email_tmpl': fields.integer('New Member Email'),
        'new_member_point': fields.integer('New Member Point'),
        'new_member_expired_duration': fields.integer('New Member Expired Duration'),        
        'enable_referal': fields.boolean('Enable Referal'),
        'referal_email_tmpl': fields.integer('Referral Email'),
        'referal_point': fields.integer('Referal Point'),
        'expired_duration': fields.integer('Expired Duration'),
        'reset_password_email_tmpl': fields.integer('Reset Password Email'),        
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
        'enable_new_member': fields.boolean('Enable New Member'),
        'new_member_email_tmpl': fields.many2one('email.template','New Member Email'),
        'new_member_point': fields.integer('New Member Point'),
        'new_member_expired_duration': fields.integer('New Member Expired Duration'),        
        'enable_referal': fields.boolean('Enable Referal'),
        'referal_email_tmpl': fields.many2one('email.template','Referral Email'),
        'referal_point': fields.integer('Referal Point'),        
        'expired_duration': fields.integer('Expired Duration'),
        'reset_password_email_tmpl': fields.many2one('email.template','Reset Password Email'),
        'duplicate_email': fields.boolean('Duplicate Email'), 
        'duplicate_social_id': fields.boolean('Duplicate Social ID'),
    }


    def get_default_enable_new_member(self, cr, uid, fields, context=None):
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            enable_new_member = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).enable_new_member
        else: 
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            enable_new_member = False
        return {'enable_new_member': enable_new_member}

    def set_default_enable_new_member(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        enable_new_member=config.enable_new_member
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'enable_new_member': enable_new_member})

    def get_default_new_member_email_tmpl(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            new_member_email_tmpl = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).new_member_email_tmpl
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            new_member_email_tmpl = 0
        return {'new_member_email_tmpl': new_member_email_tmpl}
    
    def set_default_new_member_email_tmpl(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        new_member_email_tmpl=config.new_member_email_tmpl
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'new_member_email_tmpl': new_member_email_tmpl})

    def get_default_new_member_point(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            new_member_point = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).new_member_point
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            new_member_point = 0
        return {'new_member_point': new_member_point}
    
    def set_default_new_member_point(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        new_member_point=config.new_member_point
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'new_member_point': new_member_point})
            
    def get_default_new_member_expired_duration(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            new_member_expired_duration = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).new_member_expired_duration
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            new_member_expired_duration = 0
        return {'new_member_expired_duration': new_member_expired_duration}
    
    def set_default_new_member_expired_duration(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        new_member_expired_duration=config.new_member_expired_duration
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'new_member_expired_duration': new_member_expired_duration})


    def get_default_enable_referal(self, cr, uid, fields, context=None):
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            enable_referal = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).enable_referal
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

    def get_default_referal_email_tmpl(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            referal_email_tmpl = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).referal_email_tmpl
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            referal_email_tmpl = 0
        return {'referal_email_tmpl': referal_email_tmpl}
    
    def set_default_referal_email_tmpl(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        referal_email_tmpl=config.referal_email_tmpl
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'referal_email_tmpl': referal_email_tmpl})
        
    def get_default_referal_point(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            referal_point = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).referal_point
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
            expired_duration = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).expired_duration
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
        
        
    def get_default_reset_password_email_tmpl(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            reset_password_email_tmpl = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).reset_password_email_tmpl
        else:
            customer_data = {}
            result_id = self.pool.get('rdm.customer.config').create(cr, uid, customer_data, context=context)
            reset_password_email_tmpl = 0
        return {'reset_password_email_tmpl': reset_password_email_tmpl}
    
    def set_default_reset_password_email_tmpl(self, cr, uid, ids, context=None):
        config_ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        config = self.browse(cr, uid, ids[0], context)
        reset_password_email_tmpl=config.reset_password_email_tmpl
        self.pool.get('rdm.customer.config').write(cr, uid, config_ids, {'reset_password_email_tmpl': reset_password_email_tmpl})
        
    def get_default_duplicate_email(self, cr, uid, fields, context=None):    
        ids = self.pool.get('rdm.customer.config').search(cr, uid, [('state','=', True),], context=context)
        if ids:
            duplicate_email = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).duplicate_email
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
            duplicate_social_id = self.pool.get('rdm.customer.config').browse(cr, uid, ids[0], context=context).duplicate_social_id
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
