# stdlib
from collections import deque
import re
from typing import Deque, Dict, List, Optional
# libs
import bcrypt
from cloudcix.api.membership import Membership
from cloudcix_rest.controllers import ControllerBase
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator, validate_email
# local
from contact.models import Contact


__all__ = [
    'ContactListController',
    'ContactCreateController',
    'ContactUpdateController',
]

PHONE_PATTERN = re.compile(r'^(\(?\+?[0-9]*\)?)?[0-9_\- ()]*$')


class ContactListController(ControllerBase):
    """
    Validates User data used to list Contact records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'surname',
            'company_name',
            'created',
            'email',
            'first_name',
            'id',
            'updated',
        )
        search_fields = {
            'address': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'address2': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'campaigncontact__responded': (),
            'campaigns': ('in', 'isnull'),
            'chatbot_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'city': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'company_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'country_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'currently_visiting': (),
            'created': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'email': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'first_name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'groups': ('in', 'isnull'),
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'opportunities': ('in', 'isnull'),
            'opt_out': (),
            'phone_number': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'postcode': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'subdivision_id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'surname': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'updated': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
            'website': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
        }


class ContactCreateController(ControllerBase):
    """
    Validates user data used to create Contact records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Contact
        validation_order = (
            'address',
            'address2',
            'city',
            'company_name',
            'country_id',
            'currently_visiting',
            'member_id',
            'email',
            'first_name',
            'linkedin_url',
            'notes',
            'password',
            'phone_number',
            'postcode',
            'subdivision_id',
            'surname',
            'title',
            'website',
        )

    def validate_address(self, address: Optional[str]) -> Optional[str]:
        """
        description: The first line of the geographic address of the Contact
        required: false
        type: string
        """
        if address is None:
            return None
        address = str(address).strip()
        if len(address) > self.get_field('address').max_length:
            return 'contact_contact_create_101'
        self.cleaned_data['address'] = address
        return None

    def validate_address2(self, address2: Optional[str]) -> Optional[str]:
        """
        description: The second line of the geographic address of the Contact
        required: false
        type: string
        """
        if address2 is None:
            return None
        address2 = str(address2).strip()
        if len(address2) > self.get_field('address2').max_length:
            return 'contact_contact_create_102'
        self.cleaned_data['address2'] = address2
        return None

    def validate_city(self, city: Optional[str]) -> Optional[str]:
        """
        description: The city in which the address of the Contact is located
        required: false
        type: string
        """
        if city is None:
            return None
        city = str(city).strip()
        if len(city) > self.get_field('city').max_length:
            return 'contact_contact_create_103'
        self.cleaned_data['city'] = city
        return None

    def validate_company_name(self, company_name: Optional[str]) -> Optional[str]:
        """
        description: The name of the company where the Contact is employed
        required: false
        type: string
        """
        if company_name is None:
            return None
        company_name = str(company_name).strip()
        if len(company_name) > self.get_field('company_name').max_length:
            return 'contact_contact_create_104'
        self.cleaned_data['company_name'] = company_name
        return None

    def validate_country_id(self, country_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Country of the Contacts geographic address
        required: false
        type: integer
        """
        if not country_id:
            return None
        try:
            country_id = int(country_id)
        except (TypeError, ValueError):
            return 'contact_contact_create_105'
        response = Membership.country.read(token=self.request.user.token, pk=country_id, span=self.span)
        if response.status_code != 200:
            # Request was not successful
            return 'contact_contact_create_106'
        self.cleaned_data['country_id'] = country_id
        return None

    def validate_currently_visiting(self, currently_visiting: Optional[bool]) -> Optional[str]:
        """
        description: Flag denoting if the Contact is currently visiting the Member
        type: boolean
        required: false
        """
        if currently_visiting is None:
            currently_visiting = False
        if not isinstance(currently_visiting, bool):
            return 'contact_contact_create_107'
        self.cleaned_data['currently_visiting'] = currently_visiting
        return None

    def validate_member_id(self, member_id: Optional[int]) -> Optional[str]:
        """
        description: The member_id the Contact is created in.
        required: false
        type: int
        """
        if not member_id:
            member_id = int(self.request.user.member['id'])

        if member_id != self.request.user.member['id']:
            response = Membership.member.read(token=self.request.user.token, pk=member_id, span=self.span)
            if response.status_code != 200:
                # Request was not successful
                return 'contact_contact_create_108'
        self.cleaned_data['member_id'] = member_id
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: The email address of the Contact
        required: false
        type: string
        """
        if not email:
            return None
        email = str(email.lower()).strip()
        if len(email) > self.get_field('email').max_length:
            return 'contact_contact_create_109'
        try:
            validate_email(email)
        except ValidationError:
            return 'contact_contact_create_110'
        if 'member_id' not in self.cleaned_data:
            # An error was raised and we cannot proceed with validation
            return None
        if Contact.objects.filter(email=email, member_id=self.cleaned_data['member_id']).exists():
            return 'contact_contact_create_111'
        self.cleaned_data['email'] = email
        return None

    def validate_first_name(self, first_name: Optional[str]) -> Optional[str]:
        """
        description: The first name of the Contact
        type: string
        """
        if first_name is None:
            first_name = ''
        first_name = str(first_name).strip()
        if len(first_name) == 0:
            return 'contact_contact_create_112'
        if len(first_name) > self.get_field('first_name').max_length:
            return 'contact_contact_create_113'
        self.cleaned_data['first_name'] = first_name
        return None

    def validate_linkedin_url(self, linkedin_url: Optional[str]) -> Optional[str]:
        """
        description: URL to the LinkedIn profile of the Contact
        required: false
        type: string
        """
        if not linkedin_url:
            return None
        linkedin_url = str(linkedin_url).strip()
        if len(linkedin_url) > self.get_field('linkedin_url').max_length:
            return 'contact_contact_create_114'
        try:
            validator = URLValidator()
            validator(linkedin_url)
        except ValidationError:
            return 'contact_contact_create_115'
        self.cleaned_data['linkedin_url'] = linkedin_url
        return None

    def validate_notes(self, notes: Optional[str]) -> Optional[str]:
        """
        description: Notes on the Contact
        type: string
        required: false
        """
        self.cleaned_data['notes'] = str(notes).strip() if notes else ''
        return None

    def validate_password(self, password: Optional[str]) -> Optional[str]:
        """
        description: Password for the contact required for Chatbot Services
        required: false
        type: string
        """
        if not password:
            return None
        password = str(password).strip()
        if re.match(Contact.PASSWORD_REGEX, password) is None:
            # Not a match
            return 'contact_contact_create_116'
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.cleaned_data['salt'] = salt
        self.cleaned_data['hashed_pwd'] = hashed_pwd

        return None

    def validate_phone_number(self, phone_number: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers used by the Contact
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        type: array
        """
        phone_number = phone_number or []
        if not isinstance(phone_number, list):
            return 'contact_contact_create_117'
        numbers: Deque = deque()
        for i, phone in enumerate(phone_number):
            if not isinstance(phone, dict):
                return 'contact_contact_create_118'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'contact_contact_create_119'
            if not PHONE_PATTERN.match(number):
                return 'contact_contact_create_120'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phone_number'] = list(numbers)
        return None

    def validate_postcode(self, postcode: Optional[str]) -> Optional[str]:
        """
        description: The postcode of the geographical address of the Contact
        required: false
        type: string
        """
        if postcode is None:
            return None
        postcode = str(postcode).strip()
        if len(postcode) > self.get_field('postcode').max_length:
            return 'contact_contact_create_121'
        self.cleaned_data['postcode'] = postcode
        return None

    def validate_subdivision_id(self, subdivision_id: Optional[int]) -> Optional[str]:
        """
        description:  The ID of the Subdivision in the Country of the Contacts geographic address
        required: false
        type: integer
        """
        if not subdivision_id or 'country_id' not in self.cleaned_data:
            return None
        try:
            subdivision_id = int(subdivision_id)
        except (TypeError, ValueError):
            return 'contact_contact_create_122'
        response = Membership.subdivision.read(
            token=self.request.user.token,
            country_id=self.cleaned_data['country_id'],
            pk=subdivision_id,
        )
        if response.status_code != 200:
            return 'contact_contact_create_123'
        self.cleaned_data['subdivision_id'] = subdivision_id
        return None

    def validate_surname(self, surname: Optional[str]) -> Optional[str]:
        """
        description: The surname of the Contact
        type: string
        """
        if surname is None:
            surname = ''
        surname = str(surname).strip()
        if len(surname) == 0:
            return 'contact_contact_create_124'
        if len(surname) > self.get_field('surname').max_length:
            return 'contact_contact_create_125'
        self.cleaned_data['surname'] = surname
        return None

    def validate_title(self, title: Optional[str]) -> Optional[str]:
        """
        description: The professional title of the Contact
        required: false
        type: string
        """
        if title is None:
            return None
        title = str(title).strip()
        if len(title) > self.get_field('title').max_length:
            return 'contact_contact_create_126'
        self.cleaned_data['title'] = title
        return None

    def validate_website(self, website: Optional[str]) -> Optional[str]:
        """
        description: A website link of the Contact
        required: false
        type: string
        """
        if not website:
            return None
        website = str(website).strip()
        if len(website) > self.get_field('website').max_length:
            return 'contact_contact_create_127'
        try:
            validator = URLValidator()
            validator(website)
        except ValidationError:
            return 'contact_contact_create_128'
        self.cleaned_data['website'] = website
        return None


class ContactUpdateController(ControllerBase):
    """
    Validates User data used to update a Contact
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Contact
        validation_order = (
            'address',
            'address2',
            'city',
            'company_name',
            'country_id',
            'currently_visiting',
            'email',
            'first_name',
            'linkedin_url',
            'notes',
            'opt_notes',
            'opt_out',
            'password',
            'phone_number',
            'postcode',
            'subdivision_id',
            'surname',
            'title',
            'website',
        )

    def validate_address(self, address: Optional[str]) -> Optional[str]:
        """
        description: The first line of the geographic address of the Contact
        required: false
        type: string
        """
        if address is None:
            return None
        address = str(address).strip()
        if len(address) > self.get_field('address').max_length:
            return 'contact_contact_update_101'
        self.cleaned_data['address'] = address
        return None

    def validate_address2(self, address2: Optional[str]) -> Optional[str]:
        """
        description: The second line of the geographic address of the Contact
        required: false
        type: string
        """
        if address2 is None:
            return None
        address2 = str(address2).strip()
        if len(address2) > self.get_field('address2').max_length:
            return 'contact_contact_update_102'
        self.cleaned_data['address2'] = address2
        return None

    def validate_city(self, city: Optional[str]) -> Optional[str]:
        """
        description: The city in which the address of the Contact is located
        required: false
        type: string
        """
        if city is None:
            return None
        city = str(city).strip()
        if len(city) > self.get_field('city').max_length:
            return 'contact_contact_update_103'
        self.cleaned_data['city'] = city
        return None

    def validate_company_name(self, company_name: Optional[str]) -> Optional[str]:
        """
        description: The name of the company where the Contact is employed
        required: false
        type: string
        """
        if company_name is None:
            return None
        company_name = str(company_name).strip()
        if len(company_name) > self.get_field('company_name').max_length:
            return 'contact_contact_update_104'
        self.cleaned_data['company_name'] = company_name
        return None

    def validate_country_id(self, country_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Country of the Contacts geographic address
        required: false
        type: integer
        """
        if not country_id:
            return None
        try:
            country_id = int(country_id)
        except (TypeError, ValueError):
            return 'contact_contact_update_105'
        response = Membership.country.read(token=self.request.user.token, pk=country_id, span=self.span)
        if response.status_code != 200:
            # Request was not successful
            return 'contact_contact_update_106'
        self.cleaned_data['country_id'] = country_id
        return None

    def validate_currently_visiting(self, currently_visiting: Optional[bool]) -> Optional[str]:
        """
        description: Flag denoting if the Contact is currently visiting the Member
        type: boolean
        required: false
        """
        if currently_visiting is None:
            currently_visiting = False
        if not isinstance(currently_visiting, bool):
            return 'contact_contact_update_107'
        self.cleaned_data['currently_visiting'] = currently_visiting
        return None

    def validate_email(self, email: Optional[str]) -> Optional[str]:
        """
        description: The email address of the Contact
        required: false
        type: string
        """
        if not email:
            return None
        email = str(email.lower()).strip()
        if len(email) > self.get_field('email').max_length:
            return 'contact_contact_update_108'
        try:
            validate_email(email)
        except ValidationError:
            return 'contact_contact_update_109'

        if Contact.objects.filter(
            email=email,
            member_id=self._instance.member_id,
        ).exclude(pk=self._instance.pk).exists():
            return 'contact_contact_update_110'

        self.cleaned_data['email'] = email
        return None

    def validate_first_name(self, first_name: Optional[str]) -> Optional[str]:
        """
        description: The first name of the Contact
        type: string
        """
        if first_name is None:
            first_name = ''
        first_name = str(first_name).strip()
        if len(first_name) == 0:
            return 'contact_contact_update_111'
        if len(first_name) > self.get_field('first_name').max_length:
            return 'contact_contact_update_112'
        self.cleaned_data['first_name'] = first_name
        return None

    def validate_linkedin_url(self, linkedin_url: Optional[str]) -> Optional[str]:
        """
        description: URL to the LinkedIn profile of the Contact
        required: false
        type: string
        """
        if not linkedin_url:
            return None
        linkedin_url = str(linkedin_url).strip()
        if len(linkedin_url) > self.get_field('linkedin_url').max_length:
            return 'contact_contact_update_113'
        try:
            validator = URLValidator()
            validator(linkedin_url)
        except ValidationError:
            return 'contact_contact_update_114'
        self.cleaned_data['linkedin_url'] = linkedin_url
        return None

    def validate_notes(self, notes: Optional[str]) -> Optional[str]:
        """
        description: Notes on the Contact
        type: string
        required: false
        """
        self.cleaned_data['notes'] = str(notes).strip() if notes else ''
        return None

    def validate_opt_notes(self, opt_notes: Optional[str]) -> Optional[str]:
        """
        description: Notes on the Contact recording if the opt in or out of communications from the Member
        type: string
        required: false
        """
        self.cleaned_data['opt_notes'] = str(opt_notes).strip() if opt_notes else ''
        return None

    def validate_opt_out(self, opt_out: Optional[bool]) -> Optional[str]:
        """
        description: Flag denoting if the Contact has opted out of communication from the Member
        type: boolean
        required: false
        """
        if opt_out is None:
            opt_out = False
        if not isinstance(opt_out, bool):
            return 'contact_contact_update_115'
        self.cleaned_data['opt_out'] = opt_out
        return None

    def validate_password(self, password: Optional[str]) -> Optional[str]:
        """
        description: Password for the contact required for Chatbot Services
        required: false
        type: string
        """
        if not password:
            return None
        password = str(password).strip()
        if re.match(Contact.PASSWORD_REGEX, password) is None:
            # Not a match
            return 'contact_contact_update_116'
        salt = bcrypt.gensalt()
        hashed_pwd = bcrypt.hashpw(password.encode('utf-8'), salt)
        self.cleaned_data['salt'] = salt
        self.cleaned_data['hashed_pwd'] = hashed_pwd

        return None

    def validate_phone_number(self, phone_number: Optional[List[Dict[str, str]]]) -> Optional[str]:
        """
        description: An array of named phone numbers used by the Contact
        items:
            type: object
            properties:
                name:
                    type: string
                number:
                    type: string
        required: false
        type: array
        """
        phone_number = phone_number or []
        if not isinstance(phone_number, list):
            return 'contact_contact_update_117'
        numbers: Deque = deque()
        for i, phone in enumerate(phone_number):
            if not isinstance(phone, dict):
                return 'contact_contact_update_118'
            name = phone.get('name', None)
            number = phone.get('number', None)
            if name is None or number is None:
                return 'contact_contact_update_119'
            if not PHONE_PATTERN.match(number):
                return 'contact_contact_update_120'
            key = {'name': name.strip(), 'number': number.strip()}
            if key not in numbers:
                numbers.append(key)
        self.cleaned_data['phone_number'] = list(numbers)
        return None

    def validate_postcode(self, postcode: Optional[str]) -> Optional[str]:
        """
        description: The postcode of the geographical address of the Contact
        required: false
        type: string
        """
        if postcode is None:
            return None
        postcode = str(postcode).strip()
        if len(postcode) > self.get_field('postcode').max_length:
            return 'contact_contact_update_121'
        self.cleaned_data['postcode'] = postcode
        return None

    def validate_subdivision_id(self, subdivision_id: Optional[int]) -> Optional[str]:
        """
        description: The ID of the Subdivision in the Country of the Contacts geographic address
        required: false
        type: integer
        """
        if not subdivision_id or 'country_id' not in self.cleaned_data:
            return None
        try:
            subdivision_id = int(subdivision_id)
        except (TypeError, ValueError):
            return 'contact_contact_update_122'
        response = Membership.subdivision.read(
            token=self.request.user.token,
            country_id=self.cleaned_data['country_id'],
            pk=subdivision_id,
        )
        if response.status_code != 200:
            return 'contact_contact_update_123'
        self.cleaned_data['subdivision_id'] = subdivision_id
        return None

    def validate_surname(self, surname: Optional[str]) -> Optional[str]:
        """
        description: The surname of the Contact
        type: string
        """
        if surname is None:
            surname = ''
        surname = str(surname).strip()
        if len(surname) == 0:
            return 'contact_contact_update_124'
        if len(surname) > self.get_field('surname').max_length:
            return 'contact_contact_update_125'
        self.cleaned_data['surname'] = surname
        return None

    def validate_title(self, title: Optional[str]) -> Optional[str]:
        """
        description: The professional title of the Contact
        required: false
        type: string
        """
        if title is None:
            return None
        title = str(title).strip()
        if len(title) > self.get_field('title').max_length:
            return 'contact_contact_update_126'
        self.cleaned_data['title'] = title
        return None

    def validate_website(self, website: Optional[str]) -> Optional[str]:
        """
        description: A website link of the Contact
        required: false
        type: string
        """
        if not website:
            return None
        website = str(website).strip()
        if len(website) > self.get_field('website').max_length:
            return 'contact_contact_update_127'
        try:
            validator = URLValidator()
            validator(website)
        except ValidationError:
            return 'contact_contact_update_128'
        self.cleaned_data['website'] = website
        return None
