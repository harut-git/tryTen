from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, label='100 characters max')
    email = forms.EmailField(required=True)
    comment = forms.CharField(required=True, widget=forms.Textarea)


class GenerateForm(forms.Form):
    internal_domains = forms.CharField(required=False, max_length=100, label='Internal Domains')
    client_log_level = forms.ChoiceField(required=True, choices=[(1, u'info'), (2, u'debug'), (3, u'trace'), (4, u'fatal')], label="Client Log Level")
    service_log_level = forms.ChoiceField(required=True, choices=[(1, u'info'), (2, u'debug'), (3, u'trace'), (4, u'fatal')], label="Client Log Level")
    attributes_sync_refresh_days = forms.IntegerField(required=True, label="AttributesSyncRefreshDays")
    outlook_folder_sync_depth_days = forms.IntegerField(required=True, label="OutlookFolderSyncDepthDays")
    outlook_folder_resync_interval_min = forms.IntegerField(required=True, label="OutlookFolderResyncIntervalMin")
    outlook_folder_scan_interval_ms = forms.IntegerField(required=True, label="OutlookFolderScanIntervalMs")
    item_resync_interval_ms = forms.IntegerField(required=True, label="ItemResyncIntervalMs")
    batch_processing_interval_ms = forms.IntegerField(required=True, label="BatchProcessingIntervalMs")
    reconnect_timeout_min = forms.IntegerField(required=True, label="ReconnectTimeoutMin")
    max_archive_files = forms.IntegerField(required=True, label="MaxArchiveFiles")
    clean_statuses_and_categories = forms.IntegerField(required=True, label="CleanStatusesAndCategories")
    selection_timeout_ms = forms.IntegerField(required=True, label="SelectionTimeoutMs")
    status_refresh_interval_min = forms.IntegerField(required=True, label="StatusRefreshIntervalMin")
