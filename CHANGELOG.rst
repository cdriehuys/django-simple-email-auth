#########
Changelog
#########

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
