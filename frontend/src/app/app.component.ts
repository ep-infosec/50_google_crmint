// Copyright 2018 Google Inc
//
// Licensed under the Apache License, Version 2.0 (the "License");
// you may not use this file except in compliance with the License.
// You may obtain a copy of the License at
//
//      http://www.apache.org/licenses/LICENSE-2.0
//
// Unless required by applicable law or agreed to in writing, software
// distributed under the License is distributed on an "AS IS" BASIS,
// WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
// See the License for the specific language governing permissions and
// limitations under the License.

import { Component } from '@angular/core';

import { environment } from 'environments/environment';

declare global {
  interface Window {
    crmintConf: {
      appTitle: string
    }
  }
}

const crmintConf = window.crmintConf || {appTitle: 'Custom'};

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.sass']
})
export class AppComponent {
  title = `CRMint App • ${crmintConf.appTitle}`;

  alerts = [
    // Example
    // {
    //   icon: 'alert-octagon',
    //   text: 'Removing of active pipeline is unavailable',
    //   type: 'danger'
    // }
  ];

  closeAlert(index) {
    this.alerts.splice(index, 1);
  }

  addAlert(message) {
    this.alerts.push({
      icon: 'alert',
      text: message,
      type: 'danger'
    });
  }
}
