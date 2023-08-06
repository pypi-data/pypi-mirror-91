import json
import os

import requests


_query = '''
mutation createTaskFromTemplate($templateName: String!, $project: String!, $queue: String!, $variables: JSONString!) {
  createTaskFromTemplate(
    templateName: $templateName,
    project: $project,
    queue: $queue,
    variables: $variables,
    streamStdout: false,
    streamStderr: false,
  ) {
    ok
    error
    task {
      id
    }
  }
}'''


def client(url=None):
    if url is None:
        url = os.environ.get('SEC__FUNCTION_URL')
    return FunctionClient(url)


class FunctionClient:
    def __init__(self, url):
        self.url = url

    def _send_api(self, payload):
        res = requests.post(f'{self.url}/graphql', json=payload)
        return res.json()

    def create_task_from_template(self, project, queue, template, variables):
        payload = {
            'query': _query,
            'variables': {
                'templateName': template,
                'project': project,
                'queue': queue,
                'variables': json.dumps(variables),
            }
        }
        res = self._send_api(payload)
        return res['data']['createTaskFromTemplate']['task']['id']
