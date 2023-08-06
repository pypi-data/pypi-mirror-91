# SimpleTelnetMail

## Requirements
This package require : 
 - python3
 - python3 Standard Library

## Installation
```bash
pip install SimpleTelnetMail 
```

## Description 
Send simples emails with Telnet.

## Examples

### Simple usage

#### Command line
```bash
SimpleTelnetMail --host="smtp.server.com" --from="my.address@domain.com" --to="receiver@domain.com" --message="Secret and not secure email with Telnet."
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver@domain.com" -m "Secret and not secure email with Telnet." --username="my.address@domain.com" --password="password"
```

#### Python
```python
from SimpleTelnetMail import TelnetMail

client = TelnetMail("my.server.com", from_ = "my.address@domain.com", to = ["receiver@domain.com"], message = "Secret and secure email with Telnet.")
client.send_mail()

client = TelnetMail("my.server.com", from_ = "my.address@domain.com", to = ["receiver@domain.com"], message = "Secret and secure email with Telnet.", username="my.address@domain.com", password="password")
client.send_mail()
```

### Advanced usage

#### Command line
Don't forgot to use `--ssl` or `-s` option to secure your email with **SSL**/**TLS**.
1. Without authentication, with custom headers, to several recipients:
```bash
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver1@domain.com,receiver2@domain.com" -m "Secret and secure email with Telnet." --port=587 --pseudo="Me" --debug=4 --ssl --ehlo="MYPC" Date="Sat, 19 Dec 2020 01:02:03 -0000" Subject="Secret Email" MIME_Version="1.0", Encrypted="ROT13", Fake="Fake hearder", Sender="PSEUDO <my.address@domain.com>", Comments="My comment", Keywords="Email, Secret", Expires="Sat, 25 Dec 2021 05:35:23 -0000", Language="en-EN, it-IT", Importance="hight", Priority="urgent", Sensibility="Company-Confidential", From="PSEUDO <my.address@domain.com>", To="receiver1@domain.com,receiver2@domain.com", Content_Type="text/plain; charset=us-ascii", Content_Transfer_Encoding="quoted-printable"
```

2. With authentication
```bash
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver@domain.com" -m "Secret and secure email with Telnet." -U "my.address@domain.com" -W "password" --port=587 --pseudo="Me" --debug=4 --ssl --ehlo="MYPC"
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver@domain.com" -m "Secret and secure email with Telnet." -U "my.address@domain.com" -W "password" -p 587 -P "Me" -d 4 -s -e "MYPC" Subject="Hello" MIME_Version="1.0" Content_Transfer_Encoding="quoted-printable" Content_Type="text/plain; charset=us-ascii"
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver@domain.com" -m "Secret and secure email with Telnet." -U "my.address@domain.com" -W "password" -p 587 -P "Me" -d 4 -s -e "MYPC" Subject="Hello" MIME_Version="1.0" Content_Transfer_Encoding="7bit" Content_Type="text/plain; charset=utf-8"
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver@domain.com" -m "U2VjcmV0IGFuZCBzZWN1cmUgZW1haWwgd2l0aCBUZWxuZXQu" -U "my.address@domain.com" -W "password" -p 587 -P "Me" -d 4 -s -e "MYPC" Subject="Hello" MIME_Version="1.0" Content_Transfer_Encoding="base64" Content_Type="text/plain; charset=utf-8"
SimpleTelnetMail -H "smtp.server.com" -f "my.address@domain.com" -t "receiver1@domain.com,receiver2@domain.com" -m "PHA+U2VjcmV0IGFuZCBzZWN1cmUgZW1haWwgd2l0aCBUZWxuZXQuPC9wPg==" -U "my.address@domain.com" -W "password" -p 587 -P "Me" -d 4 -s -e "MYPC" Subject="Hello" MIME_Version="1.0" Content_Transfer_Encoding="base64" Content_Type="text/html; charset=utf-8"
```

#### Python
1. Without authentication, with custom headers, to several recipients:
```python
from SimpleTelnetMail import TelnetMail

client = TelnetMail("my.server.com", port= 87, from_="my.address@domain.com", to=["receiver1@domain.com", "receiver2@domain.com"], message="Secret and secure email with Telnet.", ehlo="MYPC", pseudo="Me", ssl=True, debug=4, Subject="Secret Email", Date="Sat, 19 Dec 2020 01:02:03 -0000", MIME_Version="1.0", Encrypted="ROT13", Fake="Fake hearder", Sender="PSEUDO <my.address@domain.com>", Comments="My comment", Keywords="Email, Secret", Expires="Sat, 25 Dec 2021 05:35:23 -0000", Language="en-EN, it-IT", Importance="hight", Priority="urgent", Sensibility="Company-Confidential", From="PSEUDO <my.address@domain.com>", To="receiver1@domain.com,receiver2@domain.com", Content_Type="text/plain; charset=us-ascii", Content_Transfer_Encoding="quoted-printable")
client.send_mail()

print(repr(client))
print(client)
print(client.responses.decode())
```

2. With authentication
```python
from SimpleTelnetMail import TelnetMail

client = TelnetMail("my.server.com", port=587, from_="my.address@domain.com", to=["receiver@domain.com"], message="Secret and secure email with Telnet.", ehlo="MYPC", pseudo="Me", ssl=True, debug=4, username="my.address@domain.com", password="password")
client.send_mail()

print(repr(client))
print(client)
print(client.responses.decode())

client = TelnetMail("my.server.com", port=587, from_="my.address@domain.com", to=["receiver@domain.com"], message="Secret and secure email with Telnet.", ehlo="MYPC", pseudo="Me", ssl=True, debug=4, username="my.address@domain.com", password="password", Subject="Hello", MIME_Version="1.0", Content_Transfer_Encoding="quoted-printable", Content_Type="text/plain; charset=us-ascii")
client.send_mail()

client = TelnetMail("my.server.com", port=587, from_="my.address@domain.com", to=["receiver@domain.com"], message="PHA+U2VjcmV0IGFuZCBzZWN1cmUgZW1haWwgd2l0aCBUZWxuZXQuPC9wPg==", ehlo="MYPC", pseudo="Me", ssl=True, debug=4, username="my.address@domain.com", password="password", Subject="Hello", MIME_Version="1.0", Content_Transfer_Encoding="base64", Content_Type="text/html; charset=utf-8")
client.send_mail()
```

## Link
[Github Page](https://github.com/mauricelambert/SimpleTelnetMail)

## Licence
Licensed under the [GPL, version 3](https://www.gnu.org/licenses/).