Introduction
============

This is a full-blown functional test. The emphasis here is on testing what
the user may input and see, and the system is largely tested as a black box.
We use PloneTestCase to set up this test as well, so we have a full Plone site
to play with. We *can* inspect the state of the portal, e.g. using 
self.portal and self.folder, but it is often frowned upon since you are not
treating the system as a black box. Also, if you, for example, log in or set
roles using calls like self.setRoles(), these are not reflected in the test
browser, which runs as a separate session.

Being a doctest, we can tell a story here.

First, we must perform some setup. We use the testbrowser that is shipped
with Five, as this provides proper Zope 2 integration. Most of the 
documentation, though, is in the underlying zope.testbrower package.

    >>> from Products.Five.testbrowser import Browser
    >>> browser = Browser()
    >>> portal_url = self.portal.absolute_url()

The following is useful when writing and debugging testbrowser tests. It lets
us see all error messages in the error_log.

    >>> self.portal.error_log._ignored_exceptions = ()

With that in place, we can go to the portal front page and log in. We will
do this using the default user from PloneTestCase:

    >>> from Products.PloneTestCase.setup import portal_owner, default_password

Because add-on themes or products may remove or hide the login portlet, this test will use the login form that comes with plone.  

    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()

Here, we set the value of the fields on the login form and then simulate a
submit click.  We then ensure that we get the friendly logged-in message:

    >>> "You are now logged in" in browser.contents
    True

Finally, let's return to the front page of our site before continuing

    >>> browser.open(portal_url)

-*- extra stuff goes here -*-
The Volume content type
===============================

In this section we are tesing the Volume content type by performing
basic operations like adding, updadating and deleting Volume content
items.

Adding a new Volume content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Volume' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Volume').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Volume' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Volume Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Volume' content item to the portal.

Updating an existing Volume content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Volume Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Volume Sample' in browser.contents
    True

Removing a/an Volume content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Volume
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Volume Sample' in browser.contents
    True

Now we are going to delete the 'New Volume Sample' object. First we
go to the contents tab and select the 'New Volume Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Volume Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Volume
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Volume Sample' in browser.contents
    False

Adding a new Volume content item as contributor
------------------------------------------------

Not only site managers are allowed to add Volume content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Volume' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Volume').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Volume' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Volume Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Volume content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Publication content type
===============================

In this section we are tesing the Publication content type by performing
basic operations like adding, updadating and deleting Publication content
items.

Adding a new Publication content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Publication' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Publication').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Publication' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Publication Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Publication' content item to the portal.

Updating an existing Publication content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Publication Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Publication Sample' in browser.contents
    True

Removing a/an Publication content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Publication
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Publication Sample' in browser.contents
    True

Now we are going to delete the 'New Publication Sample' object. First we
go to the contents tab and select the 'New Publication Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Publication Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Publication
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Publication Sample' in browser.contents
    False

Adding a new Publication content item as contributor
------------------------------------------------

Not only site managers are allowed to add Publication content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Publication' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Publication').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Publication' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Publication Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Publication content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Praesentationen von Internetressourcen content type
===============================

In this section we are tesing the Praesentationen von Internetressourcen content type by performing
basic operations like adding, updadating and deleting Praesentationen von Internetressourcen content
items.

Adding a new Praesentationen von Internetressourcen content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Praesentationen von Internetressourcen' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Internetressourcen').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Internetressourcen' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Internetressourcen Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Praesentationen von Internetressourcen' content item to the portal.

Updating an existing Praesentationen von Internetressourcen content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Praesentationen von Internetressourcen Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Praesentationen von Internetressourcen Sample' in browser.contents
    True

Removing a/an Praesentationen von Internetressourcen content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Praesentationen von Internetressourcen
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Internetressourcen Sample' in browser.contents
    True

Now we are going to delete the 'New Praesentationen von Internetressourcen Sample' object. First we
go to the contents tab and select the 'New Praesentationen von Internetressourcen Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Praesentationen von Internetressourcen Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Praesentationen von Internetressourcen
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Internetressourcen Sample' in browser.contents
    False

Adding a new Praesentationen von Internetressourcen content item as contributor
------------------------------------------------

Not only site managers are allowed to add Praesentationen von Internetressourcen content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Praesentationen von Internetressourcen' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Internetressourcen').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Internetressourcen' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Internetressourcen Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Praesentationen von Internetressourcen content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Praesentationen von Aufsatz in Zeitschrift content type
===============================

In this section we are tesing the Praesentationen von Aufsatz in Zeitschrift content type by performing
basic operations like adding, updadating and deleting Praesentationen von Aufsatz in Zeitschrift content
items.

Adding a new Praesentationen von Aufsatz in Zeitschrift content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Praesentationen von Aufsatz in Zeitschrift' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Aufsatz in Zeitschrift').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Aufsatz in Zeitschrift' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Aufsatz in Zeitschrift Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Praesentationen von Aufsatz in Zeitschrift' content item to the portal.

