from django.db import models
from django.utils.timezone import now

# Create your models here.


MATCH_TYPE = (
    (0, u'男单'),
    (1, u'女单'),
    (2, u'男双'),
    (3, u'女双'),
    (4, u'混双')
)


class AthleteInfo(models.Model):
    objects = None
    GENDER = (
        (0, u'男'),
        (1, u'女'),
    )

    SPORT_LEVEL = (
        (0, u'特级'),
        (1, u'一级'),
        (2, u'二级'),
        (3, u'三级'),
        (4, u'四级'),
        (5, u'五级'),
        (6, u'六级'),
        (7, u'七级'),
        (8, u'八级'),
    )

    STATE = (
        (0, u'启用'),
        (1, u'删除'),
        (2, u'禁用')
    )

    HAND_HELD = (
        (0, u'右手'),
        (1, u'左手'),
    )

    athlete_id = models.CharField(max_length=32, unique=True)
    company_id = models.CharField(max_length=32, default='', db_index=True)
    name = models.CharField(max_length=64, db_index=True)
    english_name = models.CharField(max_length=64, db_index=True, default='')
    gender = models.IntegerField(choices=GENDER, default=0)
    profile_photo = models.ImageField(max_length=128, upload_to="clubstatic/img/athlete",
                                      default='clubstatic/img/athlete/default-photo.png')
    nationality = models.CharField(max_length=32, default='')
    native_place = models.CharField(max_length=255, default='')
    folk = models.CharField(max_length=32, default='汉族')
    birthday = models.DateTimeField(blank=True, null=True)
    sport_project = models.CharField(max_length=32)
    hand_held = models.IntegerField(choices=HAND_HELD, default=0)
    sport_level = models.IntegerField(choices=SPORT_LEVEL)
    initial_training_time = models.DateTimeField(blank=True, null=True)
    first_coach = models.CharField(max_length=64, default='')
    pro_team_coach = models.CharField(max_length=64, default='')
    nat_team_coach = models.CharField(max_length=64, default='')
    state = models.IntegerField(choices=STATE, default=0)
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'athlete_info'


class MatchInfo(models.Model):

    objects = None
    MATCH_RESULT = (
        (1, u'胜'),
        (2, u'负'),
    )

    match_id = models.CharField(unique=True, max_length=32)
    level1 = models.CharField(max_length=32, default='')
    level2 = models.CharField(max_length=32, default='')
    match_type = models.IntegerField(choices=MATCH_TYPE, default=0)
    match_name = models.CharField(max_length=128, db_index=True)
    match_date = models.DateTimeField(blank=True, null=True)
    player_a = models.CharField(max_length=32, db_index=True)
    player_a_id = models.CharField(max_length=128, db_index=True)
    player_b = models.CharField(max_length=32, db_index=True)
    player_b_id = models.CharField(max_length=128, db_index=True)
    winnum_a = models.IntegerField(default=0)
    winnum_b = models.IntegerField(default=0)
    match_result = models.IntegerField(choices=MATCH_RESULT)
    match_round = models.CharField(max_length=32, default='')
    memo = models.CharField(max_length=2048, default='')
    created_at = models.DateTimeField(default=now)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'match_info'
