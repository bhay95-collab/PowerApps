# Builds powerapps/flows/EDD_Rollover_Demo.zip (Import Package (Legacy)).
# Flow "EDD Rollover (demo data)": daily 01:00 AEST. Keeps EDDs in the future on Ward_4A/4B/5A/6A_Shared.
#   python3 tools/flows/build_edd_rollover_flow.py
#
# Rules (per Ben, 2 Nov 2026):
#   - Only rows with a patient name (Patient column not blank).
#   - EDD blank, today or in the past  -> new EDD = today + random 1..7 days.
#   - AROC EDD (4A/4B/5A only): blank/passed, or EDD was just reset -> new AROC = new EDD + random 0..30 days.
#   - Variable Rollover_switch = false  -> flow does nothing (use before go-live).
import json, os, uuid, zipfile

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..')
OUT = os.path.join(ROOT, 'powerapps', 'flows', 'EDD_Rollover_Demo.zip')
FLOW = 'e4d2a7b9-3c51-4f86-a0d7-5b1c8e9f2a64'
API_SP, CONN_SP = 'f1a9c3e5-7b24-4d60-8e1f-2c6a9d0b4e73', 'a6c2e8f0-4d19-4b7a-93e5-0f8d1b7c5a29'
NAME = 'EDD Rollover (demo data - keeps EDDs in the future)'

def mid(key):
    return str(uuid.uuid5(uuid.UUID(FLOW), key))

AUTH = {'value': "@json(decodeBase64(triggerOutputs().headers['X-MS-APIM-Tokens']))['$ConnectionKey']", 'type': 'Raw'}
TZ = "'UTC','E. Australia Standard Time','yyyy-MM-dd'"

def var(name, key, typ, value, after):
    return {'runAfter': after, 'metadata': {'operationMetadataId': mid(name)}, 'type': 'InitializeVariable',
            'inputs': {'variables': [{'name': key, 'type': typ, 'value': value}]}}

def compose(name, expr, after):
    return {'runAfter': after, 'metadata': {'operationMetadataId': mid(name)}, 'type': 'Compose', 'inputs': expr}

def http(name, method, uri, headers, after, body=None):
    p = {'dataset': "@variables('SiteUrl')", 'parameters/method': method, 'parameters/uri': uri, 'parameters/headers': headers}
    if body is not None:
        p['parameters/body'] = body
    return {'runAfter': after, 'metadata': {'operationMetadataId': mid(name)}, 'type': 'OpenApiConnection',
            'inputs': {'host': {'apiId': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline',
                                'connectionName': 'shared_sharepointonline', 'operationId': 'HttpRequest'},
                       'parameters': p, 'authentication': AUTH}}

def local_date(item, field):
    """yyyy-MM-dd (Brisbane) of a SharePoint date, 1900 if blank."""
    return f"convertTimeZone(coalesce({item}?[{field}],'1900-01-01T00:00:00Z'),{TZ})"

def passed(item, field):
    return f"lessOrEquals({local_date(item, field)},outputs('Today_AEST'))"

ROW = "items('Each_row')"
FILTER_ITEM = "item()"
AROC = "outputs('AROC_col')"
EDDF = "outputs('EDD_col')"
HAS_AROC = "items('Each_ward')?['hasAroc']"

# rows worth touching: has patient name AND (EDD needs reset OR AROC needs reset)
filter_expr = ("@and(not(empty(trim(coalesce(item()?[outputs('Patient_col')],'')))),"
               f"or({passed(FILTER_ITEM, EDDF)},"
               f"and({HAS_AROC},{passed(FILTER_ITEM, AROC)})))")

