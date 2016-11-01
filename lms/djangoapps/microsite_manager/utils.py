
from collections import namedtuple
import logging

from django.contrib.sites.models import Site

from microsite_configuration.models import (
    Microsite,
    MicrositeOrganizationMapping,
    )
from organizations import api as orgsApi


log = logging.getLogger(__name__)

HrefLabel = namedtuple('HrefLabel', ['href', 'label'])

# Microsite value object. Primary use in templates
# the url members are intended for the HrefLabel above
MicrositeVO = namedtuple('MicrositeVO', ['home_url', 'management_url', 'microsite'])


def generate_microsite_vo(microsite, port=None):
    """
    Create a namedtuple of data to show in the UI

    We build our urls here to keep the view and template simpler

    Massage microsites to get the urls we want
    Use protocol relative URL

    Perhaps another option is creating custom template filters
    https://docs.djangoproject.com/en/1.8/howto/custom-template-tags/
    """
    port_str = ':{}'.format(port) if port else ''
    return MicrositeVO(
        home_url=HrefLabel(
            href='//{}{}'.format(microsite.site.domain, port_str),
            label=microsite.site),
        management_url=HrefLabel(
            href='//{}{}/hr-management/'.format(microsite.site.domain, port_str),
            label='manage'),
        microsite=microsite
    )

def create_microsite(**kwargs):
    """
    Creates a Microsite object and related objects as needed

    :param subdomain_name: Subdomain name: 
    :param domain: Fully qualified domain name
    :param org_long_name: Organization name. May contain spaces
    :paran org_short_name:  Organization short name, no spaces or special chars
      besides hyphens and underscores. Basically needs to be sluggable
    :param org_description:  optional

    :rtype: Microsite object


    TODO: Add data checking/validation (like missing essential values)
    """
    log.info("create_microsite kwargs = {}".format(kwargs))

    subdomain_name = kwargs.get('subdomain_name')
    if subdomain_name:
        subdomain_name = subdomain_name.lower()
    else:
        raise "Missing subdomain name"

    domain = kwargs.get('domain')
    if not domain:
        raise "Missing domain name"

    org_long_name = kwargs.get('org_long_name')
    if not org_long_name:
        raise "Missing organization long name"

    org_short_name = kwargs.get('org_short_name')
    if not org_short_name:
        raise "Missing org short name"

    org_description = kwargs.get('org_description')
    # first check if microsite exists
    microsites = Microsite.objects.filter(key=subdomain_name)
    if microsites:
        return microsites[0]

    subdomain_full_hostname = "{}.{}".format(subdomain_name, domain)

    try:
        organization = orgsApi.get_organization_by_short_name(org_short_name)
        # TODO: Additional validation - Also check org by long name
    except:
        organization = None

    if not organization:
        organization = orgsApi.add_organization({
            'name': org_long_name,
            'short_name': org_short_name,
            'description': org_description,
            });

    sites = Site.objects.filter(domain=subdomain_full_hostname)
    if sites:
        site = sites[0]
    else:
        site = Site(domain=subdomain_full_hostname, name=subdomain_name)
        site.save()

    # We're just being consistent with NYIF's existing microsite for this one
    platform_name = subdomain_name.upper()   

    microsite = Microsite(
        key=subdomain_name.lower(),
        values={
            'PLATFORM_NAME': platform_name,
            'platform_name': platform_name
        },
        site=site)
    microsite.save()
    morg = MicrositeOrganizationMapping(microsite=microsite,
        organization=org_short_name)
    morg.save()
    
    return microsite

def delete_microsite(microsite):
    '''
    Deletes the given microsite and mapping to organization
    :param Microsite microsite: The microsite to delete
    :return: True if microsite deleted False if not

    TODO: Consider passing the microsite name (key is the field name) to this
    method and move the code in the `Command` handle method to here
    And add testing
    TODO: Add flag to delete org and/or site
    '''

    if not microsite:
        return False
    else:
        # Get the mapping
        mapping_qs = MicrositeOrganizationMapping.objects.filter(
            microsite=microsite.id)
        if mapping_qs.count() == 1:
            mapping_qs[0].delete()
        else:
            # found none or more than one (bad state for the lastter)
            return False

        microsite.delete()
        # at this point just assuming we've deleted it
        # TODO: Add exception handling for delete failure?
        return True
