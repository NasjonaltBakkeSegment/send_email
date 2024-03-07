# send_email

Repository for sending emails from the NBS user account. This repository can be included as a submodule into other repositories.

`git submodule add git@gitlab.met.no:met/fou/fd/nbs/send_email.git`

The `send_email.py` function can then be imported into the parent repository and run.

```
from send_email import send_email

send_email(recipient, subject, message, send_from='nbs-helpdesk@met.no', server="127.0.0.1")
```
