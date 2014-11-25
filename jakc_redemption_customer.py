from openerp.osv import fields, osv
from datetime import datetime
from datetime import timedelta
import logging

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

class rdm_customer(osv.osv):
    _name = 'rdm.customer'
    _description = 'Redemption Customer'
    
    def set_black_list(self, cr, uid, id, context=None):
        _logger.info("Blacklist ID : " + str(id))    
        self.write(cr,uid,id,{'state': 'blacklist'},context=context)
        #email_data = {}*
        #email_data['start_logger'] = 'Start Request Customer Blacklist Notification'
        #email_data['email_from'] = 'whidayat@taman-anggrek-mall.com'
        #email_data['email_to'] = 'whidayat@taman-anggrek-mall.com'
        #email_data['subject'] = "Request Blacklist For ID : "  + id
        #email_data['body_html'] = "Dear Supervisor <br/><br/> Please Approve"
        #email_data['end_logger'] = 'End Email Ticket Conversation Notification'
        #self._send_email_notification(cr, uid, email_data, context=context)                                 
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
        
    def _get_trans(self, cr, uid, trans_id , context=None):
        return self.browse(cr, uid, trans_id, context=context);
    
    def _add_referal_point(self, cr, uid, id, context=None):
        _logger.info("Start Add Referal Point : " + str(id[0]))
        
        _logger.info("End Add Referal Point : " + str(id[0]))
        
    def _referal_process(self, cr, uid, id, context=None):
        _logger.info("Start Referal Process : " + str(id[0]))
        customer_config = self.pool.get('rdm.customer.config').get_customer_config(cr, uid, context=context)
        if customer_config.enable_referal:
            trans_id = id[0]
            trans = self._get_trans(cr, uid, trans_id, context)
            if trans.ref_id:
                _logger.info('Add Referal Point')
                self._generate_referal_point(cr, uid, trans_id, trans.ref_id.id, customer_config.referal_point, customer_config.expired_duration, context=context)
            else:
                _logger.info('No Referal Point')    
        return True 
    
    def _generate_referal_point(self, cr, uid, trans_id, customer_id, point, expired_duration, context=None):
        _logger.info('Start Generate Point')
        trans = self._get_trans(cr, uid, trans_id, context)
        point_data = {}
        point_data.update({'customer_id': customer_id})
        point_data.update({'trans_id':str(trans.id)})
        point_data.update({'trans_type': 'reference'})
        point_data.update({'point':point})
        expired_date = datetime.now() + timedelta(days=expired_duration)
        point_data.update({'expired_date': expired_date})
        self.pool.get('rdm.customer.point').create(cr, uid, point_data, context=context)
        _logger.info('End Generate Coupon')
        
    def _send_email_notification(self, cr, uid, values, context=None):
        _logger.info(values['Start Send Email Notification'])
        mail_mail = self.pool.get('mail.mail')
        mail_ids = []
        mail_ids.append(mail_mail.create(cr, uid, {
            'email_from': values['email_from'],
            'email_to': values['email_to'],
            'subject': values['subject'],
            'body_html': values['body_html'],
            }, context=context))
        mail_mail.send(cr, uid, mail_ids, context=context)
        _logger.info(values['End Send Email Notification'])          
            

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
        'email': fields.char('Email',size=100, required=True),
        'password': fields.char('Password',size=20),
        'zone': fields.many2one('rdm.customer.zone','Residential Zone'),
        'education': fields.many2one('rdm.customer.education', 'Education'),
        'card_type': fields.many2one('rdm.card.type', 'Card Type', required=True),
        'interest': fields.many2one('rdm.customer.interest','Interest'),
        'ref_id': fields.many2one('rdm.customer','Refferal'),
        'receive_email': fields.boolean('Receive Email'),
        'join_date': fields.date('Join Date'),                         
        'state': fields.selection(AVAILABLE_STATES, 'Status', size=16, readonly=True),    
        'deleted': fields.boolean('Deleted',readonly=True),       
    }
    
    _defaults = {
         'contact_type': lambda *a : 'customer',               
         'state': lambda *a: 'draft',
         'deleted': lambda *a: False,      
    }
    
    def create(self, cr, uid, values, context=None):
        if 'tenant_id' in values.keys():                        
            tenant_id = values['tenant_id']
            if tenant_id is not None:
                values.update({'contact_type': 'tenant'})                            
        id =  super(rdm_customer, self).create(cr, uid, values, context=context)    
        self.set_enable(cr, uid, [id], context)
        self._referal_process(cr, uid, [id], context)
        #Send Email Notification    
        return id                            
    
rdm_customer()