row_actions = {
    'Needs_new_EDD': compose('Needs_new_EDD', '@' + passed(ROW, EDDF), {}),
    'New_EDD': compose('New_EDD',
        "@if(outputs('Needs_new_EDD'),"
        "formatDateTime(addDays(outputs('Today_AEST'),rand(1,8)),'yyyy-MM-dd'),"
        f"{local_date(ROW, EDDF)})",
        {'Needs_new_EDD': ['Succeeded']}),
    'Needs_new_AROC': compose('Needs_new_AROC',
        f"@and({HAS_AROC},or(outputs('Needs_new_EDD'),{passed(ROW, AROC)}))",
        {'New_EDD': ['Succeeded']}),
    'New_AROC': compose('New_AROC',
        "@formatDateTime(addDays(outputs('New_EDD'),rand(0,31)),'yyyy-MM-dd')",
        {'Needs_new_AROC': ['Succeeded']}),
    'Update_body': compose('Update_body',
        f"@union(if(outputs('Needs_new_EDD'),json(concat('{{\"',{EDDF},'\":\"',outputs('New_EDD'),'T00:00:00Z\"}}')),json('{{}}')),"
        f"if(outputs('Needs_new_AROC'),json(concat('{{\"',{AROC},'\":\"',outputs('New_AROC'),'T00:00:00Z\"}}')),json('{{}}')))",
        {'New_AROC': ['Succeeded']}),
    'Update_row': http('Update_row', 'POST',
        "_api/web/lists/getbytitle('@{items('Each_ward')?['title']}')/items(@{items('Each_row')?['ID']})",
        {'Accept': 'application/json;odata=nometadata', 'Content-Type': 'application/json;odata=nometadata',
         'X-HTTP-Method': 'MERGE', 'IF-MATCH': '*'},
        {'Update_body': ['Succeeded']}, body="@outputs('Update_body')"),
}

def field_lookup(name, title, after):
    return http(name, 'GET',
        "_api/web/lists/getbytitle('@{items('Each_ward')?['title']}')/fields?$filter=Title eq '" + title + "'&$select=InternalName",
        {'Accept': 'application/json;odata=nometadata'}, after)

ward_actions = {
    # look up real internal column names by display name (they differ per list)
    'Get_patient_field': field_lookup('Get_patient_field', 'Patient', {}),
    'Get_EDD_field': field_lookup('Get_EDD_field', 'EDD', {'Get_patient_field': ['Succeeded']}),
    'Get_AROC_field': field_lookup('Get_AROC_field', 'AROC EDD', {'Get_EDD_field': ['Succeeded']}),
    'Patient_col': compose('Patient_col', "@first(body('Get_patient_field')?['value'])['InternalName']", {'Get_AROC_field': ['Succeeded']}),
    'EDD_col': compose('EDD_col', "@first(body('Get_EDD_field')?['value'])['InternalName']", {'Patient_col': ['Succeeded']}),
    'AROC_col': compose('AROC_col', "@if(items('Each_ward')?['hasAroc'],first(body('Get_AROC_field')?['value'])['InternalName'],'')", {'EDD_col': ['Succeeded']}),
    'Get_ward_rows': http('Get_ward_rows', 'GET',
        "_api/web/lists/getbytitle('@{items('Each_ward')?['title']}')/items?$select=ID,@{outputs('Patient_col')},@{outputs('EDD_col')}"
        "@{if(items('Each_ward')?['hasAroc'],concat(',',outputs('AROC_col')),'')}&$top=5000",
        {'Accept': 'application/json;odata=nometadata'}, {'AROC_col': ['Succeeded']}),
    'Rows_to_update': {'runAfter': {'Get_ward_rows': ['Succeeded']}, 'metadata': {'operationMetadataId': mid('Rows_to_update')},
                       'type': 'Query', 'inputs': {'from': "@body('Get_ward_rows')?['value']", 'where': filter_expr}},
    'Each_row': {'runAfter': {'Rows_to_update': ['Succeeded']}, 'metadata': {'operationMetadataId': mid('Each_row')},
                 'type': 'Foreach', 'foreach': "@body('Rows_to_update')", 'actions': row_actions,
                 'runtimeConfiguration': {'concurrency': {'repetitions': 5}}},
}

