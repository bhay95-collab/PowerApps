# Builds powerapps/flows/DTV_Dashboard_Email.zip (Import Package (Legacy)).
# Flow "DTVDashboardEmail": Power Apps (V2) trigger -> Send an email (V2) with a CSV attachment -> respond to the app.
#   python3 tools/flows/build_dtv_email_flow.py
import json, os, zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUT = os.path.join(ROOT, 'powerapps', 'flows', 'DTV_Dashboard_Email.zip')
FLOW = 'd7a1c2e4-5b3f-4e8a-9c61-2f0b7d4e8a13'
API_O365, CONN_O365 = 'a3f6b2d1-8c4e-4f7a-b915-6e2d0c3a7f48', 'c58e9d02-1a7b-4c36-8f2e-94b1d6a0e7c5'
NAME = 'DTVDashboardEmail'

def inp(title):
    return {'title': title, 'type': 'string', 'x-ms-dynamically-added': True, 'description': 'Please enter your input', 'x-ms-content-hint': 'TEXT'}

definition = {
    'name': FLOW,
    'id': f'/providers/Microsoft.Flow/flows/{FLOW}',
    'type': 'Microsoft.Flow/flows',
    'properties': {
        'apiId': '/providers/Microsoft.PowerApps/apis/shared_logicflows',
        'displayName': NAME,
        'definition': {
            '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#',
            'contentVersion': '1.0.0.0',
            'parameters': {'$connections': {'defaultValue': {}, 'type': 'Object'}, '$authentication': {'defaultValue': {}, 'type': 'SecureObject'}},
            'triggers': {
                'manual': {
                    'type': 'Request', 'kind': 'PowerAppV2',
                    'inputs': {'schema': {'type': 'object', 'properties': {
                        'text': inp('ToEmail'), 'text_1': inp('Subject'), 'text_2': inp('BodyHtml'), 'text_3': inp('FileName'), 'text_4': inp('CsvText')},
                        'required': ['text', 'text_1', 'text_2', 'text_3', 'text_4']}}
                }
            },
            'actions': {
                'Send_an_email_(V2)': {
                    'runAfter': {}, 'type': 'OpenApiConnection',
                    'inputs': {
                        'host': {'apiId': '/providers/Microsoft.PowerApps/apis/shared_office365', 'connectionName': 'shared_office365', 'operationId': 'SendEmailV2'},
                        'parameters': {
                            'emailMessage/To': "@triggerBody()['text']",
                            'emailMessage/Subject': "@triggerBody()['text_1']",
                            'emailMessage/Body': "@triggerBody()['text_2']",
                            'emailMessage/Attachments': [{'Name': "@triggerBody()['text_3']", 'ContentBytes': "@triggerBody()['text_4']"}],
                            'emailMessage/Importance': 'Normal'
                        },
                        'authentication': {'value': "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']"}
                    }
                },
                'Respond_to_a_PowerApp_or_flow': {
                    'runAfter': {'Send_an_email_(V2)': ['Succeeded']}, 'type': 'Response', 'kind': 'PowerApp',
                    'inputs': {'statusCode': 200, 'body': {'result': 'sent'},
                               'schema': {'type': 'object', 'properties': {'result': {'title': 'result', 'x-ms-dynamically-added': True, 'type': 'string'}}}}
                }
            },
            'outputs': {}
        },
        'connectionReferences': {
            'shared_office365': {'connectionName': 'shared-office365-placeholder', 'source': 'Invoker', 'id': '/providers/Microsoft.PowerApps/apis/shared_office365', 'tier': 'NotSpecified'}
        },
        'flowFailureAlertSubscribed': False,
        'isManaged': False
    }
}
icon = 'https://static.powerapps.com/resource/ppcr/releases/v1.0.1831/1.0.1831.5067/office365/icon.png'
manifest = {
    'schema': '1.0',
    'details': {'displayName': NAME, 'description': 'DTV Audit Dashboard: emails the summary and CSV extract to the person who pressed the button', 'createdTime': '2026-10-08T00:00:00.0000000Z',
                'packageTelemetryId': 'b0e3f6a2-7d14-4c59-8e2a-31f9c7d5a6e0', 'creator': 'N/A', 'sourceEnvironment': ''},
    'resources': {
        FLOW: {'type': 'Microsoft.Flow/flows', 'suggestedCreationType': 'New', 'creationType': 'Existing, New, Update', 'details': {'displayName': NAME},
               'configurableBy': 'User', 'hierarchy': 'Root', 'dependsOn': [API_O365, CONN_O365]},
        API_O365: {'id': '/providers/Microsoft.PowerApps/apis/shared_office365', 'name': 'shared_office365', 'type': 'Microsoft.PowerApps/apis', 'suggestedCreationType': 'Existing',
                   'details': {'displayName': 'Office 365 Outlook', 'iconUri': icon}, 'configurableBy': 'System', 'hierarchy': 'Child', 'dependsOn': []},
        CONN_O365: {'type': 'Microsoft.PowerApps/apis/connections', 'suggestedCreationType': 'Existing', 'creationType': 'Existing',
                    'details': {'displayName': 'Office 365 Outlook connection', 'iconUri': icon}, 'configurableBy': 'User', 'hierarchy': 'Child', 'dependsOn': [API_O365]}
    }
}
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('manifest.json', json.dumps(manifest))
    z.writestr('Microsoft.Flow/flows/manifest.json', json.dumps({'packageSchemaVersion': '1.0', 'flowAssets': {'assetPaths': [FLOW]}}))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/definition.json', json.dumps(definition))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/apisMap.json', json.dumps({'shared_office365': API_O365}))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/connectionsMap.json', json.dumps({'shared_office365': CONN_O365}))
print('wrote', OUT)
