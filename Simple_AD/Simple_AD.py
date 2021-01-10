from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES

class Simple_AD:
    """ 
    A simple wrapper for ldap3 in an Active Directory Environment.

    Examples:

        0. Initilaize a connection
        sad = Simple_AD(server_name="server1.mydomain.com", username="mydomain.com\\jsmith", password="myawesomepassword")

        1. Get group(s) by samaccountname
        groups = sad.get_adgroup(samaccountname="Accounting")

        2. Get users from a group fast
        users_from_group = sad.expand_users_from_group(groups[0])

        3. Get a user by samaccountname
        user = sad.get_aduser(samaccountname="jsmith")
    """

    def __init__(self, server_name, username, password, use_ssl=True, default_attributes=ALL_ATTRIBUTES):
        """
        Class initilizer. Takes various ldap3 properties and passess them through

        Args:
            server_name (string):           The name of the target ldap server
            username (string):              Username to authenticate in the format: {domain_name\\user_name}. Ex: [contoso\\jsmith]
            password (string):              Password of the user
            use_ssl (bool, optional):       Binds to SSL on port 636 and should be used when possible. Defaults to True.
            default_attributes:             Sets the default attributes to get for an object during an LDAP query, optional.  Defaults to ALL_ATTRIBUTES.
                Can be set to:
                    ALL_OPERATIONAL_ATTRIBUTES - ldap3 operation attributes wrapper
                    [] - No attributes by default
                    ["member","lastLogonDate"] - Custom attributes
        """

        self.server = Server(server_name, use_ssl=use_ssl, get_info=ALL)
        self.conn = Connection(self.server, auto_bind=True, user=username, password=password, authentication=NTLM)
        self.base_ou = self.server.info.naming_contexts[0]
        self.default_attributes = default_attributes

    def get_adgroup(self, samaccountname="*", distinguishedname="*", attributes=False):
        """
        Get an AD Group Object from a filter. 
        Can return multiple results using a wildcard '*'

        Args:
            samaccountname (str, optional):     LDAP Property samaccountname. Defaults to "*".
            distinguishedname (str, optional):  LDAP Property distinguishedname.. Defaults to "*".
            attributes (bool, optional):        Custom attributes if not using defaults. Defaults to False.

        Returns:
            object: ldap3 attribute object of the group(s)
        """

        if(attributes == False):
            attributes = self.default_attributes

        self.conn.search(
            search_base=self.base_ou,
            search_filter=f'(&(objectCategory=group)(samaccountname={samaccountname})(distinguishedname={distinguishedname}))',
            search_scope='SUBTREE',
            attributes = attributes
        )

        return self.conn.entries

    def get_aduser(self, samaccountname="*", distinguishedname="*", attributes=False):
        """
        Get an AD User Object from a filter. 
        Can return multiple results using a wildcard '*'

        Args:
            samaccountname (str, optional):         LDAP Property samaccountname. Defaults to "*".
            distinguishedname (str, optional):      LDAP Property distinguishedname.. Defaults to "*".
            attributes (bool, optional):            Custom attributes if not using defaults. Defaults to False.

        Returns:
            object: ldap3 attribute object of the user(s)
        """

        if(attributes == False):
            attributes = self.default_attributes

        self.conn.search(
            search_base=self.base_ou,
            search_filter=f'(&(objectCategory=user)(samaccountname={samaccountname})(distinguishedname={distinguishedname}))',
            search_scope='SUBTREE',
            attributes = attributes
        )
        return self.conn.entries

    def expand_users_from_group(self, group, attributes=False):
        """
        A handy function to quickly expand user attributes from a group object with the [member] attribute populated.
        This is useful when you need to get additional attributes from a users in a group, but don't want to look them up for each.
        This builds a single LDAP query for all users

        Args:
            group (group object):           Group object with the [member] attribute populated
            attributes (bool, optional):    Custom attributes if not using defaults. Defaults to False.

        Raises:
            Exception: If [member] is not populated on the [group] argument, exception will be raised.

        Returns:
            object: List of AD users with their requested attributes

        Examples:
            1. Expand members from the group "Accounting"
                sad = Simple_AD(server_name="server1.mydomain.com", username="mydomain.com\\jsmith", password="myawesomepassword")
                groups = sad.get_adgroup(samaccountname="Accounting")
                users_from_group = sad.expand_users_from_group(groups[0])
        """

        if not hasattr(group, 'member'):
            raise Exception("Group must have attribute [member] populated.")

        #Validate attributes to get
        if(attributes == False):
            attributes = self.default_attributes

        #Build fast query in format: (|(distinguishedname=dn1)(distinguishedname=dn2)(...))
        members_ldap_query = ""
        for distinguishedname in group.member:
            members_ldap_query += f"(distinguishedname={distinguishedname})"
        members_ldap_query = "(|" + members_ldap_query + ")"
                
        #Get the users
        self.conn.search(
            search_base=self.base_ou,
            search_filter=members_ldap_query,
            search_scope='SUBTREE',
            attributes = attributes
        )

        #Return results
        return self.conn.entries