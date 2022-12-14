# Copyright 2021 Google Inc. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Worker to update Google Analytics remarketing audiences."""
from google.cloud import bigquery

from jobs.workers.bigquery import bq_worker
from jobs.workers.ga import ga_utils


class GAAudiencesUpdater(bq_worker.BQWorker):
  """Worker to update GA audiences using values from a BigQuery table.

  For more details on the required GA Audience JSON template format, see:
  https://developers.google.com/analytics/devguides/config/mgmt/v3/mgmtReference/management/remarketingAudience#resource.
  """

  PARAMS = [
      ('account_id', 'string', True, '',
       'GA Account ID (e.g. 12345)'),
      ('property_id', 'string', True, '',
       'GA Property Tracking ID (e.g. UA-12345-3)'),
      ('bq_project_id', 'string', False, '', 'BQ Project ID'),
      ('bq_dataset_id', 'string', True, '', 'BQ Dataset ID'),
      ('bq_table_id', 'string', True, '', 'BQ Table ID'),
      ('bq_dataset_location', 'string', False, '', 'BQ Dataset Location'),
      ('template', 'text', True, '', 'GA audience JSON template'),
  ]


  def _execute(self) -> None:
    bq_client = self._get_client()
    dataset_ref = bigquery.DatasetReference(
        self._params['bq_project_id'], self._params['bq_dataset_id'])
    table_ref = bigquery.TableReference(dataset_ref,
                                        self._params['bq_table_id'])
    patches = ga_utils.get_audience_patches(
        bq_client, table_ref, self._params['template'])
    self.log_info(f'Retrieved #{len(patches)} audience configs from BigQuery')
    ga_client = ga_utils.get_client('analytics', 'v3')
    audiences = ga_utils.fetch_audiences(
        ga_client, self._params['account_id'], self._params['property_id'])
    self.log_info(f'Fetched #{len(audiences)} audiences from the GA Property')
    operations = ga_utils.get_audience_operations(patches, audiences)
    self.log_info(f'Executing #{len(operations)} operations to update the '
                  f'state of GA with the audience configs from your BigQuery')
    ga_utils.run_audience_operations(
        ga_client,
        self._params['account_id'],
        self._params['property_id'],
        operations,
        progress_callback=self.log_info)
