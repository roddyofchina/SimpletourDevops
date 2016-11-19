#!/usr/bin/env python
#coding:utf-8

__author__ = 'Luodi'

from django.utils.safestring import mark_safe

def Page(page,url,all_pages_count,search=str('')):
    '''
    :param page:当前页
    :param all_pages_count:总页数
    :return:分页后的html字符串
    '''
    page_html=[]
    print search
    a_html = '''<li><a href="%s/1%s">首页</a></li>''' %(url,str(search))
    page_html.append(a_html)
    if page>1:
        a_html = '''<li><a href="%s/%d%s">上一页</a></li>'''%(url,page-1,str(search))
    else:
        a_html = '''<li class="disabled"><a href="#">上一页</a></li>'''
    page_html.append(a_html)
    #11个页码
    if all_pages_count<11:
        begain=0
        end=all_pages_count
    #总页数大于11
    else:
        if page<6:
            begain=0
            end =12
        else:
            if page+6>all_pages_count:
                begain=page-5
                end = all_pages_count
            else:
                begain=page -5
                end =page+5

    for i in range(begain,end):
        if page == i+1:
            a_html='''<li class="page-number active"><a href="%s/%d%s">%d</a></li>'''%(url,i+1,str(search),i+1)
        else:
            a_html='''<li><a href="%s/%d%s">%d</a></li>'''%(url,i+1,str(search),i+1)
        page_html.append(a_html)
    if page<all_pages_count:
        a_html = '''<li><a href="%s/%d%s">下一页</a></li>'''%(url,page+1,str(search))
    else:
        a_html = '''<li class="disabled"><a href="#">下一页</a></li>'''

    page_html.append(a_html)
    a_html = '''<li><a href="%s/%d%s">尾页</a></li>'''%(url,all_pages_count,str(search))
    page_html.append(a_html)
    page = mark_safe(' '.join(page_html))
    return  page

def PageCount(page):
    per_item = 15
    page =int(page)
    start = (page-1)*per_item
    end = page*per_item
    return page,start,end,per_item

