import logging
from contextlib import contextmanager
from decimal import Decimal
from typing import Optional
from urllib.parse import urljoin

import stripe
from django.urls import reverse
from stripe.error import AuthenticationError, InvalidRequestError, StripeError
from stripe.stripe_object import StripeObject

from ....core.tracing import opentracing_trace
from ....core.utils import build_absolute_uri, get_domain
from ...interface import PaymentMethodInfo
from ...utils import price_to_minor_unit
from .consts import (
    AUTOMATIC_CAPTURE_METHOD,
    MANUAL_CAPTURE_METHOD,
    METADATA_IDENTIFIER,
    PLUGIN_ID,
    STRIPE_API_VERSION,
    WEBHOOK_EVENTS,
    WEBHOOK_PATH,
)

logger = logging.getLogger(__name__)


stripe.api_version = STRIPE_API_VERSION


@contextmanager
def stripe_opentracing_trace(span_name):
    with opentracing_trace(
        span_name=span_name, component_name="payment", service_name="stripe"
    ):
        yield


def is_secret_api_key_valid(api_key: str):
    """Call api to check if api_key is a correct key."""
    try:
        with stripe_opentracing_trace("stripe.WebhookEndpoint.list"):
            stripe.WebhookEndpoint.list(api_key)
        return True
    except AuthenticationError:
        return False


def _extra_log_data(error: StripeError, payment_intent_id: Optional[str] = None):
    data = {
        "error_message": error.user_message,
        "http_status": error.http_status,
        "code": error.code,
    }
    if payment_intent_id is not None:
        data["payment_intent_id"] = payment_intent_id
    return data


def subscribe_webhook(api_key: str, channel_slug: str) -> Optional[StripeObject]:
    domain = get_domain()
    api_path = reverse(
        "plugins-per-channel",
        kwargs={"plugin_id": PLUGIN_ID, "channel_slug": channel_slug},
    )

    base_url = build_absolute_uri(api_path)
    webhook_url = urljoin(base_url, WEBHOOK_PATH)

    with stripe_opentracing_trace("stripe.WebhookEndpoint.create"):
        try:
            return stripe.WebhookEndpoint.create(
                api_key=api_key,
                url=webhook_url,
                enabled_events=WEBHOOK_EVENTS,
                metadata={METADATA_IDENTIFIER: domain},
            )
        except StripeError as error:
            logger.warning(
                "Failed to create Stripe webhook",
                extra=_extra_log_data(error),
            )
            return None


def delete_webhook(api_key: str, webhook_id: str):
    try:
        with stripe_opentracing_trace("stripe.WebhookEndpoint.delete"):
            stripe.WebhookEndpoint.delete(
                webhook_id,
                api_key=api_key,
            )
    except InvalidRequestError:
        # webhook doesn't exist
        pass


def get_or_create_customer(
    api_key: str,
    customer_id: Optional[str] = None,
    customer_email: Optional[str] = None,
) -> Optional[StripeObject]:
    try:
        if customer_id:
            with stripe_opentracing_trace("stripe.Customer.retrieve"):
                return stripe.Customer.retrieve(
                    customer_id,
                    api_key=api_key,
                )
        with stripe_opentracing_trace("stripe.Customer.create"):
            return stripe.Customer.create(
                api_key=api_key,
                email=customer_email,
            )
    except StripeError as error:
        logger.warning(
            "Failed to get/create Stripe customer",
            extra=_extra_log_data(error),
        )
        return None


