"""
Implementation of the PayPal REST API

To enable this implementation, add the following Django settings:

    CC_PROCESSOR_NAME = "PayPal"
    CC_PROCESSOR = {
        "PayPal": {
            "CLIENT_SECRET": "<client_secret>",
            "CLIENT_ID": "<client_id>",
            "PURCHASE_ENDPOINT": "/shoppingcart/paypal/payment/"
        }
    }

"""

import json
import uuid
import logging
from datetime import datetime
from collections import OrderedDict

from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _
import paypalrestsdk
from paypalrestsdk import Payment

from edxmako.shortcuts import render_to_response
from edxmako.shortcuts import render_to_string
from shoppingcart.models import Order
from shoppingcart.processors.exceptions import *
from shoppingcart.processors.helpers import get_processor_config
from microsite_configuration import microsite


log = logging.getLogger(__name__)

paypalrestsdk.configure({
    "mode": get_processor_config().get('MODE', ''),
    "client_id": get_processor_config().get('CLIENT_ID', ''),
    "client_secret": get_processor_config().get('CLIENT_SECRET', '')})


def make_payment(request):
    if request.POST:

        return_url = request.POST.get('override_custom_receipt_page', '')
        price = request.POST.get('amount', '')
        course_id = request.POST.get('course_id', 'ProSky Course')
        cancel_url = request.build_absolute_uri(
            reverse("paypal_cancel")
        )

        # Payment
        # A Payment Resource; create one using
        # the above types and intent as 'sale'
        payment = Payment({
            "intent": "sale",

            # Payer
            # A resource representing a Payer that funds a payment
            # Payment Method as 'paypal'
            "payer": {
                "payment_method": "paypal"},

            # Redirect URLs
            "redirect_urls": {
                "return_url": return_url,
                "cancel_url": cancel_url},

            # Transaction
            # A transaction defines the contract of a
            # payment - what is the payment for and who
            # is fulfilling it.
            "transactions": [{

                     # ItemList
                     "item_list": {
                         "items": [{
                                       "name": course_id,
                                       "sku": course_id,
                                       "price": price,
                                       "currency": "USD",  # always USD for now
                                       "quantity": 1}]},
                     # always one, we can only purchase one course at a time for now

                     # Amount
                     # Let's you specify a payment amount.
                     "amount": {
                         "total": price,  # total cost should be 1 x unit cost
                         "currency": "USD"},
                     "description": "ProSky Paid Course Registration"}]})

        redirect_url = ''
        payment_id = ''
        success = False
        error = ''
        # Create Payment and return status
        if payment.create():
            log.info("Payment[%s] created successfully" % payment.id)
            payment_id = payment.id
            # Redirect the user to given approval url
            for link in payment.links:
                if link.method == "REDIRECT":
                    # Convert to str to avoid google appengine unicode issue
                    # https://github.com/paypal/rest-api-sdk-python/pull/58
                    redirect_url = str(link.href)
                    log.info("Redirect for approval: %s" % redirect_url)
                    success = True
        else:
            log.info("Error while creating payment:")
            log.info(payment.error)
            error = payment.error
            success = False

    context = {
        'redirect_url': redirect_url,
        'success': success,
        'payment_id': payment_id,
        'error': error
    }

    return render_to_response('shoppingcart/paypal_confirm.html', context)


def execute_payment(params):
    """
    Execute Paypal authorized payment
    :param params: call back url
    :return: Dictionary containing execution result and payment id
    """

    result = {
        'success': False,
        'payment_id': '',
    }
    try:
        payment_id = params['paymentId']
        payer_id = params['PayerID']

        # ID of the payment. This ID is provided when creating payment.
        payment = Payment.find(payment_id)

        # PayerID is required to approve the payment.
        if payment.execute({"payer_id": payer_id}):  # return True or False
            log.info("Payment[%s] execute successfully" % payment.id)
            result['payment_id'] = payment.id
            result['create_time'] = payment.create_time
            result['payer'] = payment.payer
            result['transactions'] = payment.transactions
            result['state'] = payment.state
            result['success'] = True
        else:
            log.info(payment.error)
            result['success'] = False
    except Exception:
        result['success'] = False

    return result


def process_postpay_callback(params):
    """
    Handle a response from the payment processor.
    """

    try:
        order_id = params['ordernum']
        order = Order.objects.get(id=order_id)
        result = execute_payment(params)

        if result['success']:
            _record_purchase(result, order)
            return {
                'success': True,
                'order': order,
                'error_html': ''
            }
        else:
            return {
                'success': False,
                'order': order,
                'error_html': ''  # _get_processor_decline_html(params)
            }
    except KeyError, Order.DoesNotExist:
        raise CCProcessorDataException(_("The payment processor accepted an order whose number is not in our system."))
    except CCProcessorException as error:
        log.exception('error processing PayPal postpay callback')
        # if we have the order and the id, log it
        if hasattr(error, 'order'):
            _record_payment_info(result, error.order)
        else:
            log.info(json.dumps(result))
        return {
            'success': False,
            'order': None,  # due to exception we may not have the order
            'error_html': ''  # _get_processor_exception_html(error)
        }


