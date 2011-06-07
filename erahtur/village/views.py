# _*_ coding: utf-8 _*_;

# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.http import Http404
from village.models import *
from tagging.models import TaggedItem
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
import datetime
import os
from erahtur import settings
import django
from django.db.models import Q
import re

def make_photo_pairs(photo_set):    # return list of lists of two photos
    photo_pairs = []
    for i in range(0, len(photo_set), 2):
        pair = list(photo_set)[i: i+2]  # two photos: (0, 1), (2, 3) and so on
        if len(pair) == 1:
            pair.append(None)   # for the last photo, if len(photo_set)/2 != 0
        photo_pairs.append(pair)
    return photo_pairs

def redirect(request):
    return HttpResponseRedirect('/publications/news/district/1')

def org_list(request):
    return render_to_response('org_list.html', RequestContext(request, {
        'org_list': Organization.objects.all(),
    }))

"""
def pub_list(request, page_num):
    pubs = Publication.objects.all()
    from_pub = (int(page_num)-1) * 10
    to_pub = from_pub + 10
    pub_dict = {}
    for location in ['district', 'region', 'oblast']:
        try:
            pub_dict[location] = pubs.filter(location=location, archive=False)[from_pub:to_pub]
        except:
            pub_dict[location] = []
    district_pub_list = pub_dict['district']
    region_pub_list = pub_dict['region']
    oblast_pub_list = pub_dict['oblast']
    return render_to_response('publications_list.html', RequestContext(request, {
        'district_pub_list': district_pub_list,
        'region_pub_list': region_pub_list,
        'oblast_pub_list': oblast_pub_list,
        'pages': range(1, 11),
        'current_page': int(page_num),
    }))
"""

def publication_statistics(publication):
    words_list = publication.raw_content().split(' ')
    words_number = len(filter(lambda s: len(s) > 1, words_list))
    pictures_number = publication.publicationphoto_set.count()
    comments_number = publication.comment_set.count()
    return (words_number, pictures_number, comments_number)

def pub_list(request, pub_type, page_num):
    pubs = Publication.objects.all()
    pub_type_dict = {'district': u'Округ', 'region': u'Район', 'oblast': u'Область'}
    from_pub = (int(page_num)-1) * 10
    to_pub = from_pub + 10
    pub_list = pubs.filter(location=pub_type, archive=False)[from_pub:to_pub]
    # pub_list is list of tuples (pub, (pub_statistics))
    pub_list = zip(pub_list, map(publication_statistics, pub_list))
    return render_to_response('publications/new_pub_list.html', RequestContext(request, {
        'pub_list': pub_list,
        'pub_type': pub_type,
        'russian_pub_type': pub_type_dict[pub_type],
        'pages': range(1, 11),
        'current_page': int(page_num),
    }))
    

def publications_archive(request): # returns dict of years and months of archive pubs
     pubs = Publication.objects.all()
     archive_pubs = pubs.filter(archive=True).order_by('-date')
     years = set([pub.date.year for pub in archive_pubs])
     date_pairs = {}
     for year in years:
         pubs = archive_pubs.filter(date__year=year)
         months = set([pub.date.month for pub in pubs])
         date_pairs[year] = months
     return render_to_response('pubs_archive/publications_archive.html', RequestContext(request, {
        'dict': date_pairs,
     }))

def archive_processor(HttpRequest):
    pubs = Publication.objects.all()
    archive_pubs = pubs.filter(archive=True).order_by('-date')
    years = set([pub.date.year for pub in archive_pubs])
    date_pairs = {}
    for year in years:
        pubs = archive_pubs.filter(date__year=year)
        months = set([pub.date.month for pub in pubs])
        date_pairs[year] = months
    return {'date_pairs_processor': date_pairs,}

def pub_archive_months(request, year, month): # returns all archive pubs in year year and month month
    pub_list = Publication.objects.filter(date__year=year, date__month=month).order_by('-date')
    pub_list = zip(pub_list, map(publication_statistics, pub_list))
    return render_to_response('pubs_archive/pub_archive_months.html', RequestContext(request, {
        'pub_list': pub_list,
        'year': year,
        'month': month,
    }))

def organization(request, org_id):
    organization = Organization.objects.get(id=org_id)
    photo_set = organization.organizationphoto_set.all()
    #photo_pairs = make_photo_pairs(photo_set)
    return render_to_response('organization.html', RequestContext(request, {
        'organization': organization,
        'photos': photo_set,
    }))

    
def publication(request, pub_id):   # page of publications
    publication = Publication.objects.get(id=pub_id)
    pub_stats = publication_statistics(publication)
    photo_set = publication.publicationphoto_set.all()  # all the photos for publication
    #photo_pairs = make_photo_pairs(photo_set)
    return render_to_response('publications/publication.html', RequestContext(request, {
        'publication': publication,
        'pub_stats': pub_stats,
        'photos': photo_set,
    }))

