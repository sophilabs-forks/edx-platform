from django.conf.urls import patterns, url
from django.conf import settings

urlpatterns = patterns('shoppingcart.views',  # nopep8
    url(r'^postpay_callback/$', 'postpay_callback'),  # Both the ~accept and ~reject callback pages are handled here
    url(r'^receipt/(?P<ordernum>[0-9]*)/$', 'show_receipt'),
    url(r'^csv_report/$', 'csv_report', name='payment_csv_report'),
)

if settings.FEATURES['ENABLE_SHOPPING_CART']:
    urlpatterns += patterns(
        'shoppingcart.views',
        url(r'^$', 'show_cart'),
        url(r'^clear/$', 'clear_cart'),
        url(r'^remove_item/$', 'remove_item'),
        url(r'^add/course/{}/$'.format(settings.COURSE_ID_PATTERN), 'add_course_to_cart', name='add_course_to_cart'),
        url(r'^use_code/$', 'use_code'),
        url(r'^register_courses/$', 'register_courses'),
    )

if settings.FEATURES.get('ENABLE_PAYMENT_FAKE'):
    from shoppingcart.tests.payment_fake import PaymentFakeView
    urlpatterns += patterns(
        'shoppingcart.tests.payment_fake',
        url(r'^payment_fake', PaymentFakeView.as_view()),
    )

#enabling paypal integration
urlpatterns += patterns('',
    url(r'^paypal/payment/$', 'shoppingcart.processors.PayPal.make_payment', name='paypal_payment'),
    url(r'^paypal_callback/cancel/', 'shoppingcart.views.paypal_cancel', name='paypal_cancel'),
    url(r'^paypal_callback/(?P<ordernum>[0-9]*)/', 'shoppingcart.views.paypal_callback', name='paypal_callback'),

)

