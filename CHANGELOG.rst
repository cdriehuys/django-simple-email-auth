#########
Changelog
#########

**************
In Development
**************

Breaking Changes
================

* #12: Removed ``normalized_address`` field from ``EmailAddress`` model because
  its behavior can easily be replicated by querying against ``address__iexact``.

Features
========

* #11: Added utility method ``EmailAddress.send_verification_email`` to
  encapsulate the process of creating an ``EmailVerification`` instance and
  sending an email for it.

******
v0.1.0
******

Features
========

* Added models to track email addresses and verify them.