def ajax_news_block(request):
    pub_id = request.POST.get('pub_id', '')
    if pub_id:
        try:
            publication = Publication.objects.get(id=pub_id)
            news_block = publication.content
        except:
            news_block = u'произошла ошибка'
        return render_to_response('publications/ajax_news_block.html', {
            'news_block': news_block,
        })
    else:
        return render_to_response('publications/ajax_news_block.html', {
            'news_block': u'произошла ошибка',
        })
        

@login_required
def add_comment(request, pub_id):   # add new comment to publication with pub_id
    if request.method == 'POST':
        publication = Publication.objects.get(id=pub_id)
        author = User.objects.get(id=request.user.id)
        text = request.POST['comments_text']
        new_comment = Comment.objects.create(publication=publication, author=author, text=text)
        new_comment.save()
    return HttpResponseRedirect('/publications/%s' % pub_id)    

def pubs_by_tag(request, tag_id):  # returns pubs, associated with specified tag
    tag = get_object_or_404(Tag, id=tag_id)
    pubs_by_tag = TaggedItem.objects.get_by_model(Publication, tag)
    pub_list = zip(pubs_by_tag, map(publication_statistics, pubs_by_tag))
    return render_to_response('publications/pubs_by_tag.html', RequestContext(request, {
        'pub_list': pub_list,
        'tag': tag,
    }))
    

def hist_list(request):
    return render_to_response('hist_list.html', RequestContext(request, {
        'hist_list': History.objects.all(),
    }))

def history(request, hist_id):
    history = History.objects.get(id=hist_id)
    photo_set = history.historyphoto_set.all()
    return render_to_response('history.html', RequestContext(request, {
        'history': history,
        'photos': photo_set,
    }))
    
def neighbour_list(request):
    return render_to_response('neighbour_list.html', RequestContext(request, {
        'neighbour_list': Neighbour.objects.all(),
    }))

def neighbour(request, neighbour_id):
    neighbour = Neighbour.objects.get(id=neighbour_id)
    photo_set = neighbour.neighbourphoto_set.all()
    #photo_pairs = make_photo_pairs(photo_set)
    return render_to_response('neighbour.html', RequestContext(request, {
        'neighbour': neighbour,
        'photos': photo_set,
    }))

def music(request):
    return render_to_response('creation/music.html', RequestContext(request, {
        'songs_list': Song.objects.all(),
    }))
     
def log_in(request):
    url=request.META.get('HTTP_REFERER', '/')
    user = auth.authenticate(username=request.POST.get('username', None), password=request.POST.get('password', None))
    if user is not None:
        auth.login(request, user)
        #user_profile = user.userprofile_set.all()[0]
        #user_profile.auth_token = os.urandom(5).encode('hex')
        #user_profile.save()
        return HttpResponseRedirect(url)
    if '?' in url:
        url += '&login_error=1'
    else:
        url += '?login_error=1'
    return HttpResponseRedirect(url)

def login_page(request):    # logs user in and redirects to where arg. where arg is got via GET method
    #url=request.META.get('HTTP_REFERER', '/')
    login_errors = 0
    where = request.GET.get('where', '/')
    if request.user.is_authenticated():
        #return HttpResponseRedirect('/forum')
        return HttpResponseRedirect(where)
    if request.method == "POST":
        user = auth.authenticate(username=request.POST.get('username', None), 
                                password=request.POST.get('password', None))
        if user is not None:
            auth.login(request, user)
            #user_profile = user.userprofile_set.all()[0]
            #user_profile.auth_token = os.urandom(5).encode('hex')
            #user_profile.save()
            return HttpResponseRedirect(where)
        else:
            login_errors = 1
    return render_to_response('login_page.html', RequestContext(request, {
        'login_errors': login_errors,
        'where': where,
    }))

def logout(request):
    url = '/'
    auth.logout(request)
    return HttpResponseRedirect(url)

def login_processor(request):
    return {'login_error': request.GET.get('login_error', False)}

def registration(request):
    from erahtur.forms import RegistrationForm
    from django.contrib.auth.models import User
    if request.method=='POST':
        form = RegistrationForm(request.POST)
        if form.is_valid() and form.login_valid():
            username = form.cleaned_data['username']
            password1 = form.cleaned_data['password1']
            password2 = form.cleaned_data['password2']
            email = form.cleaned_data['email']
            if password1 == password2:
                new_user = User.objects.create_user(username=username, password=password1, email=email)
                new_user.save()
                user = auth.authenticate(username=username, password=password1)
                if user is not None:
                    auth.login(request, user)
                return HttpResponseRedirect('/accounts/user_profile_handle/')   
            return render_to_response('registration/registration.html', RequestContext(request, {
                'error': u'Пароли не одинаковые. Повторите ввод',
                'form':form,
            }))
    else:
        form=RegistrationForm()
    return render_to_response('registration/registration.html', RequestContext(request, {'form': form,}))

