import json


class _PayloadAlert:

    def __init__(self, title=None, body=None):
        super().__init__()

        self.title = title
        self.body = body

    def to_dict(self, alert_body=None):
        if alert_body is None:
            alert_body = self.body

        d = {}
        if self.title:
            d['title'] = self.title
        if alert_body:
            d['body'] = alert_body
        return d


class IOSPayloadAlert(_PayloadAlert):

    def __init__(self, title=None, body=None, action_loc_key=None, loc_key=None, loc_args=None, launch_image=None, title_loc_key=None, title_loc_args=None):
        super().__init__(title=title, body=body)

        self.action_loc_key = action_loc_key
        self.loc_key = loc_key
        self.loc_args = loc_args
        self.launch_image = launch_image
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.action_loc_key:
            d['action-loc-key'] = self.action_loc_key
        if self.loc_key:
            d['loc-key'] = self.loc_key
        if self.loc_args:
            d['loc-args'] = self.loc_args
        if self.launch_image:
            d['launch-image'] = self.launch_image
        if self.title_loc_key:
            d['title-loc-key'] = self.title_loc_key
        if self.title_loc_args:
            d['title-loc-args'] = self.title_loc_args
        return d


class SafariPayloadAlert(_PayloadAlert):

    def __init__(self, title=None, body=None, action=None):
        super().__init__(title=title, body=body)

        self.action = action

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.action:
            d['action'] = self.action
        return d


class _Payload:

    MAX_PAYLOAD_SIZE = 2048

    def __init__(self, alert=None, custom=None):
        super().__init__()

        self.alert = alert
        self.custom = custom or {}

    def to_dict(self, alert_body=None):
        d = {'aps': {}}
        if self.alert:
            d['aps']['alert'] = self.alert.to_dict(alert_body=alert_body)
        d.update(self.custom)
        return d

    def to_json(self):
        # This method automatically truncates self.alert.body if it's long.
        json_data = self._to_json()

        if self.alert and self.alert.body:
            alert_body = self.alert.body

            while alert_body:
                if len(json_data) <= self.MAX_PAYLOAD_SIZE:
                    break

                alert_body = alert_body[:-1]
                new_alert_body = f'{alert_body}...'
                json_data = self._to_json(alert_body=new_alert_body)

        return json_data

    def _to_json(self, alert_body=None):
        return json.dumps(self.to_dict(alert_body=alert_body), separators=(',', ':'), sort_keys=True).encode('utf-8')


class IOSPayload(_Payload):

    def __init__(self, alert=None, badge=None, sound=None, category=None, custom=None, content_available=False, mutable_content=False):
        super().__init__(alert=alert, custom=custom)

        self.badge = badge
        self.sound = sound
        self.category = category
        self.content_available = content_available
        self.mutable_content = mutable_content

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.badge is not None:
            d['aps']['badge'] = int(self.badge)
        if self.sound:
            d['aps']['sound'] = self.sound
        if self.category:
            d['aps']['category'] = self.category
        if self.content_available:
            d['aps']['content-available'] = 1
        if self.mutable_content:
            d['aps']['mutable-content'] = 1
        return d


class SafariPayload(_Payload):

    def __init__(self, alert=None, url_args=None, custom=None):
        super().__init__(alert=alert, custom=custom)

        self.url_args = url_args or []

    def to_dict(self, alert_body=None):
        d = super().to_dict(alert_body=alert_body)
        if self.url_args:
            d['aps']['url-args'] = self.url_args
        return d


class _Notification:

    PRIORITY_HIGH = 10
    PRIORITY_LOW = 5

    PUSH_TYPE_ALERT = 'alert'
    PUSH_TYPE_BACKGROUND = 'background'
    PUSH_TYPE_VOIP = 'voip'
    PUSH_TYPE_COMPLICATION = 'complication'
    PUSH_TYPE_FILEPROVIDER = 'fileprovider'
    PUSH_TYPE_MDM = 'mdm'

    def __init__(self, payload, apns_id=None, collapse_id=None, expiration=None, priority=None, topic=None, push_type=None):
        super().__init__()

        # A byte array containing the JSON-encoded payload of this push notification.
        # Refer to "The Remote Notification Payload" section in the Apple Local and
        # Remote Notification Programming Guide for more info.
        self.payload = payload

        # An optional canonical UUID that identifies the notification. The canonical
        # form is 32 lowercase hexadecimal digits, displayed in five groups separated
        # by hyphens in the form 8-4-4-4-12. An example UUID is as follows:
        # 	123e4567-e89b-12d3-a456-42665544000
        # If you don't set this, a new UUID is created by APNs and returned in the
        # response.
        self.apns_id = apns_id

        # A string which allows a notification to be replaced by a new notification
        # with the same CollapseID.
        self.collapse_id = collapse_id

        # An optional time at which the notification is no longer valid and can be
        # discarded by APNs. If this value is in the past, APNs treats the
        # notification as if it expires immediately and does not store the
        # notification or attempt to redeliver it. If this value is left as the
        # default (ie, Expiration.IsZero()) an expiration header will not added to the
        # http request.
        self.expiration = expiration

        # The priority of the notification. Specify either apns2.PRIORITY_HIGH (10) or
        # apns2.PRIORITY_LOW (5) If you don't set this, the APNs server will set the
        # priority to 10.
        self.priority = priority

        # The topic of the remote notification, which is typically the bundle ID for
        # your app.
        self.topic = topic

        # (Required for watchOS 6 and later; recommended for macOS, iOS, tvOS, and
        # iPadOS) The value of this header must accurately reflect the contents of
        # your notification’s payload. If there is a mismatch, or if the header is
        # missing on required systems, APNs may return an error, delay the delivery
        # of the notification, or drop it altogether.
        self.push_type = push_type

    def get_headers(self):
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        if self.apns_id:
            headers['apns-id'] = self.apns_id
        if self.collapse_id:
            headers['apns-collapse-id'] = self.collapse_id
        if self.priority:
            headers['apns-priority'] = self.priority
        if self.expiration:
            headers['apns-expiration'] = self.expiration
        if self.topic:
            headers['apns-topic'] = self.topic
        if self.push_type:
            headers['apns-push-type'] = self.push_type
        return headers

    def get_json_data(self):
        return self.payload.to_json()


class IOSNotification(_Notification):

    pass


class SafariNotification(_Notification):

    pass
