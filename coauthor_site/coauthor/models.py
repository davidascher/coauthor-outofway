# here, we keep track of user's etherpad authorIDs

import requests, json, time
from django.contrib.auth.models import User, Group

from django.db import models
from django.db.models.signals import pre_save, post_save
from django.conf import settings
from etherpad import etherpad

class UserProfile(models.Model):
    # This field is required.
    user = models.OneToOneField(User)

    # Other fields here
    etherpad_author_id = models.CharField(max_length=20)

class GroupProfile(models.Model):
    # This field is required.
    group = models.OneToOneField(Group)

    # Other fields here
    etherpad_group_id = models.CharField(max_length=20)

# XXX: handle model deletion -> pad deletion

class Pad(models.Model):
    group = models.ForeignKey(Group)
    author = models.ForeignKey(User, related_name="pads")
    name = models.CharField(max_length=20)

def before_pad_save(sender, instance, **kwargs):
    padID = etherpad.createGroupPad(instance.group.groupprofile.etherpad_group_id,
        instance.name)
    etherpad.setPublicStatus(padID, 'false')

pre_save.connect(before_pad_save, sender=Pad)


def on_group_save(sender, instance, created, **kwargs):
    # we need to create a etherpad groupid
    if created:
        try:
            groupID = etherpad.createGroupIfNotExistsFor(instance.name)
            groupprofile = GroupProfile(group=instance, etherpad_group_id=groupID)
            groupprofile.save()
        except Exception, err:  # XXX not sure why i need this - should happen automatically
            print err
            raise ValueError(err);

def on_user_save(sender, instance, created, **kwargs):
    # we need to create a user profile, and an etherpad authorid
    # we'll also automatically create a group for just this user
    if created:
        # create a group for each user, create an etherpad author ID and group ID
        # for each user/group, and add the user to their own group to start.
        try:
            group = Group(name=instance.email)
            group.save()
            instance.groups.add(group)
            instance.save()
            authorID = etherpad.createAuthorIfNotExistsFor(instance.email)
            profile = UserProfile(user=instance, etherpad_author_id=authorID)
            profile.save()
        except Exception, err:  # XXX not sure why i need this - should happen automatically
            print err
            raise ValueError(err);

post_save.connect(on_user_save, sender=User)
post_save.connect(on_group_save, sender=Group)