actions = {
    'Site_address': var('Site_address', 'SiteUrl', 'string', 'https://healthqld.sharepoint.com/teams/PhysioDreamTeam', {}),
    'Rollover_switch': var('Rollover_switch', 'RolloverOn', 'boolean', True, {'Site_address': ['Succeeded']}),
    'Today_AEST': compose('Today_AEST', "@convertTimeZone(utcNow(),'UTC','E. Australia Standard Time','yyyy-MM-dd')", {'Rollover_switch': ['Succeeded']}),
    'Wards': var('Wards', 'Wards', 'array', [
        {'title': 'Ward_4A_Shared', 'hasAroc': True},
        {'title': 'Ward_4B_Shared', 'hasAroc': True},
        {'title': 'Ward_5A_Shared', 'hasAroc': True},
        {'title': 'Ward_6A_Shared', 'hasAroc': False}], {'Today_AEST': ['Succeeded']}),
    'Condition_switch_is_on': {
        'runAfter': {'Wards': ['Succeeded']}, 'metadata': {'operationMetadataId': mid('Condition_switch_is_on')}, 'type': 'If',
        'expression': {'equals': ["@variables('RolloverOn')", True]},
        'actions': {'Each_ward': {'runAfter': {}, 'metadata': {'operationMetadataId': mid('Each_ward')}, 'type': 'Foreach',
                                  'foreach': "@variables('Wards')", 'actions': ward_actions,
                                  'runtimeConfiguration': {'concurrency': {'repetitions': 1}}}},
        'else': {'actions': {}}},
}

definition = {
    'name': FLOW,
    'id': f'/providers/Microsoft.Flow/flows/{FLOW}',
    'type': 'Microsoft.Flow/flows',
    'properties': {
        'apiId': '/providers/Microsoft.PowerApps/apis/shared_logicflows',
        'displayName': NAME,
        'definition': {
            '$schema': 'https://schema.management.azure.com/providers/Microsoft.Logic/schemas/2016-06-01/workflowdefinition.json#',
            'contentVersion': 'undefined',
            'parameters': {'$connections': {'defaultValue': {}, 'type': 'Object'}, '$authentication': {'defaultValue': {}, 'type': 'SecureObject'}},
            'triggers': {'Recurrence': {
                'recurrence': {'frequency': 'Day', 'interval': 1, 'startTime': '2026-11-03T01:00:00', 'timeZone': 'E. Australia Standard Time'},
                'metadata': {'operationMetadataId': mid('Recurrence')}, 'type': 'Recurrence'}},
            'actions': actions,
            'outputs': {}
        },
        'connectionReferences': {
            'shared_sharepointonline': {'connectionName': 'shared-sharepointonline-placeholder', 'source': 'Invoker',
                                        'id': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline', 'tier': 'NotSpecified'}},
        'flowFailureAlertSubscribed': True,
        'isManaged': False
    }
}

icon = 'https://static.powerapps.com/resource/ppcr/releases/v1.0.1827/1.0.1827.4913/sharepointonline/icon.png'
manifest = {
    'schema': '1.0',
    'details': {'displayName': NAME, 'description': 'Demo only: keeps patient EDD / AROC EDD in the future on the 4 ward shared lists',
                'createdTime': '2026-11-02T00:00:00.0000000Z', 'packageTelemetryId': mid('telemetry'), 'creator': 'N/A', 'sourceEnvironment': ''},
    'resources': {
        FLOW: {'type': 'Microsoft.Flow/flows', 'suggestedCreationType': 'New', 'creationType': 'Existing, New, Update', 'details': {'displayName': NAME},
               'configurableBy': 'User', 'hierarchy': 'Root', 'dependsOn': [API_SP, CONN_SP]},
        API_SP: {'id': '/providers/Microsoft.PowerApps/apis/shared_sharepointonline', 'name': 'shared_sharepointonline', 'type': 'Microsoft.PowerApps/apis',
                 'suggestedCreationType': 'Existing', 'details': {'displayName': 'SharePoint', 'iconUri': icon}, 'configurableBy': 'System', 'hierarchy': 'Child', 'dependsOn': []},
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
