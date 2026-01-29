from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": _("مربع"),
    "SHOW_LANGUAGES": False,
    "SITE_HEADER": _("مربع"),
    "SITE_SUBHEADER": _("پنل مدیریت محتوا وبسایت"),
    "SITE_URL": "/admin/",  # "#"
    "SITE_ICON": "/static/logo/morabe.png",

    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/svg+xml",
            "href": lambda request: static("favicon.svg"),
        },
    ],

    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "SHOW_BACK_BUTTON": False,

    "DASHBOARD_CALLBACK": "morabe.unfold_settings.dashboard_callback",

    "STYLES": [
        lambda request: static("unfold/css/style.css"),
    ],
    "SCRIPTS": [
        lambda request: static("unfold/js/script.js"),
    ],
    "BORDER_RADIUS": "6px",

    # "EXTENSIONS": {
    #     "modeltranslation": {
    #         "flags": {
    #             "fa": "🇮🇷",
    #             "en": "🇬🇧",
    #         },
    #     },
    # },

    # "SITE_DROPDOWN": [
    #     {
    #         "icon": "diamond",
    #         "title": " خانه",
    #         "link": "/en/admin",
    #     },
    # ],

    "SIDEBAR": {
        "show_search": True,
        "command_search": False,
        "show_all_applications": True,
        "navigation": [
            {
                "title": _("بلاگ"),
                "separator": True,
                "collapsible": True,
                "icon": "article",
                "items": [
                    {"title": _("پست‌ها"), "link": reverse_lazy("admin:blog_blog_changelist"), "icon": "article"},
                    {"title": _("نظرات"), "link": reverse_lazy("admin:blog_blogcomment_changelist"), "icon": "comment"},
                ]
            },
            {
                "title": _("نواحی جغرافیایی"),
                "separator": True,
                "collapsible": True,
                "icon": "map",
                "items": [
                    {"title": _("استان‌ها"), "link": reverse_lazy("admin:areas_province_changelist"), "icon": "location_city"},
                    {"title": _("شهرها"), "link": reverse_lazy("admin:areas_city_changelist"), "icon": "place"},
                ]
            },
            {
                "title": _("کاربران"),
                "separator": True,
                "collapsible": True,
                "icon": "people",
                "items": [
                    {"title": _("کاربران"), "link": reverse_lazy("admin:account_user_changelist"), "icon": "person"},
                    {"title": _("کدهای یکبارمصرف"), "link": reverse_lazy("admin:account_otpcode_changelist"), "icon": "key"},
                ]
            },
            {
                "title": _("تماس با ما"),
                "separator": True,
                "collapsible": True,
                "icon": "mail",
                "items": [
                    {"title": _("پیام‌ها"), "link": reverse_lazy("admin:contact_us_contactusmessages_changelist"), "icon": "email"},
                ]
            },
            {
                "title": _("سازندگان"),
                "separator": True,
                "collapsible": True,
                "icon": "business",
                "items": [
                    {"title": _("سازندگان"), "link": reverse_lazy("admin:contractor_contractor_changelist"), "icon": "business_center"},
                    # {"title": _("گالری"), "link": reverse_lazy("admin:contractor_gallery_changelist"), "icon": "photo_library"},
                    {"title": _("درخواست‌های همکاری"), "link": reverse_lazy("admin:contractor_registrationcontractor_changelist"), "icon": "handshake"},
                ]
            },
            {
                "title": _("سرمایه‌گذاری"),
                "separator": True,
                "collapsible": True,
                "icon": "trending_up",
                "items": [
                    {"title": _("سرمایه‌گذاری‌ها"), "link": reverse_lazy("admin:investments_investment_changelist"), "icon": "attach_money"},
                    {"title": _("فروش سرمایه‌گذاری"), "link": reverse_lazy("admin:investments_investmentsale_changelist"), "icon": "sell"},
                ]
            },
            {
                "title": _("پرداخت‌ها"),
                "separator": True,
                "collapsible": True,
                "icon": "payments",
                "items": [
                    {"title": _("کیف‌پول"), "link": reverse_lazy("admin:payment_wallet_changelist"), "icon": "account_balance_wallet"},
                    {"title": _("کارت‌های اعتباری"), "link": reverse_lazy("admin:payment_creditcard_changelist"), "icon": "credit_card"},
                    {"title": _("تراکنش‌ها"), "link": reverse_lazy("admin:payment_transaction_changelist"), "icon": "receipt"},
                    {"title": _("درخواست‌های برداشت"), "link": reverse_lazy("admin:payment_withdrawrequest_changelist"), "icon": "money_off"},
                ]
            },
            {
                "title": _("پروژه‌ها"),
                "separator": True,
                "collapsible": True,
                "icon": "construction",
                "items": [
                    {"title": _("پروژه‌ها"), "link": reverse_lazy("admin:project_project_changelist"), "icon": "folder"},
                    {"title": _("وضعیت پروژه‌ها"), "link": reverse_lazy("admin:project_projectstatus_changelist"), "icon": "timeline"},
                    # {"title": _("گالری"), "link": reverse_lazy("admin:project_gallery_changelist"), "icon": "collections"},
                    # {"title": _("گزارش پیشرفت"), "link": reverse_lazy("admin:project_projectprogressreport_changelist"), "icon": "assessment"},
                    # {"title": _("اسناد پروژه"), "link": reverse_lazy("admin:project_projectdocuments_changelist"), "icon": "description"},
                ]
            },
            {
                "title": _("سوالات متداول"),
                "separator": True,
                "collapsible": True,
                "icon": "help",
                "items": [
                    {"title": _("دسته‌بندی‌ها"), "link": reverse_lazy("admin:questions_category_changelist"), "icon": "category"},
                    {"title": _("سوالات"), "link": reverse_lazy("admin:questions_faq_changelist"), "icon": "question_answer"},
                ]
            },
            {
                "title": _("قوانین و مقررات"),
                "separator": True,
                "collapsible": True,
                "icon": "gavel",
                "items": [
                    {"title": _("قوانین"), "link": reverse_lazy("admin:rules_rules_changelist"), "icon": "policy"},
                ]
            },
            {
                "title": _("تنظیمات سایت"),
                "separator": True,
                "collapsible": True,
                "icon": "settings",
                "items": [
                    {"title": _("تنظیمات عمومی"), "link": reverse_lazy("admin:settings_siteglobalsetting_changelist"), "icon": "tune"},
                    {"title": _("شبکه‌های اجتماعی"), "link": reverse_lazy("admin:settings_socialmediasetting_changelist"), "icon": "share"},
                ]
            },
        ],
    },


    # "TABS": [
    #     {
    #         "models": ["project.project"],
    #         "items": [
    #             {
    #                 "title": _("اطلاعات پایه"),
    #                 "icon": "info",
    #                 "fields": [
    #                     "title",
    #                     "contractors",
    #                     "usage_type",
    #                     "status",
    #                     "is_featured",
    #                     "slug"
    #                 ]
    #             },
    #             {
    #                 "title": _("موقعیت مکانی"),
    #                 "icon": "location_on",
    #                 "fields": [
    #                     "province",
    #                     "city",
    #                     "address",
    #                     "map"
    #                 ]
    #             },
    #             {
    #                 "title": _("متراژ و قیمت"),
    #                 "icon": "attach_money",
    #                 "fields": [
    #                     "price_per_meter",
    #                     "total_area",
    #                     "usable_area",
    #                     "complete_area",
    #                     "investable_area",
    #                     "display_sold_area_readonly",
    #                     "display_remaining_area_readonly"
    #                 ]
    #             },
    #             {
    #                 "title": _("مشخصات فیزیکی"),
    #                 "icon": "home",
    #                 "fields": [
    #                     "floor_count",
    #                     "unit_count",
    #                     "bedroom_count",
    #                     "parking_count",
    #                     "warehouse_count"
    #                 ]
    #             },
    #             {
    #                 "title": _("زمان‌بندی"),
    #                 "icon": "calendar_today",
    #                 "fields": [
    #                     "start_date",
    #                     "estimated_completion_date"
    #                 ]
    #             },
    #             {
    #                 "title": _("مالی و سرمایه"),
    #                 "icon": "trending_up",
    #                 "fields": [
    #                     "profit_to_date",
    #                     "invest_start_from",
    #                     "total_budget",
    #                     "current_funding"
    #                 ]
    #             },
    #             {
    #                 "title": _("توضیحات"),
    #                 "icon": "description",
    #                 "fields": ["project_details"]
    #             },
    #             {
    #                 "title": _("SEO"),
    #                 "icon": "search",
    #                 "fields": [
    #                     "meta_title",
    #                     "meta_description",
    #                     "meta_keywords"
    #                 ]
    #             },
    #             {
    #                 "title": _("تاریخ‌ها"),
    #                 "icon": "history",
    #                 "fields": ["created", "modified"]
    #             }
    #         ]
    #     }
    # ]
}



DATA = {
    "headers": [
        # Col 1 header
        {
            "title": "Title",
            "subtitle": "something",  # Optional
        },
    ],
    "rows": [
        # First row
        {
            # Row heading
            "header": {
                "title": "Title",
                "subtitle": "something",  # Optional
            },
            "cols": [
                # Col 1 cell value
                {
                    "value": "1",
                    "subtitle": "something",  # Optional
                }
            ]
        },
        # Second row
        {
            # Row heading
            "header": {
                "title": "Title",
                "subtitle": "something",  # Optional
            },
            "cols": [
                # Col 1 cell value
                {
                    "value": "1",
                }
            ]
        },
    ]
}


def dashboard_callback(request, context):
    """
    Callback to prepare custom variables for index template which is used as dashboard
    template. It can be overridden in application by creating custom admin/index.html.
    """
    context.update(
        {
            "my_data_variable": DATA,  # this will be injected into templates/admin/index.html
        }
    )
    return context


def environment_callback(request):
    """
    Callback has to return a list of two values represeting text value and the color
    type of the label displayed in top right corner.
    """
    return ["Production", "danger"]


def badge_callback(request):
    return 3


