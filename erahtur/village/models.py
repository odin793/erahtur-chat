# -*- coding: utf-8 -*-
from django.db import models
from django.conf import settings as django_settings
from tinymce import models as tinymce_models
from django.contrib.auth.models import User
import tagging
from tagging.fields import TagField
from tagging.models import Tag
from os import path
from django.db.models import signals
from PIL import Image
from pytils.translit import translify
from django.core.files.storage import FileSystemStorage
from django.db.models.fields.files import FileField
from html2text import html2text as h2t
from re import sub

class SongField(FileField):
    def __init__(self, *args, **kwargs):
        super(SongField, self).__init__(*args, **kwargs)
    
    def translit(self, name):
        output_name = []
        for letter in name:
            try:
                out_letter = translify(letter)
            except ValueError:
                out_letter = '1'
            output_name.append(out_letter)
        output_name = ''.join(output_name)
        return output_name
    
    def pre_save(self, model_instance, add):
         "Returns field's value just before saving."
         file = super(FileField, self).pre_save(model_instance, add)
         if file and not file._committed:
             # Commit the file to storage prior to saving the model
             file.name = self.translit(file.name)
             file.save(file.name, file, save=False)
         return file
        

class MyPhotoField(SongField, models.ImageField):
    pass


class SongSystemStorage(FileSystemStorage):
    def __init__(self, option=None):
        #if not option:
        #    option = django_settings.CUSTOM_STORAGE_OPTIONS
        super(SongSystemStorage, self).__init__(option)
    
    def delete(self, name):
        super(SongSystemStorage, self).delete(name)
    
    def exists(self, name):
        super(SongSystemStorage, self).exists(name)
    
    def listdir(self, path):
        super(SongSystemStorage, self).listdir(path)
    
    def size(self, name):
        super(SongSystemStorage, self).size(name)
    
    def url(self, name):
        super(SongSystemStorage, self).url(name)
    
    def translit(self, name):
        output_name = []
        orig_url = self.url(name)
        for letter in name:
            try:
                out_letter = translify(letter)
            except ValueError:
                out_letter = '1'
            output_name.append(out_letter)
        output_name = ''.join(output_name)
        return output_name
    
    def save(self, name, content):
        translit_name = self.translit(name)
        print content.size, content.name, translit_name
        super(SongSystemStorage, self).save(translit_name, content) 
    
song_storage = SongSystemStorage()
        
# Create your models here.
    

class Organization(models.Model):
    name = models.CharField(u'название', max_length=50)
    about = tinymce_models.HTMLField(u'описание')
    sort = models.IntegerField(verbose_name=u'порядок следования', default=0)
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ("sort",)
        verbose_name = u'организация'
        verbose_name_plural = u'Организации'

        
class Publication(models.Model):
    title = models.CharField(u'название', max_length = 50)
    preface = tinymce_models.HTMLField(u'вступление')
    content = tinymce_models.HTMLField(u'содержание')
    location = models.CharField(u'место', max_length = 20, choices = (
        ('district', u'округ'),
        ('region', u'район'),
        ('oblast', u'область'),
    ))
    date = models.DateTimeField(verbose_name = u'дата')
    archive = models.BooleanField(verbose_name=u'в архив?', default=False)
    tags = TagField(verbose_name=u'Тэги')
    
    def get_absolute_url(self):
        from django.core.urlresolvers import reverse
        return reverse('publication', args=[self.id])
    
    def set_tags(self, tags):
        Tag.objects.update(self, tags)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
    
    def raw_text(self, html_field): # makes practically raw text from html
        #delete additional signs after h2t function
        return sub('[\t\n\r*#]+', ' ', h2t(html_field))
        
    def raw_publication(self): 
        return self.raw_title() + self.raw_preface() + self.raw_content()
    
    def raw_title(self):
        return self.raw_text(self.title).lower()
    
    def raw_preface(self):
        return self.raw_text(self.preface).lower()

    def raw_content(self):
        return self.raw_text(self.content).lower()
            
    def __unicode__(self):
        return self.title
    
    class Meta:
        ordering = ("-date",)
        verbose_name = u'публикация'
        verbose_name_plural = u'Публикации'
        