Updating an existing Praesentationen von Aufsatz in Zeitschrift content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Praesentationen von Aufsatz in Zeitschrift Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Praesentationen von Aufsatz in Zeitschrift Sample' in browser.contents
    True

Removing a/an Praesentationen von Aufsatz in Zeitschrift content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Praesentationen von Aufsatz in Zeitschrift
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Aufsatz in Zeitschrift Sample' in browser.contents
    True

Now we are going to delete the 'New Praesentationen von Aufsatz in Zeitschrift Sample' object. First we
go to the contents tab and select the 'New Praesentationen von Aufsatz in Zeitschrift Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Praesentationen von Aufsatz in Zeitschrift Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Praesentationen von Aufsatz in Zeitschrift
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Aufsatz in Zeitschrift Sample' in browser.contents
    False

Adding a new Praesentationen von Aufsatz in Zeitschrift content item as contributor
------------------------------------------------

Not only site managers are allowed to add Praesentationen von Aufsatz in Zeitschrift content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Praesentationen von Aufsatz in Zeitschrift' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Aufsatz in Zeitschrift').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Aufsatz in Zeitschrift' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Aufsatz in Zeitschrift Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Praesentationen von Aufsatz in Zeitschrift content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Praesentation von Aufsatz in Sammelband content type
===============================

In this section we are tesing the Praesentation von Aufsatz in Sammelband content type by performing
basic operations like adding, updadating and deleting Praesentation von Aufsatz in Sammelband content
items.

Adding a new Praesentation von Aufsatz in Sammelband content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Praesentation von Aufsatz in Sammelband' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentation von Aufsatz in Sammelband').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentation von Aufsatz in Sammelband' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentation von Aufsatz in Sammelband Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Praesentation von Aufsatz in Sammelband' content item to the portal.

Updating an existing Praesentation von Aufsatz in Sammelband content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Praesentation von Aufsatz in Sammelband Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Praesentation von Aufsatz in Sammelband Sample' in browser.contents
    True

Removing a/an Praesentation von Aufsatz in Sammelband content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Praesentation von Aufsatz in Sammelband
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Praesentation von Aufsatz in Sammelband Sample' in browser.contents
    True

Now we are going to delete the 'New Praesentation von Aufsatz in Sammelband Sample' object. First we
go to the contents tab and select the 'New Praesentation von Aufsatz in Sammelband Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Praesentation von Aufsatz in Sammelband Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Praesentation von Aufsatz in Sammelband
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Praesentation von Aufsatz in Sammelband Sample' in browser.contents
    False

Adding a new Praesentation von Aufsatz in Sammelband content item as contributor
------------------------------------------------

Not only site managers are allowed to add Praesentation von Aufsatz in Sammelband content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Praesentation von Aufsatz in Sammelband' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentation von Aufsatz in Sammelband').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentation von Aufsatz in Sammelband' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentation von Aufsatz in Sammelband Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Praesentation von Aufsatz in Sammelband content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Rezension einer Zeitschrift content type
===============================

In this section we are tesing the Rezension einer Zeitschrift content type by performing
basic operations like adding, updadating and deleting Rezension einer Zeitschrift content
items.

Adding a new Rezension einer Zeitschrift content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Rezension einer Zeitschrift' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension einer Zeitschrift').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension einer Zeitschrift' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension einer Zeitschrift Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Rezension einer Zeitschrift' content item to the portal.

Updating an existing Rezension einer Zeitschrift content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Rezension einer Zeitschrift Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Rezension einer Zeitschrift Sample' in browser.contents
    True

Removing a/an Rezension einer Zeitschrift content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Rezension einer Zeitschrift
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Rezension einer Zeitschrift Sample' in browser.contents
    True

Now we are going to delete the 'New Rezension einer Zeitschrift Sample' object. First we
go to the contents tab and select the 'New Rezension einer Zeitschrift Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Rezension einer Zeitschrift Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Rezension einer Zeitschrift
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Rezension einer Zeitschrift Sample' in browser.contents
    False

Adding a new Rezension einer Zeitschrift content item as contributor
------------------------------------------------

Not only site managers are allowed to add Rezension einer Zeitschrift content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Rezension einer Zeitschrift' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension einer Zeitschrift').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension einer Zeitschrift' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension einer Zeitschrift Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Rezension einer Zeitschrift content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Praesentationen von Monographien content type
===============================

In this section we are tesing the Praesentationen von Monographien content type by performing
basic operations like adding, updadating and deleting Praesentationen von Monographien content
items.

Adding a new Praesentationen von Monographien content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Praesentationen von Monographien' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Monographien').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Monographien' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Monographien Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Praesentationen von Monographien' content item to the portal.

