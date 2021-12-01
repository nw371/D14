import datetime
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from .models import CategorySub, Post, Category
from .secda import admail


def notify_subscribers_publication(post_id):
    new_post = Post.objects.get(id=post_id)
    subject = f'Добавлена публикация tasks: {new_post.name} {new_post.date.strftime("%d %m %Y")}'
    print(f"ЭТО КАТЕГОРИЯ ----------------------------------------------- {new_post.category.values('id')}")
    dcat_id = [c['id'] for c in list(new_post.category.values('id'))]
    for cat_id in dcat_id:
        filtered_susbscrbrs = list(CategorySub.objects.filter(category_id=cat_id).values('subscriber_id__user__email'))
        list_of_subscribers = [d['subscriber_id__user__email'] for d in filtered_susbscrbrs if 'subscriber_id__user__email' in d]
        pub_updates = render_to_string('email/pub_updates.html', {'post': new_post, 'instance': new_post.id})
        send_updates(subject, pub_updates, list_of_subscribers)

def collect_weekly_articles():
    date_to_filter = datetime.date.today()-datetime.timedelta(days=7)
    print(date_to_filter)
    subject = "Обновления статей за неделю"

    for i in range(1,4):
        arts = Category.objects.filter(id=i, post__date__gte = date_to_filter).values("post__name", "post__id")
        wkly_updates = render_to_string('email/weekly_pubs.html', {'posts': arts })
        #выдираем названия статей категории 1 созданных/изменённых за последнюю неделю
        filtered_susbscrbrs = list(CategorySub.objects.filter(category_id=i).values('subscriber_id__user__email'))
        list_of_subscribers = [d['subscriber_id__user__email'] for d in filtered_susbscrbrs if 'subscriber_id__user__email' in d]
        # отправляем письмо
        send_updates(subject, wkly_updates, list_of_subscribers)

def send_updates(subject, pub_updates, list_of_subscribers):
    msg = EmailMultiAlternatives(
        subject=subject,
        # body=f'Уважаемый подписчик, в интересующих Вас категориях произошли изменения. Можете перейти по ссылке http://127.0.0.1:8000/news/{instance.id}',  # сообщение с кратким описанием
        from_email=admail,  # здесь указываете почту, с которой будете отправлять
        to=list_of_subscribers, # здесь список получателей. Например, секретарь, сам врач и т. д.
    )
    msg.attach_alternative(pub_updates, "text/html")
    msg.content_subtype = "html"
    print("BODY: ", msg.body)
    print("MESSAGE : ", msg.message())
    print(f"ЛИСТ АДРЕСАТОВ {list_of_subscribers}")
    msg.send()