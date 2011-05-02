#!/usr/bin/env python
# encoding: utf-8
"""
admin.py

Created by Stas Kotseruba on 2010-06-26.
Copyright (c) 2010 __MyCompanyName__. All rights reserved.
"""

from django.contrib import admin
from django import forms
from tinymce.widgets import TinyMCE
from village.models import *

class PublicationPhotoInline(admin.TabularInline):
    model = PublicationPhoto
    #fieldsets = (
    #(u'общее', {'fields': ('image', 'description')}))
    

class HistoryPhotoInline(admin.TabularInline):
    model = HistoryPhoto
    

class NeighbourPhotoInline(admin.TabularInline):
    model = NeighbourPhoto


class OrganizationPhotoInline(admin.TabularInline):
    model = OrganizationPhoto
    

class PhotoInline(admin.TabularInline):
    model = Photo


class CommentsInline(admin.TabularInline):
    model = Comment


class PhotoAlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'description', )
    inlines = (PhotoInline, )


class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', "sort",)
    list_editable = ("sort", )
    inlines = (OrganizationPhotoInline, )


class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'preface',)
    inlines = [PublicationPhotoInline, CommentsInline]


class HistoryAdmin(admin.ModelAdmin):
    list_display = ('period', 'sort')
    list_editable = ('sort', )
    inlines = [HistoryPhotoInline, ]


class NeighbourAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort')
    list_editable = ('sort', )
    inlines = [NeighbourPhotoInline, ]


class SongAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', )


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'icq', 'pk')
    

class LinkInline(admin.TabularInline):
    model = Link
    extra = 5
    ordered_by = ['-id', ]

class LinkSectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'sort', )
    list_editable = ('sort', )
    inlines = [LinkInline, ]
    
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Publication, PublicationAdmin)
admin.site.register(History, HistoryAdmin)
admin.site.register(Neighbour, NeighbourAdmin)
admin.site.register(Song, SongAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(PhotoAlbum, PhotoAlbumAdmin)
admin.site.register(LinkSection, LinkSectionAdmin)

admin.site.root_path = '/admin/'

