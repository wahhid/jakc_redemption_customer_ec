from openerp.osv import fields, osv
from datetime import datetime
from datetime import timedelta
from datetime import date
import re
import logging
import string
import random

_logger = logging.getLogger(__name__)


AVAILABLE_STATES = [
    ('draft','New'),    
    ('active','Active'),
    ('blacklist','Black List'),    
    ('disable', 'Disable'),
]

CONTACT_TYPES = [
    ('customer','Customer'),
    ('tenant','Tenant'),
    ('both','Customer or Tenant'),    
]


class rdm_customer_change_password(osv.osv_memory):
    _name = "rdm.customer.change.password"
    _description = "Redemption Customer Change Password" 
        
    def change_password(self, cr, uid, ids, context=None):                
        params = self.browse(cr, uid, ids, context=context)
        param = params[0]           
        customer_id = context.get('customer_id',False)
        data = {}              
        if param.password_new == param.password_confirm:
            data.update({'password':param.password_new})
            self.pool.get('rdm.customer').write(cr, uid, [customer_id], data, context=context)                                                
        return True
    
    _columns = {
        'password_new': fields.char('New Password', size=50),
        'password_confirm': fields.text('Confirm Password', size=50),
    }    
       
rdm_customer_change_password()

class rdm_customer(osv.osv):
    _name = 'rdm.customer'
    _description = 'Redemption Customer'
    
    def set_black_list(self, cr, uid, id, context=None):
        _logger.info("Blacklist ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'blacklist'},context=context)
        return True
    
    def set_remove_black_list(self, cr, uid, id, context=None):
        _logger.info("Reset Blacklist ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'active'},context=context)              
        return True
    
    def set_disable(self, cr, uid, id, context=None):
        _logger.info("Activate ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'disable'},context=context)              
        return True
    
    def set_enable(self, cr, uid, id, context=None):
        _logger.info("Reset activate ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'active'},context=context)              
        return True    
        
    def get_trans(self, cr, uid, trans_id , context=None):
        return self.browse(cr, uid, trans_id, context=context);
    
    def change_password(self, cr, uid, ids, context=None):
        return {
               'type': 'ir.actions.act_window',
               'name': 'Change Password',
               'view_mode': 'form',
               'view_type': 'form',                              
               'res_model': 'rdm.customer.change.password',
               'nodestroy': True,
               'target':'new',
               'context': {'customer_id': ids[0]},
        } 
    
    def reset_password(self, cr, uid, ids, context=None):
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        rdm_customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)
        
        new_password = self._password_generator(cr, uid, context)
        customer_data = {}
        customer_data.update({'password':new_password})
        self.write(cr, uid, ids, customer_data, context=context)
        if rdm_config.enable_email and trans.receive_email:
            email_obj = self.pool.get('email.template')        
            template_ids = rdm_customer_config.reset_password_email_tmpl
            email = email_obj.browse(cr, uid, template_ids)  
            email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
            email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)
            _logger.info('Send Change Password Email Notification')
                              
    def _password_generator(self, cr, uid ,context=None):
        size = 10
        chars= string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(size))
        
        
    def _add_new_member_point(self, cr, uid, ids, context=None):
        _logger.info("Start Add New Member Point")        
        rdm_customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)        
        if rdm_customer_config.enable_new_member:
            trans_id = ids[0]
            trans = self.get_trans(cr, uid, trans_id, context)            
            new_member_point = rdm_customer_config.new_member_point
            point_data = {}
            point_data.update({'customer_id': trans.id})            
            point_data.update({'trans_type': 'member'})
            point_data.update({'point':new_member_point})
            expired_date = datetime.today()+timedelta(rdm_customer_config.new_member_expired_duration)
            point_data.update({'expired_date': expired_date.strftime('%Y-%m-%d')})
            self.pool.get('rdm.customer.point').create(cr, uid, point_data, context=context)
        _logger.info("End Add New Member Point")
            
    def _add_referal_point(self, cr, uid, ids, context=None):        
        _logger.info("Start Add Referal Point : " + str(id[0]))
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context)        
        rdm_customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)    
        if rdm_customer_config.enable_new_member:
            referal_point = rdm_customer_config.referal_point
            point_data = {}
            point_data.update({'customer_id': trans.id})            
            point_data.update({'trans_type': 'reference'})
            point_data.update({'point':referal_point})
            expired_date = datetime.today()+timedelta(rdm_customer_config.expired_duration)
            point_data.update({'expired_date': expired_date.strftime('%Y-%m-%d')})
            self.pool.get('rdm.customer.point').create(cr, uid, point_data, context=context)
        _logger.info("End Add Referal Point")
    
    def _new_member_process(self, cr, uid, ids, context=None):
        _logger.info("Start New Member Process : " + str(ids[0]))
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)
        if customer_config.enable_new_member:
            self._add_new_member_point(cr, uid, ids, context)
            trans_id = ids[0]
            trans = self.get_trans(cr, uid, trans_id, context)                
            #Send Email
            if trans.receive_email and rdm_config.enable_email:            
                _logger.info('Send Email New Member')
                email_obj = self.pool.get('email.template')        
                template_ids = customer_config.new_member_email_tmpl
                email = email_obj.browse(cr, uid, template_ids)  
                email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
                email_obj.send_mail(cr, uid, template_ids, ids[0], True, context=context)                                                            
        _logger.info("End New Member Process")
        
    def _referal_process(self, cr, uid, ids, context=None):
        _logger.info("Start Referal Process : " + str(ids[0]))
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)
        customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)
        if customer_config.enable_referal:
            trans_id = ids[0]
            trans = self.get_trans(cr, uid, trans_id, context)
            if trans.ref_id:
                self._add_referal_point(cr, uid, [trans.ref_id.id], context)
                #Send Email
                if trans.ref_id.receive_email and rdm_config.enable_email:
                    _logger.info('Send Email Referal')
                    email_obj = self.pool.get('email.template')        
                    template_ids = customer_config._email_tmpl
                    email = email_obj.browse(cr, uid, template_ids)  
                    email_obj.write(cr, uid, template_ids, {'email_from': email.email_from,
                                                    'email_to': email.email_to,
                                                    'subject': email.subject,
                                                    'body_html': email.body_html,
                                                    'email_recipients': email.email_recipients})
                    email_obj.send_mail(cr, uid, template_ids, trans.id, True, context=context)           
            else:
                _logger.info('No Referal Point')    
        return True 
            
    def check_duplicate(self, cr, uid, values, context=None):      
        customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)
        if customer_config.duplicate_email:
            if values.get('email_required'):                        
                customer_ids = self.search(cr, uid, [('email','=',values.get('email')),], context=context)
                if customer_ids:
                    return True,'Email Duplicate'                            
        if customer_config.duplicate_social_id:
            customer_ids = self.search(cr, uid, [('social_id','=',values.get('social_id')),], context=context)
            if customer_ids:
                return True,'Social ID Duplicate'
        return False,'Not Duplicate' 
    
    def onchange_mobil_phone1_number(self, cr, uid, ids, mobile_phone1, context={}):
        if not mobile_phone1:
            return {'value':{}}            
        return {'value':{'mobile_phone1':mobile_phone1}}
    
    def onchange_mobile_phone2_number(self, cr, uid, ids, mobile_phone2, context={}):
        if not mobile_phone2:
            return {'value':{}}                
        return {'value':{'mobile_phone2':mobile_phone2}}    
    
    def _send_email_notification(self, cr, uid, values, context=None):
        _logger.info('Start Send Email Notification')
        mail_mail = self.pool.get('mail.mail')
        mail_ids = []
        mail_ids.append(mail_mail.create(cr, uid, {
            'email_from': values['email_from'],
            'email_to': values['email_to'],
            'subject': values['subject'],
            'body_html': values['body_html'],
            }, context=context))
        mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info('End Send Email Notification')          
            
    def send_create_email_notification(self, cr, uid, ids, context=None):
        trans_id = ids[0]
        trans = self.get_trans(cr, uid, trans_id, context=context)
        rdm_config = self.pool.get('rdm.config').get_config(cr, uid, context=context)                
        if rdm_config and rdm_config.enable_email and trans.receive_email:
            rdm_customer_config = self.pool.get('rdm.customer.config').get_config(cr, uid, context=context)
            if rdm_customer_config.enable_new_member:
                self.send_mail_to_new_customer(cr, uid, ids, context)
            if rdm_customer_config.enable_referal:
                self.send_mail_to_referal_customer(cr, uid, ids, context)
            
    _columns = {                    
        'type': fields.many2one('rdm.customer.type','Type'),        
        'contact_type': fields.selection(CONTACT_TYPES,'Contact Type',size=16),            
        'old_ayc_number': fields.char('Old AYC #', size=50),
        'ayc_number': fields.char('AYC #', size=50),        
        'name': fields.char('Name', size=200, required=True),
        'title': fields.many2one('rdm.tenant.title','Title'),        
        'birth_place': fields.char('Birth Place', size=100),
        'birth_date': fields.date('Birth Date', required=True),
        'gender': fields.many2one('rdm.customer.gender','Gender', required=True),
        'ethnic': fields.many2one('rdm.customer.ethnic','Ethnic'),
        'religion': fields.many2one('rdm.customer.religion','Religion'),
        'marital': fields.many2one('rdm.customer.marital','Marital'),
        'social_id': fields.char('ID or Passport', size=50, required=True),
        'address': fields.text('Address'),
        'province': fields.many2one('rdm.province','Province'),
        'city': fields.many2one('rdm.city','City'),
        'zipcode': fields.char('Zipcode', size=10),
        'phone1': fields.char('Phone 1', size=20),
        'phone2': fields.char('Phone 2', size=20),
        'mobile_phone1': fields.char('Mobile Phone 1', size=20, required=True),
        'mobile_phone2': fields.char('Mobile Phone 2', size=20),                
        'email': fields.char('Email',size=100),
        'email_required': fields.boolean('Email Required'),
        'password': fields.char('Password',size=20),
        'zone': fields.many2one('rdm.customer.zone','Residential Zone'),
        'education': fields.many2one('rdm.customer.education', 'Education'),
        'card_type': fields.many2one('rdm.card.type', 'Card Type',),
        'interest': fields.many2one('rdm.customer.interest','Interest'),
        'ref_id': fields.many2one('rdm.customer','Refferal'),
        'receive_email': fields.boolean('Receive Email'),
        'join_date': fields.date('Join Date'),                         
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),    
        'deleted': fields.boolean('Deleted',readonly=True),       
    }
    
    _defaults = {
         'contact_type': lambda *a : 'customer',
         'email_required': lambda *a: True,         
         'join_date': fields.date.context_today,               
         'state': lambda *a: 'draft',
         'deleted': lambda *a: False,      
    }
    
    def create(self, cr, uid, values, context=None):
        #Upper Case Name
        if 'name' in values.keys():
            name = values.get('name')
            values.update({'name':name.upper()})

        if 'tenant_id' in values.keys():                        
            tenant_id = values['tenant_id']
            if tenant_id is not None:
                values.update({'contact_type': 'tenant'})
        
        #Lower Case Email    
        if 'email' in values.keys():
            email = values.get('email')
            if email:
                values.update({'email':email.lower()})
            
        #Mobile Phone 1          
        if 'mobile_phone1' in values.keys():            
            mobile_phone1 = values.get('mobile_phone1')
            if mobile_phone1:
                if mobile_phone1[0:3] == '+62':
                    values.update({'mobile_phone1':mobile_phone1})
                elif mobile_phone1[0] == '0':
                    mobile_phone1 = '+62' + mobile_phone1[1:len(mobile_phone1)-1]                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 1 format should be start with +62 or 0'))       

        #Mobile Phone 1        
        if 'mobile_phone2' in values.keys():            
            mobile_phone2 = values.get('mobile_phone2')
            if mobile_phone2:
                if mobile_phone2[0:3] == '+62':
                    values.update({'mobile_phone2':mobile_phone2})
                elif mobile_phone2[0] == '0':
                    mobile_phone2 = '+62' + mobile_phone2[1:len(mobile_phone2)-1]                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 2 format should be start with +62 or 0'))       
        
        #Generate Password        
        values.update({'password':self._password_generator(cr, uid, context=context)})
        
        #Checks Duplicate Customer
        is_duplicate, message = self.check_duplicate(cr, uid, values, context=context)

        if is_duplicate:
            raise osv.except_osv(('Warning'), (message))
        else:                           
            #Create Customer         
            id =  super(rdm_customer, self).create(cr, uid, values, context=context)
                
            #Enable Customer
            self.set_enable(cr, uid, [id], context)
            
            #Process New Member and Generate Point if Enable
            self._new_member_process(cr, uid, [id], context)
            
            #Process Referal and Generate Point For Reference Customer If Enable
            self._referal_process(cr, uid, [id], context)
            
            #Send Email Notification for Congrat and Customer Web Access Password
            #self.send_create_email_notification(cr, uid, [id], context)
                        
            return id 
        
    def write(self, cr, uid, ids, values, context=None):
        #Upper Case Name
        if 'name' in values.keys():
            name = values.get('name')
            values.update({'name':name.upper()})

        #Lower Case Email
        if 'email' in values.keys():
            email = values.get('email')
            if email:
                values.update({'email':email.lower()}) 
                                            
        #Mobile Phone 1        
        if 'mobile_phone1' in values.keys():            
            mobile_phone1 = values.get('mobile_phone1')
            if mobile_phone1:
                if mobile_phone1[0:3] == '+62':
                    values.update({'mobile_phone1':mobile_phone1})
                elif mobile_phone1[0] == '0':
                    mobile_phone1 = '+62' + mobile_phone1[1:len(mobile_phone1)-1]
                    values.update({'mobile_phone1':mobile_phone1})                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 1 format should be start with +62 or 0'))       

        #Mobile Phone 1        
        if 'mobile_phone2' in values.keys():            
            mobile_phone2 = values.get('mobile_phone2')
            if mobile_phone2:
                if mobile_phone2[0:3] == '+62':
                    values.update({'mobile_phone2':mobile_phone2})
                elif mobile_phone2[0] == '0':
                    mobile_phone2 = '+62' + mobile_phone2[1:len(mobile_phone2)-1]
                    values.update({'mobile_phone2':mobile_phone2})                
                else:                
                    raise osv.except_osv(('Warning'), ('Mobile Phone 2 format should be start with +62 or 0'))       
                                            
        is_duplicate, message = self.check_duplicate(cr, uid, values, context=context)

        if is_duplicate:
            raise osv.except_osv(('Warning'), (message))
        else:
            return super(rdm_customer,self).write(cr, uid, ids, values, context=context)
            
rdm_customer()

