========
Releases
========

This guide is intended to complement the `OpenStack releases site
<https://releases.openstack.org/>`__, and the project team guide's section on
`release management
<https://docs.openstack.org/project-team-guide/release-management.html>`__.

Team members make themselves familiar with the release schedule for the current
release, for example https://releases.openstack.org/train/schedule.html.

Release Model
=============

As a deployment project, Kayobe's release model differs from many other
OpenStack projects. Kayobe follows the `cycle-trailing
<https://docs.openstack.org/project-team-guide/release-management.html#trailing-the-common-cycle>`__
release model, to allow time after the OpenStack coordinated release to wait
for distribution packages and support new features. This gives us three months
after the final release to prepare our final releases. Users are typically keen
to try out the new release, so we should aim to release as early as possible
while ensuring we have confidence in the release.

Release Schedule
================

While we don't wish to repeat the OpenStack release documentation, we will
point out the high level schedule, and draw attention to areas where our
process is different.

Milestones
----------

At each of the various release milestones, pay attention to what other projects
are doing.

Feature Freeze
--------------

As with projects following the common release model, Kayobe uses a feature
freeze period to allow the code to stabilise prior to release. There is no
official feature freeze date for the cycle-trailing model, but we typically
freeze around **three weeks** after the common feature freeze. During this
time, no features should be merged to the master branch.

Before RC1
==========

Prior to creating a release candidate and stable branch, the following tasks
should be performed.

Testing
-------

Test the code and fix at a minimum all critical issues.

.. _update-dependencies-for-release:

Update dependencies to upcoming release
---------------------------------------

Prior to the release, we update the dependencies and upper constraints on the
master branch to use the upcoming release. This is now quite easy to do,
following the introduction of the ``openstack_release`` variable. This is done
prior to creating a release candidate. For example, see
https://review.opendev.org/#/c/694616/.

Synchronise kayobe-config
-------------------------

Ensure that configuration defaults in ``kayobe-config`` are in sync with those
under ``etc/kayobe`` in ``kayobe``. This can be done via:

.. code-block:: console

   cp -aR kayobe/etc/kayobe/* kayobe-config/etc/kayobe

Commit the changes and submit for review.

Synchronise kayobe-config-dev
-----------------------------

Ensure that configuration defaults in ``kayobe-config-dev`` are in sync with
those in ``kayobe-config``. This requires a little more care, since some
configuration options have been changed from the defaults. Choose a method to
suit you and be careful not to lose any configuration.

Commit the changes and submit for review.

Prepare release notes
---------------------

It's possible to add a prelude to the release notes for a particular release
using a ``prelude`` section in a ``reno`` note.

Ensure that release notes added during the release cycle are tidy and
consistent. The following command is useful to list release notes added this
cycle::

    git diff --name-only origin/stable/<previous release> -- releasenotes/

RC1
===

Prior to cutting a stable branch, the ``master`` branch should be tagged as a
release candidate.  This allows the ``reno`` tool to determine where to stop
searching for release notes for the next release.  The tag should take the
following form: ``<release tag>.0rc$n``, where ``$n`` is the release candidate
number.

This should be done for each deliverable using the `releases
<https://opendev.org/openstack/releases>`_ tooling. A release candidate and
stable branch defintitions should be added for each Kayobe deliverable
(``kayobe``, ``kayobe-config``, ``kayobe-config-dev``).  These are defined in
``deliverables/<release name>/kayobe.yaml``. Currently the same version is used
for each deliverable.

The changes should be proposed to the releases repository. For example:
https://review.opendev.org/#/c/700174.

After RC1
=========

The OpenStack proposal bot will propose changes to the new branch and the
master branch. These need to be approved.

After the stable branch has been cut, the master branch can be unfrozen and
development on features for the next release can begin. At this point it will
still be using dependencies and upper constraints from the release branch, so
revert the patch created in :ref:`update-dependencies-for-release`. For
example, see https://review.opendev.org/701747.

Finally, set the previous release used in upgrade jobs to the new release. For
example, see https://review.opendev.org/709145.

RC2+
====

Further release candidates may be created on the stable branch as necessary in
a similar manner to RC1.

Final Releases
==============

A release candidate may be promoted to a final release if it has no critical
bugs against it.

Tags should be created for each deliverable (``kayobe``, ``kayobe-config``,
``kayobe-config-dev``). Currently the same version is used for each.

The changes should be proposed to the releases repository. For example:
https://review.opendev.org/701724.

Post-release activites
----------------------

An email will be sent to the release-announce mailing list about the new
release.

Continuing Development
======================

Search for TODOs in the codebases describing tasks to be performed during the
next release cycle.

Stable Releases
===============

Stable branch releases should be made periodically for each supported stable
branch, no less than once every 45 days.
