from django import forms


class ContactForm(forms.Form):
    name = forms.CharField(required=False, max_length=100, label='100 characters max')
    email = forms.EmailField(required=True)
    comment = forms.CharField(required=True, widget=forms.Textarea)


class OutlookAddinForm(forms.Form):
    internal_domains = forms.CharField(required=False, max_length=100, label='InternalDomains')
    client_log_level = forms.ChoiceField(required=True, choices=[('info', u'info'), ('debug', u'debug'), ('trace', u'trace'), ('fatal', u'fatal')], label="ClientLogLevel")
    service_log_level = forms.ChoiceField(required=True, choices=[('info', u'info'), ('debug', u'debug'), ('trace', u'trace'), ('fatal', u'fatal')], label="ServiceLogLevel")
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
    disable_addin_subject_key = forms.CharField(required=False, max_length=100, label='DisableAddInSubjectKey')
    use_categories = forms.IntegerField(required=False, label="UseCategories")
    current_dms = forms.ChoiceField(required=True, choices=[('iManage', u'iManage'), ('iManage', u'NetDocuments')], label="CurrentDms")


class IManageForm(forms.Form):
    supported_auth_type = forms.IntegerField(required=False, label='SupportedAuthType')
    primary_cabinet_id = forms.CharField(required=True, max_length=100, label="PrimaryCabinetId")
    base_uri = forms.URLField(required=True, label="BaseUri")


class CabinetForm(forms.Form):
    prediction_attributes = forms.CharField(required=True, label='PredictionAttributes')
    default_folder_for_email = forms.CharField(required=True, label='DefaultFolderForEmail')
    default_class_for_email = forms.CharField(required=True, label='DefaultClassForEmail')
    side_pane_attributes = forms.CharField(required=True, label='SidePaneAttributes')
    top_pane_attributes = forms.CharField(required=True, label='TopPaneAttributes')