def _get_processor_decline_html(params):
    """
    Return HTML indicating that the user's payment was declined.

    Args:
        params (dict): Parameters we received from CyberSource.

    Returns:
        unicode: The rendered HTML.

    """
    payment_support_email = microsite.get_value('payment_support_email', settings.PAYMENT_SUPPORT_EMAIL)
    return _format_error_html(
        _(
            "Sorry! Our payment processor did not accept your payment.  "
            "The decision they returned was {decision}, "
            "and the reason was {reason}.  "
            "You were not charged. Please try a different form of payment.  "
            "Contact us with payment-related questions at {email}."
        ).format(
            decision='<span class="decision">{decision}</span>'.format(decision=params['decision']),
            reason='<span class="reason">{reason_code}:{reason_msg}</span>'.format(
                reason_code=params['reason_code'],
                reason_msg=REASONCODE_MAP.get(params['reason_code'])
            ),
            email=payment_support_email
        )
    )


def render_purchase_form_html(cart, callback_url=None, extra_data=None):
    """
    Renders the HTML of the hidden POST form that must be used to initiate a purchase with CyberSource

    Args:
        cart (Order): The order model representing items in the user's cart.

    Keyword Args:
        callback_url (unicode): The URL that CyberSource should POST to when the user
            completes a purchase.  If not provided, then CyberSource will use
            the URL provided by the administrator of the account
            (CyberSource config, not LMS config).

        extra_data (list): Additional data to include as merchant-defined data fields.

    Returns:
        unicode: The rendered HTML form.

    """

    return render_to_string('shoppingcart/paypal_form.html', {
        'action': get_purchase_endpoint(),
        'params': get_signed_purchase_params(
            cart, callback_url=callback_url, extra_data=None
        ),
    })


def get_signed_purchase_params(cart, callback_url=None, extra_data=None):
    """
    This method will return a digitally signed set of Paypal parameters

    Args:
        cart (Order): The order model representing items in the user's cart.

    Keyword Args:
        callback_url (unicode): The URL that Paypal should POST to when the user
            completes a purchase.  If not provided, then Paypal will use
            the URL provided by the administrator of the account
            (Paypal config, not LMS config).

        extra_data (list): Additional data to include as merchant-defined data fields.

    Returns:
        dict

    """
    return get_purchase_params(cart, callback_url=callback_url, extra_data=extra_data)


def get_purchase_params(cart, callback_url=None, extra_data=None):
    """
    This method will build out a dictionary of parameters needed by Paypal to complete the transaction

    Args:
        cart (Order): The order model representing items in the user's cart.

    Keyword Args:
        callback_url (unicode): The URL that Paypal should POST to when the user
            completes a purchase.  If not provided, then Paypal will use
            the URL provided by the administrator of the account
            (Paypal config, not LMS config).

        extra_data (list): Additional data to include as merchant-defined data fields.

    Returns:
        dict

    """
    total_cost = cart.total_cost
    amount = "{0:0.2f}".format(total_cost)
    params = OrderedDict()

    params['amount'] = amount
    params['currency'] = cart.currency
    params['orderNumber'] = "OrderId: {0:d}".format(cart.id)

    params['reference_number'] = cart.id

    params['locale'] = 'en'
    params['signed_date_time'] = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%SZ')
    params['transaction_uuid'] = uuid.uuid4().hex
    params['payment_method'] = 'paypal'
    params['total_cost'] = cart.total_cost
    params['override_custom_receipt_page'] = callback_url
    params['override_custom_cancel_page'] = callback_url

    # Get course Id, should only be one
    cart_items = cart.orderitem_set.all().select_subclasses()
    for cart_item in cart_items:
        course_key = getattr(cart_item, 'course_id', None)
        if course_key is not None:
            params['course_id'] = course_key
            break

    return params


def get_purchase_endpoint():
    """
    Return the URL of the payment end-point for CyberSource.

    Returns:
        unicode

    """
    return get_processor_config().get('PURCHASE_ENDPOINT', '')


def _record_purchase(params, order):
    """
    Record the purchase and run purchased_callbacks

    Args:
        params (dict): The parameters we received from CyberSource.
        order (Order): The order associated with this payment.

    Returns:
        None

    """

    payerInfo = params['payer']['payer_info']
    shippingAddress = payerInfo['shipping_address']

    order.purchase(
        first=getattr(payerInfo, 'first_name', ''),
        last=getattr(payerInfo, 'last_name', ''),
        street1=getattr(shippingAddress, 'line1', ''),
        street2=getattr(shippingAddress, 'line2', ''),
        city=getattr(shippingAddress, 'city', ''),
        state=getattr(shippingAddress, 'state', ''),
        postalcode=getattr(shippingAddress, 'postal_code', ''),
        country=getattr(shippingAddress, 'country_code', ''),
        cardtype='paypal',
        processor_reply_dump=params
    )


def _record_payment_info(params, order):
    """
    Record the purchase and run purchased_callbacks

    Args:
        params (dict): The parameters we received from CyberSource.

    Returns:
        None
    """
    order.processor_reply_dump = params
    order.save()


