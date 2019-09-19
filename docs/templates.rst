#########
Templates
#########

The ``django-simple-email-auth`` package ships with a few default email
templates right out of the box. These templates, while functional, should most
likely be overridden for the best user experience. By overriding the templates
used you can use the full power of Django's templating system to inject headers
and footers with information about your project or simply reword the messages.

We use `django-email-utils`_ to send emails which allows for using Django's
templating system to send both HTML and plain text emails. For each template,
you may provide a ``.txt`` file and/or a ``.html`` file. When sending, both
extensions will be searched for, and the email will be sent with all the
available content types.

**********************
Already Verified Email
**********************

Sent when a user requests a verification email for an email address that has
already been verified. The suggested actions for the user are to log in or to
reset their password.

Template Path
  :file:`email_auth/emails/already-verified`

Provided Context
  ``email``
    ``EmailAddress`` instance that has already been verified.

****************************
Duplicate Email Registration
****************************

Sent when a user attempts to register an email address that already exists in
the system. This attempt can come from a user registering for the first time or
from a user adding an additional email address to their account. This does not
imply that the email address has been verified yet. The suggested actions for
the user are:

* If this wasn't something they did, ignore the email.
* Log in since they have already verified ownership of this email address.
* Reset their password if they have forgotten it.

Template Path
  :file:`email_auth/emails/duplicate-email`

Provided Context
  ``email``
    The ``EmailAddress`` instance that has already been registered.

******************
Verification Email
******************

Sent when a user adds a new email address to their account. This can either be
their first time registering or they can be adding another email address to an
existing account. This email should ideally contain a link that the user can
click to verify their email address.

Template Path
  :file:`email_auth/emails/verify-email`

Provided Context
  ``email``
    The ``EmailAddress`` instance that has already been registered.
  ``user``
    The user account who owns the email address that the verification is sent
    to.
  ``verification``
    The ``EmailVerification`` instance containing the token used to verify
    ownership of the email address.

**************
Password Reset
**************

Sent when a user requests a password reset and the email address they provided
exists in the system and is verified.

Template Path
  :file:`email_auth/emails/reset-password`

Provided Context
  ``password_reset``
    The ``PasswordReset`` instance containing the token used to reset the user's
    password.


.. _django-email-utils: https://github.com/cdriehuys/django-email-utils
