===============
 zope.sendmail
===============

.. image:: https://img.shields.io/pypi/v/zope.sendmail.svg
        :target: https://pypi.python.org/pypi/zope.sendmail/
        :alt: Latest release

.. image:: https://img.shields.io/pypi/pyversions/zope.sendmail.svg
        :target: https://pypi.org/project/zope.sendmail/
        :alt: Supported Python versions

.. image:: https://travis-ci.com/zopefoundation/zope.sendmail.svg?branch=master
        :target: https://travis-ci.com/zopefoundation/zope.sendmail

.. image:: https://coveralls.io/repos/github/zopefoundation/zope.sendmail/badge.svg?branch=master
        :target: https://coveralls.io/github/zopefoundation/zope.sendmail?branch=master

.. image:: https://readthedocs.org/projects/zopesendmail/badge/?version=latest
        :target: https://zopesendmail.readthedocs.io/en/latest/
        :alt: Documentation Status

zope.sendmail is a package for email sending from Zope 3 applications.
Email sending from Zope 3 applications works as follows:

A Zope 3 application locates a mail delivery utility
(``IMailDelivery``) and feeds a message to it. It gets back a unique
message ID so it can keep track of the message by subscribing to
``IMailEvent`` events.

The utility registers with the transaction system to make sure the
message is only sent when the transaction commits successfully.
(Among other things this avoids duplicate messages on
``ConflictErrors``.)

If the delivery utility is a ``IQueuedMailDelivery``, it puts the
message into a queue (a Maildir mailbox in the file system). A
separate process or thread (``IMailQueueProcessor``) watches the queue
and delivers messages asynchronously. Since the queue is located in
the file system, it survives Zope restarts or crashes and the mail is
not lost.  The queue processor can implement batching to keep the
server load low.

If the delivery utility is a ``IDirectMailDelivery``, it delivers
messages synchronously during the transaction commit.  This is not a
very good idea, as it makes the user wait.  Note that transaction
commits must not fail, but that is not a problem, because mail
delivery problems dispatch an event instead of raising an exception.

However, there is a problem -- sending events causes unknown code to
be executed during the transaction commit phase.  There should be a
way to start a new transaction for event processing after this one is
commited.

An ``IMailQueueProcessor`` or ``IDirectMailDelivery`` actually
delivers the messages by using a mailer (``IMailer``) component that
encapsulates the delivery process.  There currently is only one
mailer:

``ISMTPMailer`` sends all messages to a relay host using SMTP.

Documentation is hosted at https://zopesendmail.readthedocs.io/