def create_payment_intent(
    api_key: str,
    amount: Decimal,
    currency: str,
    auto_capture: bool = True,
    customer: Optional[StripeObject] = None,
    payment_method_id: Optional[str] = None,
    metadata: Optional[dict] = None,
    setup_future_usage: Optional[str] = None,
    off_session: Optional[bool] = None,
    payment_method_types: Optional[List[str]] = None,
    automatic_payment_methods: Optional[dict] = None,
    return_url:Optional[str] = None,
    confirm:Optional[str] = None,
    customer_email: Optional[str] = None,
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    capture_method = AUTOMATIC_CAPTURE_METHOD if auto_capture else MANUAL_CAPTURE_METHOD
    additional_params = {}

    if customer:
        additional_params["customer"] = customer

    if payment_method_id and customer:
        additional_params["payment_method"] = payment_method_id

        additional_params["off_session"] = off_session if off_session else False
        if off_session:
            additional_params["confirm"] = True

    if setup_future_usage in ["on_session", "off_session"] and not payment_method_id:
        additional_params["setup_future_usage"] = setup_future_usage

    if metadata:
        additional_params["metadata"] = metadata

    if payment_method_types and isinstance(payment_method_types, list):
        additional_params["payment_method_types"] = payment_method_types

    if automatic_payment_methods and isinstance(automatic_payment_methods, dict):
        additional_params["automatic_payment_methods"] = automatic_payment_methods

    if customer_email:
        additional_params["receipt_email"] = customer_email

    if return_url:
        additional_params["return_url"] = return_url

    if confirm:
        additional_params["confirm"] = confirm

    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.create"):
            intent = stripe.PaymentIntent.create(
                api_key=api_key,
                amount=price_to_minor_unit(amount, currency),
                currency=currency,
                capture_method=capture_method,
                **additional_params,
            )
        return intent, None
    except StripeError as error:
        logger.warning(
            "Failed to create Stripe payment intent", extra=_extra_log_data(error)
        )
        return None, error


def update_payment_method(
    api_key: str,
    payment_method_id: str,
    metadata: dict[str, str],
):
    with stripe_opentracing_trace("stripe.PaymentMethod.modify"):
        try:
            stripe.PaymentMethod.modify(
                payment_method_id,
                api_key=api_key,
                metadata=metadata,
            )
        except StripeError as error:
            logger.warning(
                "Failed to assign channel slug to payment method",
                extra=_extra_log_data(error),
            )


def list_customer_payment_methods(
    api_key: str, customer_id: str
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentMethod.list"):
            payment_methods = stripe.PaymentMethod.list(
                api_key=api_key,
                customer=customer_id,
                type="card",  # we support only cards for now
            )
        return payment_methods, None
    except StripeError as error:
        return None, error


def retrieve_payment_intent(
    api_key: str, payment_intent_id: str
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.retrieve"):
            payment_intent = stripe.PaymentIntent.retrieve(
                payment_intent_id,
                api_key=api_key,
            )
        return payment_intent, None
    except StripeError as error:
        logger.warning(
            "Unable to retrieve a payment intent",
            extra=_extra_log_data(error),
        )
        return None, error


def capture_payment_intent(
    api_key: str, payment_intent_id: str, amount_to_capture: int
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.capture"):
            payment_intent = stripe.PaymentIntent.capture(
                payment_intent_id,
                amount_to_capture=amount_to_capture,
                api_key=api_key,
            )
        return payment_intent, None
    except StripeError as error:
        logger.warning(
            "Unable to capture a payment intent",
            extra=_extra_log_data(error),
        )
        return None, error


def modify_payment_intent(
    api_key: str,
    payment_intent_id: str,
    payment_method:Optional[str]
) -> Tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.retrieve"):
            payment_intent = stripe.PaymentIntent.modify(
                payment_intent_id,
                api_key=api_key,
                payment_method=payment_method,
            )
        return payment_intent, None
    except StripeError as error:
        logger.warning(
            "Unable to modify a payment intent",
            extra=_extra_log_data(error),
        )
        return None, error

def refund_payment_intent(
    api_key: str, payment_intent_id: str, amount_to_refund: int
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.Refund.create"):
            refund = stripe.Refund.create(
                payment_intent=payment_intent_id,
                amount=amount_to_refund,
                api_key=api_key,
            )
        return refund, None
    except StripeError as error:
        logger.warning(
            "Unable to refund a payment intent",
            extra=_extra_log_data(error),
        )
        return None, error


def cancel_payment_intent(
    api_key: str, payment_intent_id: str
) -> tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.cancel"):
            payment_intent = stripe.PaymentIntent.cancel(
                payment_intent_id,
                api_key=api_key,
            )
        return payment_intent, None
    except StripeError as error:
        logger.warning(
            "Unable to cancel a payment intent",
            extra=_extra_log_data(error),
        )

        return None, error


def construct_stripe_event(
    api_key: str, payload: bytes, sig_header: str, endpoint_secret: str
) -> StripeObject:
    with stripe_opentracing_trace("stripe.Webhook.construct_event"):
        return stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret, api_key=api_key
        )


def get_payment_method_details(
    payment_intent: StripeObject,
) -> Optional[PaymentMethodInfo]:
    charges = payment_intent.get("charges", None)
    payment_method_info = None
    if charges:
        charges_data = charges.get("data", [])
        if not charges_data:
            return None
        charge_data = charges_data[-1]
        payment_method_details = charge_data.get("payment_method_details", {})

        if payment_method_details.get("type") == "card":
            card_details = payment_method_details.get("card", {})
            exp_year = card_details.get("exp_year", "")
            exp_year = int(exp_year) if exp_year else None
            exp_month = card_details.get("exp_month", "")
            exp_month = int(exp_month) if exp_month else None
            payment_method_info = PaymentMethodInfo(
                last_4=card_details.get("last4", ""),
                exp_year=exp_year,
                exp_month=exp_month,
                brand=card_details.get("brand", ""),
                type="card",
            )
    return payment_method_info

def confirm_payment(
    api_key: str, payment_intent_id: str, payment_method: str, return_url: Optional[str]
) -> Tuple[Optional[StripeObject], Optional[StripeError]]:
    try:
        with stripe_opentracing_trace("stripe.PaymentIntent.confirm"):
            payment_intent = stripe.PaymentIntent.confirm(
                payment_intent_id,
                api_key=api_key,
                payment_method=payment_method,
                return_url=return_url
            )
        return payment_intent, None
    except StripeError as error:
        logger.warning(
            "Unable to confirm a payment intent",
            extra=_extra_log_data(error),
        )
        return None, error
