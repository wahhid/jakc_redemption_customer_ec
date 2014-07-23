from openerp.osv import fields, osv

class rdm_customer(osv.osv):
    _name = 'rdm.customer'
    _description = 'Redemption Customer'
    _columns = {
        'type': fields.many2one('rdm.customer.type','Type'),
        'old_ayc_number': fields.char('Old AYC #', size=50),
        'ayc_number': fields.char('AYC #', size=50),        
        'name': fields.char('Name', size=200),        
        'birth_place': fields.char('Birth Place', size=100),
        'birth_date': fields.date('Birth Date'),
        'gender': fields.many2one('rdm.customer.gender','Gender'),
        'ethnic': fields.many2one('rdm.customer.ethnic','Ethnic'),
        'religion': fields.many2one('rdm.customer.religion','Religion'),
        'marital': fields.many2one('rdm.customer.marital','Marital'),
        'social_id': fields.char('ID or Passport', size=50),
        'address': fields.text('Address'),
        'province': fields.many2one('rdm.province','Province'),
        'city': fields.many2one('rdm.city','City'),
        'zipcode': fields.char('Zipcode', size=10),
        'phone1': fields.char('Phone 1', size=20),
        'phone2': fields.char('Phone 2', size=20),
        'mobile_phone1': fields.char('Mobile Phone 1', size=20),
        'mobile_phone2': fields.char('Mobile Phone 2', size=20),
        'email': fields.char('Email',size=100),
        'zone': fields.many2one('rdm.customer.zone','Residential Zone'),
        'education': fields.many2one('rdm.customer.education', 'Education'),
        'card_type': fields.many2one('rdm.card.type', 'Card Type'),
        'interest': fields.many2one('rdm.customer.interest','Interest'),
        'ref_id': fields.many2one('rdm.customer','Refferal'),
        'receive_email': fields.boolean('Receive Email'),
        'join_date': fields.date('Join Date'),                
    }        
    
rdm_customer()
