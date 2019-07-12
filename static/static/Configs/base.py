base_string = '''
[-HKEY_CURRENT_USER\Software\Zero]
[HKEY_CURRENT_USER\Software\Zero]

[HKEY_CURRENT_USER\Software\Zero\OutlookAddin]
"InternalDomains"="zeroapp.ai"
"ClientLogLevel"="trace"
"ServiceLogLevel"="trace"
"AttributesSyncRefreshDays"=dword:00000001
"OutlookFolderSyncDepthDays"=dword:0000001E
"OutlookFolderResyncIntervalMin"=dword:000001a4
"OutlookFolderScanIntervalMs"=dword:00000064
"ItemResyncIntervalMs"=dword:00000005
"BatchProcessingIntervalMs"=dword:00000032
"ReconnectTimeoutMin"=dword:00000001
"MaxArchiveFiles"=dword:00000014
"CleanStatusesAndCategories"=dword:00000001
"SelectionTimeoutMs"=dword:00000005
"StatusRefreshIntervalMin"=dword:00000000
"DisableAddInSubjectKey"="zero-deactivate"
"UseCategories"=dword:00000001
"CurrentDms"="iManage"

[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses]

[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\iManage]
"SupportedAuthType"=dword:00000002
"PrimaryCabinetId"="iwork"
"BaseUri"="https://10.1.1.5/"

[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\iManage\Cabinets]

[HKEY_CURRENT_USER\Software\Zero\OutlookAddin\Dmses\iManage\Cabinets\iwork]
"PredictionAttributes"="1,2,0"
"DefaultFolderForEmail"="FL_DEL_NEW"
"DefaultClassForEmail"=""
"SidePaneAttributes"="1,2,0,3"
"TopPaneAttributes"="1,2,0,3"'''