Updating an existing Praesentationen von Monographien content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Praesentationen von Monographien Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Praesentationen von Monographien Sample' in browser.contents
    True

Removing a/an Praesentationen von Monographien content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Praesentationen von Monographien
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Monographien Sample' in browser.contents
    True

Now we are going to delete the 'New Praesentationen von Monographien Sample' object. First we
go to the contents tab and select the 'New Praesentationen von Monographien Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Praesentationen von Monographien Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Praesentationen von Monographien
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Praesentationen von Monographien Sample' in browser.contents
    False

Adding a new Praesentationen von Monographien content item as contributor
------------------------------------------------

Not only site managers are allowed to add Praesentationen von Monographien content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Praesentationen von Monographien' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Praesentationen von Monographien').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Praesentationen von Monographien' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Praesentationen von Monographien Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Praesentationen von Monographien content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Rezension einer Monographie content type
===============================

In this section we are tesing the Rezension einer Monographie content type by performing
basic operations like adding, updadating and deleting Rezension einer Monographie content
items.

Adding a new Rezension einer Monographie content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Rezension einer Monographie' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension einer Monographie').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension einer Monographie' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension einer Monographie Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Rezension einer Monographie' content item to the portal.

Updating an existing Rezension einer Monographie content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Rezension einer Monographie Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Rezension einer Monographie Sample' in browser.contents
    True

Removing a/an Rezension einer Monographie content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Rezension einer Monographie
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Rezension einer Monographie Sample' in browser.contents
    True

Now we are going to delete the 'New Rezension einer Monographie Sample' object. First we
go to the contents tab and select the 'New Rezension einer Monographie Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Rezension einer Monographie Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Rezension einer Monographie
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Rezension einer Monographie Sample' in browser.contents
    False

Adding a new Rezension einer Monographie content item as contributor
------------------------------------------------

Not only site managers are allowed to add Rezension einer Monographie content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Rezension einer Monographie' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension einer Monographie').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension einer Monographie' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension einer Monographie Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Rezension einer Monographie content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)


The Rezension content type
===============================

In this section we are tesing the Rezension content type by performing
basic operations like adding, updadating and deleting Rezension content
items.

Adding a new Rezension content item
--------------------------------

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

Then we select the type of item we want to add. In this case we select
'Rezension' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

And we are done! We added a new 'Rezension' content item to the portal.

Updating an existing Rezension content item
---------------------------------------

Let's click on the 'edit' tab and update the object attribute values.

    >>> browser.getLink('Edit').click()
    >>> browser.getControl(name='title').value = 'New Rezension Sample'
    >>> browser.getControl('Save').click()

We check that the changes were applied.

    >>> 'Changes saved' in browser.contents
    True
    >>> 'New Rezension Sample' in browser.contents
    True

Removing a/an Rezension content item
--------------------------------

If we go to the home page, we can see a tab with the 'New Rezension
Sample' title in the global navigation tabs.

    >>> browser.open(portal_url)
    >>> 'New Rezension Sample' in browser.contents
    True

Now we are going to delete the 'New Rezension Sample' object. First we
go to the contents tab and select the 'New Rezension Sample' for
deletion.

    >>> browser.getLink('Contents').click()
    >>> browser.getControl('New Rezension Sample').click()

We click on the 'Delete' button.

    >>> browser.getControl('Delete').click()
    >>> 'Item(s) deleted' in browser.contents
    True

So, if we go back to the home page, there is no longer a 'New Rezension
Sample' tab.

    >>> browser.open(portal_url)
    >>> 'New Rezension Sample' in browser.contents
    False

Adding a new Rezension content item as contributor
------------------------------------------------

Not only site managers are allowed to add Rezension content items, but
also site contributors.

Let's logout and then login as 'contributor', a portal member that has the
contributor role assigned.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = 'contributor'
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)

We use the 'Add new' menu to add a new content item.

    >>> browser.getLink('Add new').click()

We select 'Rezension' and click the 'Add' button to get to the add form.

    >>> browser.getControl('Rezension').click()
    >>> browser.getControl(name='form.button.Add').click()
    >>> 'Rezension' in browser.contents
    True

Now we fill the form and submit it.

    >>> browser.getControl(name='title').value = 'Rezension Sample'
    >>> browser.getControl('Save').click()
    >>> 'Changes saved' in browser.contents
    True

Done! We added a new Rezension content item logged in as contributor.

Finally, let's login back as manager.

    >>> browser.getLink('Log out').click()
    >>> browser.open(portal_url + '/login_form')
    >>> browser.getControl(name='__ac_name').value = portal_owner
    >>> browser.getControl(name='__ac_password').value = default_password
    >>> browser.getControl(name='submit').click()
    >>> browser.open(portal_url)



