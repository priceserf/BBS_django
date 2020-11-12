class Page(object):
    def __init__(self,cuss_page,all_count,per_page,show_page,base_url):
        '''

        :param cuss_page:  当前的页数
        :param all_count:  数据库总行数
        :param per_page:   每一页显示的行数
        :show_page     :   设定的一次显示的页数
        :base_url      :   需要设置的地址
        '''
        try:
            self.cuss_page=int(cuss_page)
        except Exception as e:
            self.cuss_page=1
        self.per_page=per_page
        self.all_count=all_count
        self.show_page =show_page
        self.base=base_url

    def start(self):
        start = (self.cuss_page - 1) * self.per_page
        return start

    def end(self):
        end = self.cuss_page * self.per_page
        return end

    def page(self):
        page_list=[]
        # 拿到总页数a
        a,b=divmod(self.all_count,self.per_page)
        if b:
            a=a+1
        self.all_page=a

        # 设置页面数字的显示数量，每次显示11个页数,#以当年的页面数为基准

        make_page = int((self.show_page - 1) / 2)   #5 当前页数前后显示页码的数量
        bagin=1
        end_for=self.all_page+1
        if self.all_page <= self.show_page:      #对总页数的判断，如果总页数小于11
            bagin=1
            end_for=self.all_page + 1
        else:                                    #总页数大于11页
            if self.cuss_page <= make_page :     #当前页数小于等于5时
                bagin=1
                end_for=self.show_page + 1
            else:                                #当前页数大于5
                if self.cuss_page + make_page > self.all_page:      #当前页面加上后5页总和如果大于总页数
                    bagin=self.all_page - self.show_page + 1
                    end_for=self.all_page + 1
                else:
                    bagin=self.cuss_page - make_page
                    end_for=self.cuss_page + make_page + 1

        # 创建上一页按钮
        if self.cuss_page <=1:
            vue = "<li><a href='%s?page=#'></a></li>"%(self.base)
        else:
            vue = "<li><a href='%s?page=%s'>上一页</a><li>" %(self.base,self.cuss_page-1)
        page_list.append(vue)

        # 拿到每一个页码数字
        for i in range(bagin,end_for):
            if i == self.cuss_page:  #如果当年选择的页数和网址上的页数一致
                temp ="<li class='active'><a href='%s?page=%s'>%s</a></li>" %(self.base,i,i)
            else:
                temp = "<li><a href='%s?page=%s'>%s</a></li>" % (self.base,i,i)
            page_list.append(temp)

        # 设置下一页按钮
        if self.cuss_page >= self.all_page:
            bot = "<li><a href='/backend?page=ds'></a><li>"
        else:
            bot = "<li><a href='%s?page=%s'>下一页</a></li>" % (self.base,self.cuss_page + 1)
        page_list.append(bot)

        return ''.join(page_list)
