
class PaginationHandler(object):
    def __init__(self, current_page, data_count,urlname,per_page_count=10, pager_num=7):
        self.current_page = current_page
        self.data_count = data_count
        self.per_page_count = per_page_count
        self.pager_num = pager_num
        self.urlname=urlname

    @property
    def start(self):
        return (self.current_page - 1) * self.per_page_count

    @property
    def end(self):
        return self.current_page * self.per_page_count

    @property
    def total_count(self):
        v, y = divmod(self.data_count, self.per_page_count)
        if y:
            v += 1
        return v

    def render(self,keyword=''):
        page_list = []
        if self.total_count < self.pager_num:
            start_index = 1
            end_index = self.total_count + 1
        else:
            if self.current_page <= (self.pager_num + 1) / 2:
                start_index = 1
                end_index = self.pager_num + 1
            else:
                start_index = self.current_page - (self.pager_num - 1) / 2
                end_index = self.current_page + (self.pager_num + 1) / 2
                if (self.current_page + (self.pager_num - 1) / 2) > self.total_count:
                    end_index = self.total_count + 1
                    start_index = self.total_count - self.pager_num + 1

        if self.current_page == 1:
            prev=u'<li class="am-disabled"><a href="javascript:void(0);">«</a></li>'
        else:
            prev = u'<li><a  href="%s?page=%s%s">«</a></li>' % (self.urlname, self.current_page - 1,keyword)
        page_list.append(prev)

        for i in range(int(start_index), int(end_index)):
            if i == self.current_page:
                temp=u'<li class="am-active"><a  href="%?page=%s%s">%s</a></li>' % (self.urlname, i,keyword, i)
            else:
                temp=u'<li><a  href="%s?page=%s%s">%s</a></li>' % (self.urlname, i,keyword, i)
            page_list.append(temp)

        if self.current_page == self.total_count:
            nex=u'<li class="next-page"><a href="javascript:void(0);">»</a></li>'
        else:
            nex = u'<li class="next-page"><a class="page" href="%s?page=%s%s">»</a></li>' % (self.urlname, self.current_page + 1,keyword)
        page_list.append(nex)
        page_sum=u'<li><span class="am-text-secondary">共 %s 页</span></li>'%self.total_count
        page_list.append(page_sum)
        page_str = "".join(page_list)
        return page_str


	  
