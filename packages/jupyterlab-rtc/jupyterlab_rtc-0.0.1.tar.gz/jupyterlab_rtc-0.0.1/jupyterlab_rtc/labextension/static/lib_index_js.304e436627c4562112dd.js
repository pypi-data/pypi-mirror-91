(self["webpackChunk_jupyterlab_rtc"] = self["webpackChunk_jupyterlab_rtc"] || []).push([["lib_index_js"],{

/***/ "./lib/AutomergeActions.js":
/*!*********************************!*\
  !*** ./lib/AutomergeActions.js ***!
  \*********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "initDocument": () => /* binding */ initDocument,
/* harmony export */   "initDocumentText": () => /* binding */ initDocumentText,
/* harmony export */   "applyChanges": () => /* binding */ applyChanges,
/* harmony export */   "getChanges": () => /* binding */ getChanges,
/* harmony export */   "merge": () => /* binding */ merge,
/* harmony export */   "getHistory": () => /* binding */ getHistory
/* harmony export */ });
/* harmony import */ var automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! automerge-wasm-bundler */ "webpack/sharing/consume/default/automerge-wasm-bundler/automerge-wasm-bundler");
/* harmony import */ var automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0__);

const initDocument = () => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().init();
};
const initDocumentText = () => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().from({
        docId: '',
        textArea: new (automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().Text)()
    });
};
const applyChanges = (doc, changes) => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().applyChanges(doc, changes);
};
const getChanges = (oldDoc, newDoc) => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().getChanges(oldDoc, newDoc);
};
const merge = (oldDoc, newDoc) => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().merge(oldDoc, newDoc);
};
const getHistory = (doc) => {
    return automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_0___default().getHistory(doc).map(state => [state.change.message, state.snapshot.textArea]);
};


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

"use strict";
__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => __WEBPACK_DEFAULT_EXPORT__
/* harmony export */ });
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! automerge-wasm-bundler */ "webpack/sharing/consume/default/automerge-wasm-bundler/automerge-wasm-bundler");
/* harmony import */ var automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _AutomergeActions__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./AutomergeActions */ "./lib/AutomergeActions.js");


// import { CodeMirrorEditor } from '@jupyterlab/codemirror';


class Rtc {
    constructor(notebookTracker, editorTracker) {
        this.notebookTracker = notebookTracker;
        this.editorTracker = editorTracker;
        this.notebookTracker.activeCellChanged.connect((sender, cell) => this._activeCellChanged(cell));
        this.editorTracker.widgetAdded.connect((sender, widget) => this._setupFileEditor(widget.content));
        this.editorTracker.currentChanged.connect((sender, widget) => this._setupFileEditor(widget.content));
    }
    _onCellValueChange(value, change) {
        if (this.rtcCell.textArea) {
            if (this.cell.model.value.text !== this.rtcCell.textArea.toString()) {
                const newDoc = automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_2___default().change(this.rtcCell, (d) => {
                    if (change.type === 'insert') {
                        d.textArea.insertAt(change.start, change.value);
                    }
                    if (change.type === 'remove') {
                        d.textArea.deleteAt(change.start, (change.end - change.start));
                    }
                });
                const changes = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.getChanges)(this.rtcCell, newDoc);
                this.rtcCell = newDoc;
                this.ws.send(changes[0]);
            }
        }
    }
    _activeCellChanged(cell) {
        if (cell != null) {
            this.rtcCell = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.initDocument)();
            this.cell = cell;
            this.cell.editor.model.value.changed.connect((value, change) => this._onCellValueChange(value, change));
            //      this.ws = new WebSocket(`ws://localhost:8888/jupyterlab_rtc/websocket?doc=${cell.id}`);
            this.ws = new WebSocket(`ws://localhost:4321/${cell.id}`);
            this.ws.binaryType = 'arraybuffer';
            this.ws.onmessage = (message) => {
                if (message.data) {
                    const data = new Uint8Array(message.data);
                    const changedDoc = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.applyChanges)(this.rtcCell, [data]);
                    this.rtcCell = changedDoc;
                    const text = this.rtcCell.textArea.toString();
                    if (this.cell.model.value.text !== text) {
                        this.cell.model.value.text = text;
                    }
                }
            };
        }
    }
    _onFileEditorValueChange(value, change) {
        if (this.rtcEditor.textArea) {
            if (this.fileEditor.model.value.text !== this.rtcEditor.textArea.toString()) {
                const newDoc = automerge_wasm_bundler__WEBPACK_IMPORTED_MODULE_2___default().change(this.rtcEditor, (d) => {
                    if (change.type === 'insert') {
                        d.textArea.insertAt(change.start, change.value);
                    }
                    if (change.type === 'remove') {
                        d.textArea.deleteAt(change.start, (change.end - change.start));
                    }
                });
                const changes = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.getChanges)(this.rtcEditor, newDoc);
                this.rtcEditor = newDoc;
                this.ws.send(changes[0]);
            }
        }
    }
    _setupFileEditor(fileEditor) {
        if (fileEditor != null) {
            this.rtcEditor = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.initDocument)();
            this.fileEditor = fileEditor;
            this.fileEditor.editor.model.value.changed.connect((value, change) => this._onFileEditorValueChange(value, change));
            //      this.ws = new WebSocket(`ws://localhost:8888/jupyterlab_rtc/websocket?doc=${cell.id}`);
            this.ws = new WebSocket(`ws://localhost:4321/${fileEditor.id}`);
            this.ws.binaryType = 'arraybuffer';
            this.ws.onmessage = (message) => {
                if (message.data) {
                    const data = new Uint8Array(message.data);
                    const changedDoc = (0,_AutomergeActions__WEBPACK_IMPORTED_MODULE_3__.applyChanges)(this.rtcEditor, [data]);
                    this.rtcEditor = changedDoc;
                    const text = this.rtcEditor.textArea.toString();
                    if (this.fileEditor.model.value.text !== text) {
                        this.fileEditor.model.value.text = text;
                    }
                }
            };
        }
    }
}
/**
 * Initialization data for the @jupyterlab/rtc extension.
 */
const rtc = {
    id: '@jupyterlab/rtc:extension',
    autoStart: true,
    requires: [
        _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_1__.INotebookTracker,
        _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_0__.IEditorTracker
    ],
    activate: (app, notebookTracker, editorTracker) => {
        const rtc = new Rtc(notebookTracker, editorTracker);
        console.log('JupyterLab extension @jupyterlab/rtc is activated!', rtc);
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (rtc);


/***/ })

}]);
//# sourceMappingURL=lib_index_js.304e436627c4562112dd.js.map