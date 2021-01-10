# Python_Simple_AD
A simple Active Directory Python module to reduce boilerplate and increase productivity.

# Requirements
```
pip3 install ldap3
pip3 install simple_ad
```

# Sample Usage
```
from simple_ad import Simple_AD

server="yourserver.local"
username="yourdomain.local\\jsmith"
password = "yourawesomepassword"

sad = Simple_AD(server_name=server, username=username, password=password)

groups = sad.get_adgroup(samaccountname="Accounting*")
users_from_group = sad.expand_users_from_group(groups[0])

users1 = sad.get_aduser(samaccountname="jsmith")
users2 = sad.get_aduser(distinguishedname="CN=John Smith,OU=Accounting,DC=youdomain,DC=com")
```