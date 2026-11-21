
import random

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from faker import Faker

from blog.models import Article, Category, Tag


class Command(BaseCommand):
    help = "Генерирует тестовые статьи блога"

    def add_arguments(self, parser):
        parser.add_argument(
            "--articles",
            type=int,
            default=100_000
        )

        parser.add_argument(
            "--batch-size",
            type=int,
            default=2000
        )

    @transaction.atomic
    def handle(self, *args, **options):
        total = options["articles"]
        batch_size = options["batch_size"]

        if total < 1:
            raise CommandError("Количество статей должно быть больше нуля")

        if batch_size < 1:
            raise CommandError("Размер пакета должен быть больше нуля")

        fake = Faker("ru_RU")
        User = get_user_model()

        users = [
            User.objects.get_or_create(
                username=f"blog_seed_user_{i}"
            )[0]
            for i in range(20)
        ]

        Category.objects.bulk_create(
            [
                Category(
                    name=f"Рубрика {i}",
                    description=fake.sentence()
                )
                for i in range(1, 51)
            ],
            ignore_conflicts=True
        )

        Tag.objects.bulk_create(
            [
                Tag(name=f"Тег {i}")
                for i in range(1, 201)
            ],
            ignore_conflicts=True
        )

        categories = list(Category.objects.all())
        tags = list(Tag.objects.all())

        if not categories or len(tags) < 3:
            raise CommandError("Недостаточно рубрик или тегов")

        through = Article.tags.through
        created = 0

        for start in range(0, total, batch_size):
            size = min(batch_size, total - start)

            articles = Article.objects.bulk_create(
                [
                    Article(
                        title=fake.sentence(nb_words=6)[:200],
                        content=fake.text(max_nb_chars=1200),
                        status=random.choices(
                            ["published", "draft"],
                            weights=[8, 2]
                        )[0],
                        category=random.choice(categories),
                        author=random.choice(users),
                        view_count=random.randint(0, 5000)
                    )
                    for _ in range(size)
                ],
                batch_size=batch_size
            )

            tag_links = [
                through(
                    article_id=article.pk,
                    tag_id=tag.pk
                )
                for article in articles
                for tag in random.sample(tags, 3)
            ]

            through.objects.bulk_create(
                tag_links,
                batch_size=batch_size * 3
            )

            created += size

            self.stdout.write(
                f"Создано {created} из {total}"
            )

        self.stdout.write(
            self.style.SUCCESS(
                f"Генерация завершена. Создано статей: {created}"
            )
        )
