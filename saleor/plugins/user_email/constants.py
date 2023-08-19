import os

from django.conf import settings

PLUGIN_ID = "mirumee.notifications.user_email"


DEFAULT_EMAIL_TEMPLATES_PATH = os.path.join(
    settings.PROJECT_ROOT, "saleor/plugins/user_email/default_email_templates"
)

ACCOUNT_CONFIRMATION_TEMPLATE_FIELD = "account_confirmation"
ACCOUNT_COMPLETION_TEMPLATE_FIELD = "account_completion"
ACCOUNT_COMPLETION_EMAIL_NAME_FIELD = "account_completion_email_name"
ACCOUNT_COMPLETION_EMAIL_ADDRESS_FIELD = "account_completion_email_address"
ACCOUNT_SET_CUSTOMER_PASSWORD_TEMPLATE_FIELD = "account_set_customer_password"
ACCOUNT_DELETE_TEMPLATE_FIELD = "account_delete"
ACCOUNT_CHANGE_EMAIL_CONFIRM_TEMPLATE_FIELD = "account_change_email_confirm"
ACCOUNT_CHANGE_EMAIL_REQUEST_TEMPLATE_FIELD = "account_change_email_request"
ACCOUNT_PASSWORD_RESET_TEMPLATE_FIELD = "account_password_reset"
INVOICE_READY_TEMPLATE_FIELD = "invoice_ready"
ORDER_CONFIRMATION_TEMPLATE_FIELD = "order_confirmation"
ORDER_CONFIRMED_TEMPLATE_FIELD = "order_confirmed"
ORDER_FULFILLMENT_CONFIRMATION_TEMPLATE_FIELD = "order_fulfillment_confirmation"
ORDER_FULFILLMENT_UPDATE_TEMPLATE_FIELD = "order_fulfillment_update"
ORDER_PAYMENT_CONFIRMATION_TEMPLATE_FIELD = "order_payment_confirmation"
ORDER_CANCELED_TEMPLATE_FIELD = "order_canceled"
ORDER_REFUND_CONFIRMATION_TEMPLATE_FIELD = "order_refund_confirmation"
SEND_GIFT_CARD_TEMPLATE_FIELD = "send_gift_card"

TEMPLATE_FIELDS = [
    ACCOUNT_CONFIRMATION_TEMPLATE_FIELD,
    ACCOUNT_COMPLETION_TEMPLATE_FIELD,
    ACCOUNT_SET_CUSTOMER_PASSWORD_TEMPLATE_FIELD,
    ACCOUNT_DELETE_TEMPLATE_FIELD,
    ACCOUNT_CHANGE_EMAIL_CONFIRM_TEMPLATE_FIELD,
    ACCOUNT_CHANGE_EMAIL_REQUEST_TEMPLATE_FIELD,
    ACCOUNT_PASSWORD_RESET_TEMPLATE_FIELD,
    INVOICE_READY_TEMPLATE_FIELD,
    ORDER_CONFIRMATION_TEMPLATE_FIELD,
    ORDER_CONFIRMED_TEMPLATE_FIELD,
    ORDER_FULFILLMENT_CONFIRMATION_TEMPLATE_FIELD,
    ORDER_FULFILLMENT_UPDATE_TEMPLATE_FIELD,
    ORDER_PAYMENT_CONFIRMATION_TEMPLATE_FIELD,
    ORDER_CANCELED_TEMPLATE_FIELD,
    ORDER_REFUND_CONFIRMATION_TEMPLATE_FIELD,
    SEND_GIFT_CARD_TEMPLATE_FIELD,
]

ACCOUNT_CONFIRMATION_DEFAULT_TEMPLATE = "confirm.html"
ACCOUNT_COMPLETION_DEFAULT_TEMPLATE = "complete.html"
ACCOUNT_SET_CUSTOMER_PASSWORD_DEFAULT_TEMPLATE = "set_customer_password.html"
ACCOUNT_DELETE_DEFAULT_TEMPLATE = "account_delete.html"
ACCOUNT_CHANGE_EMAIL_CONFIRM_DEFAULT_TEMPLATE = "email_changed_notification.html"
ACCOUNT_CHANGE_EMAIL_REQUEST_DEFAULT_TEMPLATE = "request_email_change.html"
ACCOUNT_PASSWORD_RESET_DEFAULT_TEMPLATE = "password_reset.html"
INVOICE_READY_DEFAULT_TEMPLATE = "send_invoice.html"
ORDER_CONFIRMATION_DEFAULT_TEMPLATE = "confirm_order.html"
ORDER_CONFIRMED_DEFAULT_TEMPLATE = "confirmed_order.html"
ORDER_FULFILLMENT_CONFIRMATION_DEFAULT_TEMPLATE = "confirm_fulfillment.html"
ORDER_FULFILLMENT_UPDATE_DEFAULT_TEMPLATE = "update_fulfillment.html"
ORDER_PAYMENT_CONFIRMATION_DEFAULT_TEMPLATE = "confirm_payment.html"
ORDER_CANCELED_DEFAULT_TEMPLATE = "order_cancel.html"
ORDER_REFUND_CONFIRMATION_DEFAULT_TEMPLATE = "order_refund.html"
SEND_GIFT_CARD_DEFAULT_TEMPLATE = "gift_card.html"


