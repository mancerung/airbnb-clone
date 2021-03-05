from django.contrib import admin
from django.utils.html import mark_safe
from . import models


@admin.register(models.RoomType, models.Facility, models.Amenity, models.HouseRule)
class ItemAdmin(admin.ModelAdmin):
    """ Item Admin Definition """

    list_display = ("name", "used_by")

    def used_by(self, obj):
        return obj.rooms.count()


# class PhotoInline(admin.StackedInline):
class PhotoInline(admin.TabularInline):
    model = models.Photo


@admin.register(models.Room)
class RoomAdmin(admin.ModelAdmin):
    """ Room Admin Definition """

    # ModelAdmin은 모델이 외부에서 보여지는 방식 변경가능 1.리스트(list_display) 2.내부(=개별상세, fields)
    list_display = (
        "name",
        "country",
        "city",
        "price",
        "address",
        "guests",
        "beds",
        "bedrooms",
        "baths",
        "check_in",
        "check_out",
        "instant_book",
        "count_amenities",
        "count_photos",
        "total_rating",
    )
    # ordering = ("name", "price")

    list_filter = (
        "instant_book",
        "host__superhost",
        "room_type",
        "amenities",
        "facilities",
        "house_rules",
        "city",
        "country",
    )

    search_fields = ("city", "^host__username")
    # "^city",  # startwith   =iexact
    # 디폴트 : icontains 대소문자 구별X
    # 아래목록을 or 조건으로 검색함

    fieldsets = (
        (
            "Basic Info",
            {
                "fields": (
                    "name",
                    "description",
                    "country",
                    "city",
                    "address",
                    "price",
                    "room_type",
                )
            },
        ),
        (
            "Times",
            {"fields": ("check_in", "check_out", "instant_book")},
        ),
        (
            "Spaces",
            {"fields": ("guests", "beds", "bedrooms", "baths")},
        ),
        (
            "More About the Space",
            # 아래와 같이하면 접을 수 있다
            # {
            #     "classes": ("collapse",),
            #     "fields": ("amenities", "facilities", "house_rules"),
            # },
            {"fields": ("amenities", "facilities", "house_rules")},
        ),
        (
            "Last Details",
            {"fields": ("host",)},
        ),
    )
    # fields = ("country",) #상세에서 보여줄 목록

    filter_horizontal = ("amenities", "facilities", "house_rules")

    # admin 패널 안에 admin 패널을 넣는다.
    # raw_id_fields = ("amenities",)
    raw_id_fields = ("host",)

    inlines = (PhotoInline,)

    def count_amenities(self, obj):
        return obj.amenities.count()
        # self는 클래스, obj는 현재 row

    count_amenities.short_description = "Amenity Count"
    # count_amenities.short_description = "hello~"

    def count_photos(self, obj):
        return obj.photos.count()

    count_photos.short_description = "Photo Count"
    # def save_model(self, request, obj, form, change):
    #     print(obj, change, form)
    #     # send_mail() 활용 예
    #     # obj.user = request.user user 가져와서 저장해도 되는지 판단,기록
    #     super().save_model(request, obj, form, change)


@admin.register(models.Photo)
class PhotoAdmin(admin.ModelAdmin):
    """ Photo Admin Definition """

    list_display = ("__str__", "get_thumbnail")

    def get_thumbnail(self, obj):
        # obj.file string이 아니고 클래스다. print해보자.
        # print(dir(obj.file))
        return mark_safe(f'<img width="50px" src="{obj.file.url}" />')
        # 태그 사용하려면 보안설정해야한다

    get_thumbnail.short_description = "Thumbnail"