def publication_post_save_handler(sender, **kwargs):
    if kwargs.get("created", False):
        ids = []
        for loc in ["district", "region", "oblast"]:
            # all non-archive pubs older than 100 last pubs
            for pub in Publication.objects.filter(location=loc, archive=False)[100:]:
                ids.append(pub.pk)
        if ids:
            # its should be in archive
            Publication.objects.filter(pk__in=ids).update(archive=True) 
signals.post_save.connect(publication_post_save_handler, sender=Publication)


class Comment(models.Model):
    publication = models.ForeignKey(Publication)
    author = models.ForeignKey(User)
    text = models.TextField(verbose_name=u'комментарий')
    date_added = models.DateTimeField(auto_now_add=True)


class History(models.Model):
    period = models.CharField(u'период', max_length = 50)
    content = tinymce_models.HTMLField(u'содержание')
    sort = models.IntegerField(verbose_name=u'порядок следования', default=0)
    
    def __unicode__(self):
        return self.period
    
    class Meta:
        ordering = ('sort',)
        verbose_name = u'исторический период'
        verbose_name_plural = u'Исторические периоды'


class PublicationPhoto(models.Model):
    image = MyPhotoField(u'фото', upload_to='photos/publications')
    description = models.CharField(u'описание', max_length=100)
    pub = models.ForeignKey(Publication)
    
    class Meta:
        verbose_name_plural = u'Фотографии к публикации'
    
    def __unicode__(self):
        return u'фото к публикации'


class HistoryPhoto(models.Model):
    image = MyPhotoField(u'фото', upload_to='photos/history')
    description = models.CharField(u'описание', max_length=100)
    history = models.ForeignKey(History)  

    class Meta:
        verbose_name_plural = u'Фотографии к историческому периоду'
    
    def __unicode__(self):
        return u'фото периода'

    
class Neighbour(models.Model):
    name = models.CharField(u'название', max_length = 50)
    content = tinymce_models.HTMLField(u'содержание')
    sort = models.IntegerField(verbose_name=u'порядок следования' ,default=0)   
    
    def __unicode__(self):
        return self.name
    
    class Meta:
        ordering = ('sort', )
        verbose_name = u'сосед'
        verbose_name_plural = u'Соседи'


class NeighbourPhoto(models.Model):
    image = MyPhotoField(u'фото', upload_to='photos/neighbours')
    description = models.CharField(u'описание', max_length=100)
    neighbour = models.ForeignKey(Neighbour)

    class Meta:
        verbose_name_plural = u'Фотографии соседа'
    
    def __unicode__(self):
        return u'фото соседа'


class OrganizationPhoto(models.Model):
    image = MyPhotoField(u'фото', upload_to='photos/organizations')
    description = models.CharField(u'описание', max_length=100)
    organization = models.ForeignKey(Organization)    

    class Meta:
        verbose_name_plural = u'Фотографии организации'
    
    def __unicode__(self):
        return u'фото организации'


class Song(models.Model):
    song = SongField(verbose_name=u'трек', upload_to='audio')
    name = models.CharField(u'название', max_length=80, blank=True, null=True)
    artist = models.CharField(u'исполнитель', max_length=80, blank=True, null=True)
    year = models.PositiveIntegerField(verbose_name=u'год', blank=True, null=True)
               
    class Meta:
        ordering = ('-year', )
        verbose_name = u'трек'
        verbose_name_plural = u'Аудиозаписи'
    
    def __unicode__(self):
        return u'трек'


class UserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    avatar = MyPhotoField(u'аватар', upload_to='photos/user_avatars', blank=True)
    first_name = models.CharField(u'имя', max_length=30, blank=True)
    last_name = models.CharField(u'фамилия', max_length=30, blank=True)
    patronymic = models.CharField(u'отчество', max_length=30, blank=True)
    birth_date = models.DateField(verbose_name=u'дата рождения', blank=True, null=True)
    icq = models.CharField(verbose_name='ICQ', max_length=20, blank=True, null=True)
    location = models.CharField(verbose_name=u'место жительства', max_length=60, blank=True, null=True)
    #site = models.URLField(u'сайт', max_length=80, blank=True, null=True, verify_exists=False)
    phones = models.TextField(u'телефоны', blank=True)
    sites = models.TextField(u'сайты', blank=True)
    #auth_token = models.CharField(u'входной токен', max_length=16 ,blank=True)
    
    class Meta:
        verbose_name = u'профиль пользователя'
        verbose_name_plural = u'Профили пользователей'


