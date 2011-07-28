# _*_ coding: utf-8 _*_;

from urllib import urlencode

from django.utils.datastructures import MultiValueDictKeyError
from django.core.paginator import Paginator, EmptyPage
from django.http import Http404
from django.conf import settings


def unicode_urlencode(params):
    """
    A unicode aware version of urllib.urlencode
    """

    if isinstance(params, dict):
        params = params.items()
    return urlencode([(k, isinstance(v, unicode) and v.encode('utf-8') or v) for k, v in params])


class NinjaPaginator(object):
    """
    Pagination decorator with multiple types of pagination
    Should be used along with 'render_to' decorator
    from django-annoying application
    http://bitbucket.org/offline/django-annoying/wiki/Home
    """

    def __init__(self, object_list='object_list', style=None, per_page=10, frame_size=8):
        """
        receive decorator parameters 
        """
        self.object_list = object_list
        self.style = style or getattr(settings, "PAGINATION_STYLE", "digg")
        self.per_page = per_page
        self.per_page_backup = per_page
        self.frame_size = frame_size
        
    def __call__(self, function):
        """
        receive decorated function and return decorate method
        """
        self.function = function
        return self.decorate
    
    def decorate(self, request, *args, **kwargs):
        """
        style pagination according to 'style' parameter
        """
        self.output = self.function(request, *args, **kwargs)
        if not isinstance(self.output, dict):
            return self.output
        
        params = request.GET.copy()
        
        try:
            self.page_num = int(params.pop('page')[0])
        except (ValueError, KeyError):
            self.page_num = 1

        if "per_page" in params:
            self.per_page = int(params['per_page'])
        else:
            # reset per_page variable to default
            self.per_page = self.per_page_backup
            params['per_page'] = self.per_page
            
        extra_params = unicode_urlencode(params)

        self.paginate_qs = self.output.pop(self.object_list)
        self.paginator = Paginator(self.paginate_qs, self.per_page)
        try:
            self.page = self.paginator.page(self.page_num)
        except EmptyPage:
            raise  Http404()
        self.output['page_num'] = self.page_num
        self.output['per_page'] = self.per_page
        self.output['extra_params'] = extra_params
        self.pages = self.paginator.num_pages
        self.output[self.object_list] = self.page.object_list
        self.output[self.style] = True
        run_style = getattr(self, "%s_style" % self.style)
        return run_style()
    
    def digg_style(self):
        if self.page_num > 1:
            self.output['PREVIOUS'] = self.page_num -1
        if self.page_num < self.paginator.num_pages:
            self.output['NEXT'] = self.page_num + 1
        if self.pages > self.frame_size and self.pages <= self.frame_size +2:
            self.output['left_page_numbers'] = range(1, self.pages + 1)
        elif self.pages < self.frame_size:
            self.output['left_page_numbers'] = range(1, self.pages + 1)
        elif self.pages > self.frame_size and self.page_num < self.frame_size - 1:
            self.output['left_page_numbers'] = range(1, self.frame_size + 1)
            self.output['right_page_numbers'] = range(self.pages -1, self.pages +1)
        elif self.pages > self.frame_size and self.page_num > self.frame_size - 2 and self.pages - (self.frame_size / 2) <= self.page_num + 1:
            self.output['left_page_numbers'] = range(1, 3)
            self.output['middle_page_numbers'] = range(self.pages - self.frame_size + 1, self.pages +1)
        elif self.pages > self.frame_size and self.page_num > self.frame_size - 2:
            self.output['left_page_numbers'] = range(1, 3)
            self.output['middle_page_numbers'] = range(self.page_num - (self.frame_size / 2) +1, self.page_num + (self.frame_size / 2))
            self.output['right_page_numbers'] = range(self.pages -1, self.pages +1)
        return self.output

    def filmfeed_style(self):
        if self.pages < self.frame_size:
            self.output['page_numbers'] = range(1, self.pages + 1)
        elif self.page_num < (self.frame_size / 2) + 1:
            self.output['page_numbers'] = range(1, self.frame_size + 1)
        elif self.page_num >= (self.frame_size / 2) + 1 and self.pages - (self.frame_size / 2) <= self.page_num:
            self.output['page_numbers'] = range(self.pages - self.frame_size + 1, self.pages + 1)
        elif self.page_num >= (self.frame_size / 2) + 1:
            start = self.page_num - (self.frame_size / 2)
            end = self.page_num + (self.frame_size / 2)
            self.output['page_numbers'] = range(start, end + 1)
        return self.output
    
    def muzx_style(self):
        side_size = int(self.frame_size / 2.0)
        left_plus = max(0, side_size - (self.pages - self.page_num))
        right_plus = max(0, side_size - (self.page_num - 1))
        prev_pages = range(1, self.page_num)[-1 * (side_size + left_plus):]
        next_pages = range(self.page_num + 1, self.pages + 1)[:side_size + right_plus]
        self.output['page_numbers'] = prev_pages + [self.page_num] + next_pages
        return self.output
