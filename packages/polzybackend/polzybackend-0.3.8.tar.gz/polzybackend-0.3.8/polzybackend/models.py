from polzybackend import db, auth
from polzybackend.utils import generate_id, date_format
from polzybackend.utils.auth_utils import generate_token, get_expired, is_supervisor, load_attributes
from datetime import datetime, date
from sqlalchemy import and_
from functools import reduce
import json


# authentication
@auth.verify_token
def verify_token(token):
    #user = User.query.filter_by(access_key=token).first()
    user = db.session.query(User).filter_by(access_key=token).first()
    if user and user.key_expired > datetime.utcnow():
        #db.session.expire_on_commit = False
        db.session.expunge(user)
        return user


#
# Authentication Models
#

#
# Association Models
#

# association table for user-role relation
user_company_roles = db.Table(
    'user_company_roles',
    db.Column('user_id', db.String(56), db.ForeignKey('users.id'), primary_key=True),
    db.Column('company_id', db.String(56), db.ForeignKey('companies.id'), primary_key=True),
    db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True)
)


class CompanyToCompany(db.Model):
    #
    # association object between companies
    #
    __tablename__ = 'company_company'
    parent_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    child_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    parent = db.relationship('Company', backref='child_companies', foreign_keys=[parent_id])
    child = db.relationship('Company', backref='parent_companies', foreign_keys=[child_id])


class UserToCompany(db.Model):
    #
    # association object between user and company
    #
    __tablename__ = 'user_company'
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), primary_key=True)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), primary_key=True)
    attributes = db.Column(db.String(1024), nullable=True)

    # relationships
    user = db.relationship(
        'User',
        lazy='subquery',
        backref='companies',
        foreign_keys=[user_id],
    )
    company = db.relationship(
        'Company',
        lazy='subquery',
        backref='users',
        foreign_keys=[company_id],
    )
    roles = db.relationship(
        'Role',
        lazy='subquery',
        secondary=user_company_roles,
        primaryjoin=and_(user_id == user_company_roles.c.user_id, company_id == user_company_roles.c.company_id),
        backref=db.backref('user_to_companies'),
    )

    def to_json(self):
        return {
            'id': self.company.id,
            'name': self.company.name,
            'displayedName': str(self.company),
            'attributes': load_attributes(self.company.attributes),
        }

    def to_admin_json(self):
        child_companies = CompanyToCompany.query.filter_by(parent_id=self.company_id).all()
        return {
            'id': self.company.id,
            'name': self.company.name,
            'displayedName': str(self.company),
            'childCompanies': [{
                'id': ch.child_id,
                'name': ch.child.name,
                'attributes': ch.attributes,
            } for ch in child_companies],
            'users': [{
                'id': u.user.id,
                'email': u.user.email,
                'roles': [r.name for r in u.roles],
                'attributes': u.attributes if u.attributes else '',
            } for u in self.company.users],
        }


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(16), unique=True, nullable=False)
    is_supervisor = db.Column(db.Boolean, nullable=False, default=False)


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    email = db.Column(db.String(64), unique=True, nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    displayed_name = db.Column(db.String(64), nullable=True)
    first_name = db.Column(db.String(64), nullable=True)
    last_name = db.Column(db.String(64), nullable=True)
    # oauth_provider_id = db.Column(db.Integer, db.ForeignKey('oauth_providers.id'), nullable=False)
    # oauth_user_id = db.Column(db.String(128), nullable=False)
    # oauth_token = db.Column(db.String(128), nullable=False)
    access_key = db.Column(db.String(128), nullable=False, default=generate_token)
    key_expired = db.Column(db.DateTime, nullable=False, default=get_expired)
    # current session attributes
    stage = db.Column(db.String(8), nullable=True)
    language = db.Column(db.String(8), nullable=True)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=True)

    # relationships
    # oauth_provider = db.relationship(
    #    'OAuthProvider',
    #    foreign_keys=[oauth_provider_id],
    # )
    company = db.relationship(
        'UserToCompany',
        primaryjoin=and_(
            id == UserToCompany.user_id,
            company_id == UserToCompany.company_id,
        ),
        uselist=False,
        lazy='subquery',
    )

    def __str__(self):
        return self.displayed_name or self.first_name or self.last_name or self.email.split('@')[0]

    def set_stage(self, stage):
        self.stage = stage
        db.session.commit()

    def set_language(self, language):
        self.language = language
        db.session.commit()

    def set_company(self, company_id=None, company=None):
        # check if either company data is provided
        if company_id is None and company is None:
            raise Exception('Neither Company ID nor Company provided')

        # check if company should be fetched
        if company is None:
            company = Company.query.get(company_id)
        
        # check if company exists
        if company is None:
            raise Exception('Company not found')

        # get UserToCompany instance
        user_company = UserToCompany.query.filter(and_(
            UserToCompany.user_id == self.id,
            UserToCompany.company_id == company.id,
        )).first()

        # check if association exists
        if user_company is None:
            raise Exception(f'User is not assigned to company ID {company_id}')

        # set company
        self.company_id = company.id
        db.session.commit()

        # return company json
        return user_company.to_json()

    def is_supervisor(self):
        return reduce(lambda result, company: result or is_supervisor(company), self.companies, False)

    def get_permissions(self):
        if self.company:
            user_roles = [r.name.lower() for r in self.company.roles]

            return {
                'policy': any(role in ['admin', 'clerk'] for role in user_roles),
                'antrag': any(role in ['admin', 'agent'] for role in user_roles),
            }

        return {
            'policy': False,
            'antrag': False,
        }

    def to_json(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': str(self),
            'isSupervisor': self.is_supervisor(),
            'stage': self.stage,
            'accessToken': self.access_key,
            'companies': [company.to_json() for company in self.companies],
        }

    def get_admin_json(self):
        return {
            'possibleRoles': [r.name for r in Role.query.all()],
            'companies': [company.to_admin_json() for company in filter(
                lambda company: is_supervisor(company),
                self.companies
            )],
        }


