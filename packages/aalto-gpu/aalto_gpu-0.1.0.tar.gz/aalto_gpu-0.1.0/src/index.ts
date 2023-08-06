import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import {
  IDisposable, 
  DisposableDelegate
} from '@lumino/disposable'

import {
  DocumentRegistry
} from '@jupyterlab/docregistry';

import {
  ToolbarButton, 
  Dialog
} from '@jupyterlab/apputils';

import {
  jupyterIcon
} from '@jupyterlab/ui-components';

import {
  NotebookPanel, 
  INotebookModel
} from '@jupyterlab/notebook';

import { requestAPI } from './aalto-gpu';

/**
 * Initialization data for the aalto-gpu extension.
 */
const extension: JupyterFrontEndPlugin<void> = {
  activate,
  id: 'aalto-gpu',
  autoStart: true,
};

export class ButtonExtension implements DocumentRegistry.IWidgetExtension<NotebookPanel, INotebookModel> {

  app: JupyterFrontEnd
  constructor(application: JupyterFrontEnd) {
    this.app = application
  }

  createNew(panel: NotebookPanel, context: DocumentRegistry.IContext<INotebookModel>): IDisposable {
    let callback = async () => {
      let data;
      const dataToSend = { notebook_path: context.localPath }
      try {
        data = await requestAPI<any>('send_job', {
          body: JSON.stringify(dataToSend),
          method: 'POST'
        });
        console.log(data);

      } catch (reason) {
        console.error(`Error on POST /aalto-gpu/send_job.\n${reason}`)
      }
      const dialog = new Dialog({
        title: 'Sending job',
        body: data['dialog_body'],
        buttons: [
          Dialog.okButton({ label: 'Ok' })
        ]
      })
      dialog.launch().then(
        () => {console.log('Closed dialog window')}
      )
    };
    let button = new ToolbarButton({
      className: 'aalto-gpu-button',
      icon: jupyterIcon,
      onClick: callback,
      tooltip: 'GPU something something'
    })

    panel.toolbar.insertItem(10, 'gpuButton', button);
    return new DisposableDelegate(() => {
      button.dispose();
    });
  }
}

async function activate(app: JupyterFrontEnd) {
  console.log('JupyterLab extension aalto-gpu is activated!');

  requestAPI<any>('get_example')
    .then(data => {
      console.log(data);
    })
    .catch(reason => {
      console.error(
        `The aalto_gpu server extension appears to be missing.\n${reason}`
      );
    });
  try {
    const data = await requestAPI<any>('send_job');
    console.log(data);
  }  catch (reason) {
    console.error(`Error on GET /aalto-gpu/send_job.\n${reason}`);
  }
  app.docRegistry.addWidgetExtension('Notebook', new ButtonExtension(app))
}

export default extension;
