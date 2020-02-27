
# Python program invoked by crontab on the DSVM, executes processing based on the
# presence or absence of a "trigger blob".
# Chris Joakim, Microsoft, 2019/05/09
#
# see https://github.com/Azure/azure-storage-python
# see https://github.com/Azure/azure-storage-python/blob/master/azure-storage-blob/azure/storage/blob/blockblobservice.py
# see https://github.com/Azure/azure-storage-python/blob/master/azure-storage-blob/azure/storage/blob/baseblobservice.py

import datetime
import json
import os
import platform
import sys
import traceback
import uuid

# Microsoft open-source library for Azure Blob Storage
from azure.storage.blob import BlockBlobService

now = datetime.datetime.now()
run_time = str(now).replace(' ', '-')
run_id   = str(uuid.uuid4())
log_messages = list()

def print_env_vars():
    for name in os.environ:
        value = os.getenv(name)
        print('{} -> {}'.format(name, value))

def read_env_var(name, default_value='?'):
    if name in os.environ:
        v = os.environ[name]
        abbrev = v[:10]
        log('read_env_var found: {} -> {}... ({})'.format(name, abbrev, len(v)))
        return v
    else:
        log('read_env_var not found: {}'.format(name))
        return default_value

def get_blob_client():
    acct = read_env_var('AZURE_STORAGE_ACCOUNT')
    key  = read_env_var('AZURE_STORAGE_KEY')
    blob_client = BlockBlobService(account_name=acct, account_key=key)
    return blob_client

def read_blob(container_name, blob_name, parse_json=True):
    try:
        client = get_blob_client()
        blob = client.get_blob_to_text(container_name, blob_name)
        content = blob.content
        log('read_blob, read: {}/{}'.format(container_name, blob_name))
        if parse_json:
            return json.loads(content)
        else:
            return content
    except:
        log('read_blob, error: {}/{}'.format(container_name, blob_name))
        return None

def write_blob(container_name, blob_name, obj, as_json=True):
    try:
        content = obj
        if as_json:
            content = json.dumps(obj, sort_keys=False, indent=2)
        client = get_blob_client()
        client.create_blob_from_text(container_name, blob_name, content, encoding='utf-8')
        log("write_json_blob; created {}/{}".format(container_name, blob_name))
        return True
    except:
        log('write_json_blob, error: {}/{}'.format(container_name, blob_name))
        return False

def list_blobs(container_name):
    client = get_blob_client()
    return client.list_blobs(container_name)

def delete_blob(container_name, blob_name):
    client = get_blob_client()
    client.delete_blob(container_name, blob_name)

def process_trigger_blob(container_name, blob_name, out_container_name):
    success = False
    try:
       trigger_obj = read_blob(container_name, blob_name, True)
       
       if trigger_obj != None:
           # Your business logic goes here!
           # Current super-simple example logic simply writes the augmented trigger-blob contents
           # to another container, then delete the trigger blob.
           
           log("input trigger_obj:\n{}".format(json.dumps(trigger_obj, sort_keys=False, indent=4)))

           trigger_obj['run_id'] = run_id
           trigger_obj['run_time'] = run_time
           trigger_obj['os_name']  = os.name
           trigger_obj['os_system'] = platform.system()
           trigger_obj['os_release'] = platform.release()
       
           log("output object:\n{}".format(json.dumps(trigger_obj, sort_keys=False, indent=4)))
           write_blob(out_container_name, blob_name, trigger_obj, True)

           # If successful so far, then delete the trigger blob after processing it above.
           delete_blob(container_name, blob_name)
           success = True
    except:
        print(sys.exc_info())
        traceback.print_exc()
    finally:
        return success

def read_text_file(infile):
    lines = list()
    with open(infile, 'rt') as f:
        for idx, line in enumerate(f):
            lines.append(line.strip())
    return lines

def write_text_file(outfile, text):
    with open(outfile, "w", newline="\n") as out:
        out.write(text)
        print("file written: {}".format(outfile))

def log(msg):
    print(msg)
    log_messages.append(msg)

def arg_present(s):
    for arg in sys.argv:
        if arg.lower() == s:
            return True
    return False


if __name__ == "__main__":
    log('datetime: {}'.format(now))
    log('run_id:   {}'.format(run_id))
    log('run_time: {}'.format(run_time))

    # Get the names of the Function, and Azure Storage Blobs and containers
    # from optional environment variables:
    func                = read_env_var('FUNCTION', 'none')
    flags               = read_env_var('FLAGS', 'none')
    in_container_name   = read_env_var('IN_CONTAINER_NAME', 'dsvmin')
    in_blob_name        = read_env_var('IN_BLOB_NAME', 'trigger.json')
    out_container_name  = read_env_var('OUT_CONTAINER_NAME', 'dsvmout')
    logs_container_name = read_env_var('LOGS_CONTAINER_NAME', 'dsvmlogs')
    trigger_blob_value  = read_env_var('TRIGGER_BLOB_VALUE', 'Miles,Elsa')
    
    try:
        if func == 'env':
            print_env_vars()
            print('datetime: {}'.format(now))
            print('run_time: {}'.format(run_time))
            print('run_id:   {}'.format(run_id))
            
        elif func == 'create_trigger_blob':
            container_name, blob_name = in_container_name, in_blob_name
            blob_value = trigger_blob_value
            data = dict()
            data['container_name'] = container_name
            data['blob_name'] = blob_name
            data['value'] = blob_value
            data['date_time'] = str(datetime.datetime.now())
            write_blob(container_name, blob_name, data)

        elif func == 'get_blob':
            container_name, blob_name = in_container_name, in_blob_name
            print('get_blob: {}/{}'.format(container_name, blob_name))
            if blob_name.lower().endswith('.json'):
                obj  = read_blob(container_name, blob_name, True)
                jstr = json.dumps(obj, sort_keys=False, indent=4)
                print(jstr)
            else:
                text = read_blob(container_name, blob_name, False)
                print(text)

        elif func == 'delete_blob':
            container_name, blob_name = in_container_name, in_blob_name
            print('delete_blob: {}/{}'.format(container_name, blob_name))
            result = delete_blob(container_name, blob_name)
            print('result: {}'.format(result))

        elif func == 'list_blobs':
            container_name = in_container_name
            print('list_blobs; container: {}'.format(container_name))
            blob_list = list_blobs(container_name)
            for blob in blob_list:
                print('blob: {}'.format(str(blob.name)))

        elif func == 'process_trigger_blob':
            container_name, blob_name = in_container_name, in_blob_name
            result = process_trigger_blob(container_name, blob_name, out_container_name)
            log('process_trigger_blob; result: {}'.format(result))

    except:
        print(sys.exc_info())
        traceback.print_exc()
    finally:
        content = "\n".join(log_messages)
        if '--eoj-file' in flags:
            outfile = 'logs/{}-{}.log'.format(run_time, func).replace('_', '-')
            write_text_file(outfile, content)
        if '--eoj-blob' in flags:
            bname = '{}-{}.log'.format(run_time, func).replace('_', '-')
            write_blob('dsvmlogs', bname, content, False)
