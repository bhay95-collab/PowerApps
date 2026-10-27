# Builds powerapps/flows/Get_Rule_PDF.zip (Import Package (Legacy)).
# Flow "GetRulePdf": Power Apps (V2) trigger (FilePath, e.g. /Shared Documents/RBWH Clinical Informatics/RBWH Business Rules/Allied Health.pdf)
#   -> SharePoint "Get file content using path" on the CITTA site -> respond with the PDF as a base64 data address.
#   python3 tools/flows/build_rule_pdf_flow.py
import json, os, zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUT = os.path.join(ROOT, 'powerapps', 'flows', 'Get_Rule_PDF.zip')
FLOW = '8c3d5f27-6a1e-4b94-b2d8-1f7a9e4c6b30'
API_SP, CONN_SP = 'b7e2c9a4-5d13-4f68-8a20-3c9e1d7b5f46', 'd1a6f8e3-9b24-4c57-a3e0-6f2b8d4c1e95'
NAME = 'GetRulePdf'
SITE = 'https://healthqld.sharepoint.com/teams/CITTA'
GET = 'Get_file_content_using_path'

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
                        'text': {'title': 'FilePath', 'type': 'string', 'x-ms-dynamically-added': True, 'description': 'Please enter your input', 'x-ms-content-hint': 'TEXT'}},
                        'required': ['text']}}
                }
            },
            'actions': {
                GET: {
                    'runAfter': {}, 'type': 'OpenApiConnection',
                    'inputs': {
                        'host': {'apiId': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline', 'connectionName': 'shared_sharepointonline', 'operationId': 'GetFileContentByPath'},
                        'parameters': {
                            'dataset': SITE,
                            'path': "@triggerBody()['text']",
                            'inferContentType': True
                        },
                        'authentication': {'value': "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']", 'type': 'Raw'}
                    }
                },
                'Respond_to_a_PowerApp_or_flow': {
                    'runAfter': {GET: ['Succeeded']}, 'type': 'Response', 'kind': 'PowerApp',
                    'inputs': {'statusCode': 200,
                               'body': {'pdf': f"@concat('data:application/pdf;base64,', body('{GET}')?['$content'])"},
                               'schema': {'type': 'object', 'properties': {'pdf': {'title': 'pdf', 'x-ms-dynamically-added': True, 'type': 'string'}}}}
                }
            },
            'outputs': {}
        },
        'connectionReferences': {
            'shared_sharepointonline': {'connectionName': 'shared-sharepointonline-placeholder', 'source': 'Invoker', 'id': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline', 'tier': 'NotSpecified'}
        },
        'flowFailureAlertSubscribed': False,
        'isManaged': False
    }
}
icon = 'https://static.powerapps.com/resource/ppcr/releases/v1.0.1827/1.0.1827.4913/sharepointonline/icon.png'
manifest = {
    'schema': '1.0',
    'details': {'displayName': NAME, 'description': 'Floorwalking app: returns one RBWH Business Rules PDF from the CITTA site (FilePath = /Shared Documents/...) so the app can show it', 'createdTime': '2026-10-27T00:00:00.0000000Z',
                'packageTelemetryId': 'e5b19c73-2f84-4d0a-96c1-7a3d8e2f4b18', 'creator': 'N/A', 'sourceEnvironment': ''},
    'resources': {
        FLOW: {'type': 'Microsoft.Flow/flows', 'suggestedCreationType': 'New', 'creationType': 'Existing, New, Update', 'details': {'displayName': NAME},
               'configurableBy': 'User', 'hierarchy': 'Root', 'dependsOn': [API_SP, CONN_SP]},
        API_SP: {'id': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline', 'name': 'shared_sharepointonline', 'type': 'Microsoft.PowerApps/apis', 'suggestedCreationType': 'Existing',
                 'details': {'displayName': 'SharePoint', 'iconUri': icon}, 'configurableBy': 'System', 'hierarchy': 'Child', 'dependsOn': []},
        CONN_SP: {'type': 'Microsoft.PowerApps/apis/connections', 'suggestedCreationType': 'Existing', 'creationType': 'Existing',
                  'details': {'displayName': 'SharePoint connection', 'iconUri': icon}, 'configurableBy': 'User', 'hierarchy': 'Child', 'dependsOn': [API_SP]}
    }
}
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED) as z:
    z.writestr('manifest.json', json.dumps(manifest))
    z.writestr('Microsoft.Flow/flows/manifest.json', json.dumps({'packageSchemaVersion': '1.0', 'flowAssets': {'assetPaths': [FLOW]}}))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/definition.json', json.dumps(definition))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/apisMap.json', json.dumps({'shared_sharepointonline': API_SP}))
    z.writestr(f'Microsoft.Flow/flows/{FLOW}/connectionsMap.json', json.dumps({'shared_sharepointonline': CONN_SP}))
print('wrote', OUT)
