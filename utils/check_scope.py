from .get_domain_name import get_domain_name
import fnmatch

def matches_wildcard(domain, wildcard):
    # Convert domain and wildcard to lowercase
    domain = domain.lower()
    wildcard = wildcard.lower()
    
    # Use fnmatch to handle wildcard patterns
    return fnmatch.fnmatch(domain, wildcard)


def is_in_scope(subdomain_name, scopes, ooscopes):
    domain_name = get_domain_name(subdomain_name).lower()
    
    # Check if domain matches any out-of-scope patterns
    for ooscape in ooscopes:
        if matches_wildcard(subdomain_name, ooscape):
            return False
    
    # Check if domain is in scope
    if domain_name in scopes:
        return True

    return False
