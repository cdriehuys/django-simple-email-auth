#########
Changelog
#########

**************
In Development
**************

Breaking Changes
================

* #23: The default ordering of `EmailVerification` instances has been switched
  from ``email__normalized_address`` (doesn't exist) to ``time_created``.

Features
========

* #6: Add ``PasswordReset`` model to facilitate password resets using verified
  email addresses.
* #20: Add ``EmailAddress.send_already_verified`` method to send a notification
  to the user that their email address has already been verified.

Bug Fixes
=========

* #22: The ``time_sent`` field is now populated when calling
  ``EmailVerification.send_email``.

******
v0.2.0
******

Breaking Changes
================

* #12: Removed ``normalized_address`` field from ``EmailAddress`` model because
  its behavior can easily be replicated by querying against ``address__iexact``.
* #13: Rename admin class ``EmailVerification`` to ``EmailVerificationAdmin``.

Features
========

* #11: Added utility method ``EmailAddress.send_verification_email`` to
  encapsulate the process of creating an ``EmailVerification`` instance and
  sending an email for it.
* #14: Added method to send a notification that an email address had another
  registration attempt.

******
v0.1.0
******

Features
========

* Added models to track email addresses and verify them.