def is_username_unique(request):
    username = request.POST.get('username', '');
    if username:
        try:
            db_user = User.objects.get(username=username);
            unique = u'bad'
            print unique
        except User.DoesNotExist:
            unique = u'good'
            print unique
    else:
        unique = u'введите имя'
    return render_to_response('registration/is_username_unique.html', {
        'unique': unique,
    })

@login_required
def user_profile_handle(request):   # creating and changing user profile
    from forms import UserProfileForm
    try:
        profile = request.user.get_profile()
        if profile.phones:
            phones_list = profile.phones.split('\n')
        else:
            phones_list = []
        #phone_amount = len(phones_list) + 1
        if profile.sites:
            sites_list = profile.sites.split('\n')
        else:
            sites_list = []
    except UserProfile.DoesNotExist:
        profile = UserProfile(user=request.user)
        phones_list = []
        sites_list = []
        
    try:    
        year = int(request.POST['year'])
        month = int(request.POST['month'])
        day = int(request.POST['day'])
        save_bitrh_date = True
    except:
        save_bitrh_date = False
    
    form = UserProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if form.is_valid():
        pr = form.save(commit=False)
        
        new_phones_list = request.POST.getlist('phone') # take all phones from POST
            # filter bad phones
        clean_phones_list = filter(lambda x: len(x.strip())>0, new_phones_list)
            # making string from phones list
        phones_str = '\n'.join([unicode(p) for p in clean_phones_list])
        if phones_str:
            pr.phones = phones_str
        
        new_sites_list = request.POST.getlist('site')
        clean_sites_list = filter(lambda x: len(x.strip())>0, new_sites_list)
        sites_str = '\n'.join([unicode(p) for p in clean_sites_list])
        pr.sites = sites_str
        
        if save_bitrh_date:
            if day and month and year is not None: 
                    # add birth date to UserProfile object
                pr.birth_date = datetime.date(year, month, day)
            else:
                p.birth_date = None
        
        pr.save()
        user_profile_url = os.path.join('/accounts/user_profile', request.user.username)
        return HttpResponseRedirect(user_profile_url)
    
    return render_to_response("user_profile_handle.html", RequestContext(request, {
        "form": form,
        "phones_list": phones_list,
        'sites_list': sites_list,
    }))

def user_profile(request, username):    # display any user profile page
    req_user = request.user
    try:
        prof_user = User.objects.get(username=username)
        try:
            profile = prof_user.get_profile()
            if profile.phones:
                phones_list = profile.phones.split('\n')
            else:
                phones_list = []
            if profile.sites:
                sites_list = profile.sites.split('\n')
            else:
                sites_list = []
        except:
            profile = False
            phones_list = []
            sites_list = []
        logged_in = False
        if req_user == prof_user:
            logged_in = True            
        return render_to_response('user_profile.html', RequestContext(request, {
            'profile': profile,
            'prof_user': prof_user,
            'logged_in': logged_in,
            'phones_list': phones_list,
            'sites_list': sites_list,
        }))
    except:
        message = u'Пользователя %s не существует' % username
        return render_to_response('user_doesnt_exist.html', RequestContext(request, {
            'message': message,
        }))

def photoalbums_list(request):  #   display all photo albums
    photoalbums_list = PhotoAlbum.objects.all()
    data = []
    for album in photoalbums_list:
        album_key_photo = Photo.objects.filter(album=album, key_photo=True)[0]
        data.append([album, album_key_photo])
    return render_to_response('creation/photoalbums_list.html', RequestContext(request, {
        'data': data,
    }))

def photoalbum(request, album_id):
    album = PhotoAlbum.objects.get(id=album_id)
    photos = album.photos.all()
    #photo_pairs = make_photo_pairs(photos)
    return render_to_response('creation/photoalbum.html', RequestContext(request, {
        'album': album,
        'photos': photos,
    }))

def links(request):
    links_sections = LinkSection.objects.all()
    return render_to_response('links.html', RequestContext(request, {
        'links_sections': links_sections,
    }))