class PhotoAlbum(models.Model):
    name = models.CharField(u'название', max_length=50)
    description = models.CharField(u'описание', max_length=150, blank=True)

    class Meta:
        verbose_name = u'фотоальбом'
        verbose_name_plural = u'Фотоальбомы'    


class Photo(models.Model):
    album = models.ForeignKey('PhotoAlbum', related_name='photos')
    image = MyPhotoField(u'фото', upload_to='photos/photos')
    description = models.CharField(u'описание', max_length=100, blank=True)
    key_photo = models.BooleanField(u'обложка')
    
    class Meta:
        verbose_name = u'фото'
        verbose_name_plural = u'фотографии'
    
    def __unicode__(self):
        return u'фото'
    

class Panorama(models.Model):
    name = models.CharField(u'название', max_length=100)
    preview_1 = MyPhotoField(u'превью_1', upload_to='photos/panorams')
    preview_2 = MyPhotoField(u'превью_2', upload_to='photos/panorams')
    short_description = tinymce_models.HTMLField(u'короткое описание')
    full_description = tinymce_models.HTMLField(u'полное описание')
    date = models.DateField(verbose_name=u'дата съемки', blank=True, null=True)
    jpg_1_link_download = models.URLField(u'jpg_1 архив', max_length=150, verify_exists=False)
    jpg_1_download_size = models.CharField(u'jpg_1 размер архива', max_length=30)
    flash_1_link_download = models.URLField(u'flash_1 архив', max_length=150, verify_exists=False)
    flash_1_download_size = models.CharField(u'flash_1 размер архива', max_length=30)
    mov_1_link_download = models.URLField(u'mov_1 архив', max_length=150, verify_exists=False)
    mov_1_download_size = models.CharField(u'mov_1 размер архива', max_length=30)
    jpg_1_link_view = models.URLField(u'jpg_1', max_length=150, verify_exists=False)
    jpg_1_view_size = models.CharField(u'jpg_1 размер', max_length=30)
    flash_1_link_view = models.URLField(u'flash_1', max_length=150, verify_exists=False)
    flash_1_view_size = models.CharField(u'flash_1 размер', max_length=30)
    jpg_2_link_download = models.URLField(u'jpg_2 архив', max_length=150, verify_exists=False)
    jpg_2_download_size = models.CharField(u'jpg_2 размер архива', max_length=30)
    flash_2_link_download = models.URLField(u'flash_2 архив', max_length=150, verify_exists=False)
    flash_2_download_size = models.CharField(u'flash_2 размер архива', max_length=30)
    jpg_2_link_view = models.URLField(u'jpg_2', max_length=150, verify_exists=False)
    jpg_2_view_size = models.CharField(u'jpg_2 размер', max_length=30)
    flash_2_link_view = models.URLField(u'flash_2', max_length=150, verify_exists=False)
    flash_2_view_size = models.CharField(u'flash_2 размер', max_length=30)
    tags = TagField(verbose_name=u'Тэги')
    
    def set_tags(self, tags):
        Tag.objects.update(self, tags)
    
    def get_tags(self):
        return Tag.objects.get_for_object(self)
        
    class Meta:
        verbose_name = u'панорама'
        verbose_name_plural = u'Панорамы'
    
    def __unicode__(self):
        return self.name


class LinkSection(models.Model):
    name = models.CharField(u'название раздела', max_length=30)
    sort = models.IntegerField(verbose_name=u'порядок следования', default=0)
    
    class Meta:
        ordering = ('sort', )
        verbose_name = u'раздел ссылкок'
        verbose_name_plural = u'Ссылки'


class Link(models.Model):
    name = models.CharField(u'название', max_length = 30)
    href = models.URLField(u'ссылка', max_length=80, verify_exists=False)
    section = models.ForeignKey('LinkSection', related_name='links')
    
    class Meta:
        ordering = ('id',)
        verbose_name = u'ссылка'
        verbose_name_plural = u'Ссылки'
    
    def __unicode__(self):
        return u'ссылка'
    