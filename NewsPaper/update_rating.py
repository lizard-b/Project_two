def update_rating(self):
    # Суммарный рейтинг каждой статьи автора умножается на 3
    post_ratings = self.post_set.aggregate(total_post_rating=Sum('post_rating'))['total_post_rating'] or 0
    post_rating = post_ratings * 3

    # Суммарный рейтинг всех комментариев автора
    comment_ratings = self.user.comment_set.aggregate(total_comment_rating=Sum('comment_rating'))[
                          'total_comment_rating'] or 0

    # Суммарный рейтинг всех комментариев к статьям автора
    post_comments_ratings = Comment.objects.filter(post_id__author_id=self).aggregate(total_post_comments_rating=Sum('comment_rating'))[
        'total_post_comments_rating'] or 0

    # Итоговый рейтинг автора
    self.user_rating = post_rating + comment_ratings + post_comments_ratings