def search(request):
    query = request.GET.get('id_search', '')
    splitted_query_list = query.split(' ')
    if query not in splitted_query_list: # query has more than one word
        query_list = splitted_query_list + [query]
    else :
        query_list = [query]
    # in search_dict key is pub, value is block of pub's text with highlighted tokens
    search_dict = {} 
    hl_dict = {} # tokens to highlight and pubs, where it was finded
    for token in query_list:
        pubs = []
        edited_token = token
        #pubs = find_pubs(edited_token)
        #if pubs and len(token) > 2: # short tokens are not good. only 3 signs and more
        #    hl_dict[edited_token] = pubs
        #elif not pubs and len(token) > 3:
        if len(token) > 5:
            # delete 1 sign from the token to expand search results
            edited_token = token[:-2] 
            #pubs = find_pubs(edited_token)
            pubs = find_pubs(edited_token)
            if pubs:
                hl_dict[edited_token] = pubs
        #if not pubs and len(token) > 5:
        elif len(token) > 3:
            # delete 2 signs from the token to expand search results for long tokens  
            edited_token = token[:-1] 
            #pubs = find_pubs(edited_token)                
            pubs = find_pubs(edited_token)                
            if pubs:
                hl_dict[edited_token] = pubs
        elif len(token) > 2:
            pubs = find_pubs(edited_token)
            if pubs:
                hl_dict[edited_token] = pubs
    all_finded_tokens = hl_dict.keys() # list of finded tokens
    all_finded_pubs = hl_dict.values() # is a list of lists of finded pubs
    
    # constructing one list of pubs to highlight
    pubs_to_hl = reduce(lambda x, y: x + y, all_finded_pubs, []) 
    for pub in set(pubs_to_hl):
        search_dict[pub] = [
            pub.title,
            highlight_token(pub.raw_preface(), all_finded_tokens),
            highlight_token(pub.raw_content(), all_finded_tokens),
        ]
    
    return render_to_response('search/search_results.html', RequestContext(request, {
        'query': query,
        'search_dict': search_dict,
    }))

def highlight_token(text, tokens_list):
    
    """"
    highlights tokens in tokens_list in object's text fields
    returns block of text with highlighted tokens
    
    The idea is to make a tokens map (positions of tokens in text)
    Then we cut whole text according to tokens map
    Then we pass these blocks of text as arguments to hightlighting function
    """
    
    tokens_map = get_tokens_map(text, tokens_list) # make map
    # cut text and making unique list of text blocks
    blocks_of_result = set(get_results_blocks(text, tokens_map)) 
    
    # hightlighting begins
    highlighted_blocks = []
    for text_block in blocks_of_result:    
        for token in tokens_list: # constructing text with highlighted tokens
            #space_position = text_block.find(' ', text_block.find(token))
            #token = text_block[text_block.find(token):space_position]
            output_text = re.sub(
                token, 
                '<span style="background-color: #FFFACD;">%s</span>' % token,
                text_block,
            )
            text_block = output_text # to highlight another token in next cycle
        highlighted_blocks.append(text_block)
    
    return highlighted_blocks

def get_tokens_map(text, tokens_list):
    """returns list of positions, where tokens are placed in text"""
    tokens_map = []
    for token in tokens_list:
        pos = -1
        new_pos = 0
        while new_pos != -1:
            new_pos = text.find(token, pos+1)
            if new_pos != -1:
                tokens_map.append(new_pos)
            pos = new_pos
            
    tokens_map = sorted(tokens_map)
    return tokens_map

def get_results_blocks(text, tokens_map):
    """returns blocks of text with tokens instead of all publication text"""
    if not tokens_map:
        return []
    begin_from = tokens_map[0]-60
    if begin_from < 0:
         begin_from = 0
    if len(tokens_map) == 1:
        return ['...' + text[begin_from: tokens_map[0]+80] + '...']
    blocks = []
    n = 0
    last = tokens_map[-1]
    for i in range(1, len(tokens_map)):
        if tokens_map[i] - tokens_map[n] > 150:
            if tokens_map[i] - tokens_map[i-1] < 100:
                m = (tokens_map[i] - tokens_map[i-1])/2
            else:
                m = 50
            blocks.append('...' + text[begin_from: tokens_map[i-1]+m] + '...')
            distance = tokens_map[i] - tokens_map[i-1]
            begin_from = tokens_map[i]-m
            n = i
            if tokens_map[i]==last:
                blocks.append('...' + text[begin_from: tokens_map[i]+80] + '...')        
        
        elif tokens_map[i]==tokens_map[-1]:
            blocks.append('...' + text[begin_from: tokens_map[i]+80] + '...')                     
    
    return blocks
    
def find_pubs(token):
    """find pubs with token token. returns list of pubs"""
    pubs = []
    for pub in Publication.objects.all():
        raw_pub = pub.raw_publication() # removes html tags
        if re.search(token, raw_pub):
            pubs.append(pub)
    return pubs
     