'''
class OAuthProvider(db.Model):
    __tablename__ = 'oauth_providers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    client_id = db.Column(db.String(128), nullable=False)
    secret_key = db.Column(db.String(128), nullable=False)

    def __str__(self):
        return self.name
'''


#
# Company Model
#
class Company(db.Model):
    __tablename__ = "companies"
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    name = db.Column(db.String(128), unique=True, nullable=False)
    displayed_name = db.Column(db.String(64), nullable=True)
    email = db.Column(db.String(32), nullable=True)
    phone = db.Column(db.String(16), nullable=True)
    country = db.Column(db.String(32), nullable=True)
    post_code = db.Column(db.String(8), nullable=True)
    city = db.Column(db.String(32), nullable=True)
    address = db.Column(db.String(64), nullable=True)
    attributes = db.Column(db.String(1024), nullable=True)

    def __str__(self):
        return self.displayed_name or self.name


#
# Activity Models
#
class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.String(56), primary_key=True, default=generate_id)
    creator_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    policy_number = db.Column(db.String(64), nullable=False)
    effective_date = db.Column(db.Date, nullable=False, default=date.today)
    type = db.Column(db.String(32), nullable=False)
    status = db.Column(db.String(64), nullable=True)
    finished = db.Column(db.DateTime, nullable=True)
    attributes = db.Column(db.String, nullable=True)
    
    # relationships
    creator = db.relationship(
        'User',
        backref=db.backref('created_activities', order_by='desc(Activity.created)'),
        foreign_keys=[creator_id],
    )

    def __str__(self):
        return self.id

    @classmethod
    def new(cls, data, policy, current_user):
        # 
        # create instance using data
        #

        instance = cls(
            policy_number=policy.number,
            effective_date=datetime.strptime(policy.effective_date, date_format).date(),
            type=data['activity'].get('name'),
            creator_id=current_user.id,
            attributes=json.dumps(data['activity'].get('fields'))
        )
        
        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    @classmethod
    def read_policy(cls, policy_number, effective_date, current_user):
        #
        # create instance of reading a policy
        #

        instance = cls(
            policy_number=policy_number,
            effective_date=datetime.strptime(effective_date, date_format).date(),
            type='Read Policy',
            creator=current_user,
            finished=datetime.utcnow(),
            status='OK',
        )

        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    def finish(self, status):
        #
        # sets is_finished to True 
        #
        self.status = status
        self.finished = datetime.utcnow()
        db.session.commit()


#
# Gamification Models
#
class GamificationEvent(db.Model):
    __tablename__ = 'gamification_events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(32), unique=True, nullable=False)

    def __str__(self):
        return self.name


class GamificationActivity(db.Model):
    __tablename__ = 'gamification_activities'
    id = db.Column(db.Integer, primary_key=True)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    processed = db.Column(db.DateTime, nullable=True)
    is_processed = db.Column(db.Boolean, nullable=False, default=False)
    event_details = db.Column(db.String(1024), nullable=True)
    event_id = db.Column(db.Integer, db.ForeignKey('gamification_events.id'), nullable=False)
    user_id = db.Column(db.String(56), db.ForeignKey('users.id'), nullable=False)
    company_id = db.Column(db.String(56), db.ForeignKey('companies.id'), nullable=False)

    # relationships
    event = db.relationship('GamificationEvent', foreign_keys=[event_id])
    user = db.relationship('User', backref='gamification_activities', foreign_keys=[user_id])
    company = db.relationship('Company', backref='gamification_activities', foreign_keys=[company_id])

    def __str__(self):
        msg = f'{self.user.email}: {self.event.name}'
        if self.processed:
            return f'{msg} - processed at {self.processed.strftime("%d.%m.%Y, %H:%M:%S")}'
        else:
            return f'{msg} - NOT processed'

    @classmethod
    def new(cls, user, event, event_details):
        # 
        # create instance based on the provided data
        #

        if not isinstance(event, GamificationEvent):
            if isinstance(event, int):
                event = db.session.query(GamificationEvent).filter_by(id=event).first()
            elif isinstance(event, str):
                event = db.session.query(GamificationEvent).filter_by(name=event).first()

        print(f"new GamificationActivity. user.id = {user.id}, event = {event.name}, event_details = {event_details}")

        instance = cls(
            user_id=user.id,
            company_id=user.company.company_id,
            event=event,
            event_details=event_details,
        )
        
        # store to db
        db.session.add(instance)
        db.session.commit()
        
        return instance

    def set_processed(self):
        #
        # set activity as processed
        #

        self.processed = datetime.utcnow()
        self.is_processed = True

        # save to db
        db.session.commit()
