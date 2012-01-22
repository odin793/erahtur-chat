# _*_ coding: utf-8 _*_;

from django import template
from django.conf import settings
from django.db.models.fields.files import ImageFieldFile
from erahtur.village.models import *
from django.contrib.auth import views as auth_views
from PIL import Image
from os import path, makedirs
from hashlib import sha256
import pytils
import re

register = template.Library()

@register.inclusion_tag('navbar/navbar.html')
def navbar():
    org_list = Organization.objects.all()[:10]
    hist_list = History.objects.all()
    neighbour_list = Neighbour.objects.all()
    return {
        'org_list': org_list,
        'hist_list': hist_list,
        'neighbour_list': neighbour_list
    }

@register.inclusion_tag('navbar/panorams_list_template.html')
def panorams_list(panorams):    
    return {'panorams': panorams,}

@register.simple_tag
def chat_host_name():
    chat_host_name = settings.CHAT_HOST_NAME
    return chat_host_name

@register.filter(name = 'get_thumbnail')
def get_thumbnail(photo):
    if isinstance(photo, ImageFieldFile): # photo can be object from models or an image
        infile_path = photo.path
    else:
        infile_path = photo.image.path
    infile_name = path.split(infile_path)[1]
    infile_dir = path.split(infile_path)[0]
    thumb_dir = path.join(infile_dir, 'thumbnails')
    if not path.exists(thumb_dir):
        makedirs(thumb_dir)
    outfile_name = path.splitext(infile_name)[0] + '_thumbnail.jpg'
    outfile_path = path.join(thumb_dir, outfile_name)
    if isinstance(photo, ImageFieldFile):
        outfile_url = photo.url.replace(path.split(infile_path)[1], path.join('thumbnails', outfile_name))    
    else:
        outfile_url = photo.image.url.replace(path.split(infile_path)[1], path.join('thumbnails', outfile_name))    
    if not path.exists(outfile_path):
        try:
            im = Image.open(infile_path)
            x, y = im.size
            if x == y:
                im.thumbnail((170, 170), Image.ANTIALIAS)
                im.save(outfile_path, "JPEG")
                return outfile_url                    
            if x > y:
                 left = int(round((x-y)/2))
                 upper = 0
                 right = left + y
                 lower = y
            elif x < y:
                left = 0
                upper = int(round((y-x)*0.8/2)) # 0.8 - because user head is usually in the upper part of the photo
                right = x
                lower = x + int(round((y-x)*0.8/2))
            size = (170, 170)
            box = (left, upper, right, lower)
            crop_im = im.crop(box)
            crop_im.thumbnail(size, Image.ANTIALIAS)
            crop_im.save(outfile_path, "JPEG")
            return outfile_url    
        except:
            if isinstance(photo, ImageFieldFile):
                return photo.url
            else:
                return photo.image.url
    else:
        return outfile_url

    
@register.filter(name='pytils_date')
def pytils_date(date):
    return pytils.dt.ru_strftime(u"%d %B %Y", inflected=True, date=date)

@register.filter(name='get_url')
def get_url(url):
    if re.search(r'^http://', url) is not None:
        return url
    else:
        return 'http://' + url

@register.filter(name='phone_repr')
def phone_repr(phone_str):
    if len(phone_str) == 11:
        phone_repr = '%s %s %s %s %s' % (
            phone_str[0], phone_str[1:4], 
            phone_str[4:7], phone_str[7:9],
            phone_str[9:11]
        )
    else:
        phone_repr = phone_str
    return phone_repr

@register.simple_tag
def chat_auth_token(user):
    return sha256(settings.SECRET_KEY + ":" + user.username).hexdigest()
    
@register.inclusion_tag('navbar/right_column.html')
def right_column():
    pubs = Publication.objects.all()
    archive_pubs = pubs.filter(archive=True).order_by('-date')
    years = set([pub.date.year for pub in archive_pubs])
    date_pairs = {}
    for year in years:
        pubs = archive_pubs.filter(date__year=year)
        months = set([pub.date.month for pub in pubs])
        date_pairs[year] = months
    return {'date_pairs_processor': date_pairs,}