ACCOUNT_CONFIRMATION_SUBJECT_FIELD = "account_confirmation_subject"
ACCOUNT_COMPLETION_SUBJECT_FIELD = "account_completion_subject"
ACCOUNT_SET_CUSTOMER_PASSWORD_SUBJECT_FIELD = "account_set_customer_password_subject"
ACCOUNT_DELETE_SUBJECT_FIELD = "account_delete_subject"
ACCOUNT_CHANGE_EMAIL_CONFIRM_SUBJECT_FIELD = "account_change_email_confirm_subject"
ACCOUNT_CHANGE_EMAIL_REQUEST_SUBJECT_FIELD = "account_change_email_request_subject"
ACCOUNT_PASSWORD_RESET_SUBJECT_FIELD = "account_password_reset_subject"
INVOICE_READY_SUBJECT_FIELD = "invoice_ready_subject"
ORDER_CONFIRMATION_SUBJECT_FIELD = "order_confirmation_subject"
ORDER_CONFIRMED_SUBJECT_FIELD = "order_confirmed_subject"
ORDER_FULFILLMENT_CONFIRMATION_SUBJECT_FIELD = "order_fulfillment_confirmation_subject"
ORDER_FULFILLMENT_UPDATE_SUBJECT_FIELD = "order_fulfillment_update_subject"
ORDER_PAYMENT_CONFIRMATION_SUBJECT_FIELD = "order_payment_confirmation_subject"
ORDER_CANCELED_SUBJECT_FIELD = "order_canceled_subject"
ORDER_REFUND_CONFIRMATION_SUBJECT_FIELD = "order_refund_confirmation_subject"
SEND_GIFT_CARD_SUBJECT_FIELD = "send_gift_card_subject"


ACCOUNT_CONFIRMATION_DEFAULT_SUBJECT = "Account confirmation e-mail"
ACCOUNT_COMPLETION_DEFAULT_SUBJECT = "Account completion e-mail"
ACCOUNT_SET_CUSTOMER_PASSWORD_DEFAULT_SUBJECT = "Hello from {{ site_name }}!"
ACCOUNT_DELETE_DEFAULT_SUBJECT = "Delete your account"
ACCOUNT_CHANGE_EMAIL_CONFIRM_DEFAULT_SUBJECT = "Email change e-mail"
ACCOUNT_CHANGE_EMAIL_REQUEST_DEFAULT_SUBJECT = "Email change e-mail"
ACCOUNT_PASSWORD_RESET_DEFAULT_SUBJECT = "Password reset e-mail"
INVOICE_READY_DEFAULT_SUBJECT = "Invoice"
ORDER_CONFIRMATION_DEFAULT_SUBJECT = "Order #{{ order.number }} details"
ORDER_CONFIRMED_DEFAULT_SUBJECT = "Order #{{ order.number }} confirmed"
ORDER_FULFILLMENT_CONFIRMATION_DEFAULT_SUBJECT = (
    "Your order {{ order.number }} has been fulfilled"
)
ORDER_FULFILLMENT_UPDATE_DEFAULT_SUBJECT = (
    "Shipping update for order {{ order.number }}"
)
ORDER_PAYMENT_CONFIRMATION_DEFAULT_SUBJECT = "Order {{ order.number }} payment details"
ORDER_CANCELED_DEFAULT_SUBJECT = "Order {{ order.number }} canceled"
ORDER_REFUND_CONFIRMATION_DEFAULT_SUBJECT = "Order {{ order.number }} refunded"
SEND_GIFT_CARD_DEFAULT_SUBJECT = "Gift card for {{ site_name }}"
