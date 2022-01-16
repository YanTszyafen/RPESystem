from django.shortcuts import render
from home.models import AdsCategory, Ad, Comment, RPESModel
from django.http.response import HttpResponseNotFound
# Create your views here.
from django.views import View
from django.core.paginator import Paginator, EmptyPage
from django.shortcuts import redirect
from django.urls import reverse

class IndexView(View):
    def get(self,request):
        categories=AdsCategory.objects.all()
        cat_id=request.GET.get('cat_id',1)
        try:
            category=AdsCategory.objects.get(id=cat_id)
        except AdsCategory.DoesNotExist:
            return HttpResponseNotFound('No such category!')
        # 4. Get paging parameters
        page_num = request.GET.get('page_num', 1)
        page_size = request.GET.get('page_size', 6)
        ads = Ad.objects.filter(category=category)
        # 6. Create Paginator
        paginator = Paginator(ads, page_size)
        # 7. Paging
        try:
            page_ads = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page!')
        # total page
        total_page = paginator.num_pages
        # 8. Translate data to templates
        context = {
            'categories': categories,
            'category': category,
            'ads': page_ads,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num
        }
        return render(request, 'index.html',context=context)

class DetailView(View):
    def get(self, request):
        # 1. Receive ad id
        id = request.GET.get('id')
        # 4. Get paging parameters
        page_size = request.GET.get('page_size', 6)
        # print(page_size)
        page_num = request.GET.get('page_num', 1)
        # print(page_num)
        # 3. Query category data
        categories = AdsCategory.objects.all()
        # 2. Query ad data by id
        try:
            ad = Ad.objects.get(id=id)
        except Ad.DoesNotExist:
            return render(request, '404.html')
        else:
            ad.total_views += 1
            ad.save()

        # Query the top 10 article data
        hot_ads = Ad.objects.order_by('-total_views')[:9]

        # 5. Query comment data by the info of paging
        comments = Comment.objects.filter(ad=ad).order_by('-created')

        total_count = comments.count()
        # 6. Create Paginator
        paginator = Paginator(comments, page_size)
        # 7. Paging
        try:
            page_comments = paginator.page(page_num)
        except EmptyPage:
            return HttpResponseNotFound('Empty Page!')
        # print(paginator.page(1))
        # print(paginator.page(2))
        # print(paginator.page(3))
        total_page = paginator.num_pages

        # 8. Translate data to templates
        context = {
            'categories': categories,
            'category': ad.category,
            'ad': ad,
            'hot_ads': hot_ads,
            'total_count': total_count,
            'comments': page_comments,
            'page_size': page_size,
            'total_page': total_page,
            'page_num': page_num
        }
        return render(request, 'detail.html', context=context)
    def post(self,request):
        #1. Receive user info
        user = request.user
        # 2. Check user is logged in or not
        if user and user.is_authenticated:
            # 3. Logged in users can post form data
            #     3.1 Receive comment data
            id = request.POST.get('id')
            content = request.POST.get('content')
            #     3.2 Check the article is exist or not
            try:
                ad = Ad.objects.get(id=id)
            except Ad.DoesNotExist:
                return HttpResponseNotFound('No such ad!')
            #     3.3 Save comment data
            Comment.objects.create(
                content=content,
                ad=ad,
                user=user
            )
            #     3.4 Modify the number of comments on the article
            ad.comments_count += 1
            ad.save()

            path = reverse('home:detail')+'?id={}'.format(ad.id)
            return redirect(path)
        else:
            # 4. Not logged in users will jump to the login page
            return redirect(reverse('users:login'))


class PredictView(View):
    def get(self, request):
        return render(request, 'predict.html')
    def post(self,request):
        room = int(request.POST.get('room'))
        metro = request.POST.get('metro')
        square = float(request.POST.get('square'))
        modelob = RPESModel.objects.get(id=1)
        result = modelob.r1 * room
        if metro in ['м.Обухово', 'м.Озерки', 'м.Лесная', 'м.Площадь Мужества', 'м.Ладожская', 'м.Пионерская', 'м.Елизаровская', 'м.Конкретный', 'м.Технологический институт', 'м.проспект Большевиков',\
                     'м.Академическая', 'м.Московские ворота', 'м.Парк Победы', 'м.Бухарестская', 'м.Московская', 'м.Электросила', 'м.Старая деревня', 'м.Зенит', 'м.Василеостровская', 'м.Фрунзенская',\
                     'м.Обходной канал','м.Звенигородская','м.Черная река','м.Международный','м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская',\
                     'м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая','м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская',\
                     'м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m1
        if metro in ['м.Лесная','м.Площадь Мужества','м.Ладожская','м.Пионерская','м.Елизаровская','м.Конкретный','м.Технологический институт','м.проспект Большевиков','м.Академическая','м.Московские ворота',\
            'м.Парк Победы','м.Бухарестская','м.Московская','м.Электросила','м.Старая деревня','м.Зенит','м.Василеостровская','м.Фрунзенская','м.Обходной канал','м.Звенигородская','м.Черная река',\
            'м.Международный','м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская','м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор',\
            'м.Беговая','м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская',\
            'м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m2
        if metro in ['м.Бухарестская','м.Московская''м.Электросила','м.Старая деревня','м.Зенит','м.Василеостровская','м.Фрунзенская','м.Обходной канал','м.Звенигородская','м.Черная река','м.Международный',\
                     'м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская','м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая',\
                     'м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская',\
                     'м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m3
        if metro in ['м.Московская','м.Электросила','м.Старая деревня','м.Зенит','м.Василеостровская','м.Фрунзенская','м.Обходной канал','м.Звенигородская','м.Черная река','м.Международный',\
                     'м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская','м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая',\
                     'м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская',\
                     'м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m4
        if metro in ['м.Фрунзенская','м.Обходной канал','м.Звенигородская','м.Черная река','м.Международный','м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая',\
                     'м.Новочеркасская','м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая','м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская',\
                     'м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m5
        if metro in ['м.Звенигородская','м.Черная река','м.Международный','м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская',\
                     'м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая','м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь',\
                     'м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m6
        if metro in ['м.Черная река','м.Международный','м.Площадь Александра Невского','м.Политехнический','м.Приморская','м.Садовая','м.Новочеркасская',\
                     'м.Площадь Восстания','м.Лиговский проспект','м.Гостиный двор','м.Беговая','м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская',\
                     'м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская',\
                     'м.Чернышевская','м.Крестовский остров']:
            result += modelob.m7
        if metro in ['м.Маяковская','м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская',\
                     'м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m8
        if metro in ['м.Выборгская','м.Владимирская','м.Петроградская','м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект',\
                     'м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m9
        if metro in ['м.Сенная площадь','м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская',\
                     'м.Чернышевская','м.Крестовский остров']:
            result += modelob.m10
        if metro in ['м.Балтийская','м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m11
        if metro in ['м.Спорт','м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m12
        if metro in ['м.Достоевская','м.Чкаловская','м.Невский проспект','м.Адмиралтейская','м.Площадь Ленина','м.Горьковская','м.Чернышевская','м.Крестовский остров']:
            result += modelob.m13
        if metro in ['м.Чернышевская','м.Крестовский остров']:
            result += modelob.m14
        if metro in ['м.Крестовский остров']:
            result += modelob.m15
        result += modelob.s1 * square + modelob.c1
        context = {
            'result': result,
            'room': room,
            'metro': metro,
            'square': square
        }
        return render(request, 'predict.html', context=context)