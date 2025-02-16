// @ts-nocheck
import { WebChannelHandler } from "@/js/webchannel";

import 'suneditor/dist/css/suneditor.min.css';
import SunEditor from "suneditor";
import lang from 'suneditor/src/lang';
import plugins from 'suneditor/src/plugins';
import type {CommandPlugin} from 'suneditor/src/plugins/CommandPlugin';
import type {Core} from "suneditor/src/lib/core";
import type {SunEditorOptions} from "suneditor/src/suneditor";

const addNbspPlugin: CommandPlugin = {
    name: "addNbspPlugin",
    display: "command",

    title: "&amp;nbsp; 추가",
    innerHTML: '<span class="se-icon-text">&</span>',
    buttonClass: "se-code-view-enabled",

    add: function (core: Core, targetElement: HTMLElement) {
        const context = core.context;

        // Store button reference in context
        context.addNbspCommand = {
            targetButton: targetElement
        };
    },
    action: function () {
        this.functions.insertHTML("&nbsp;");
    }
};

const toggleStyleCopyPlugin: CommandPlugin = {
    name: "toggleStyleCopyPlugin",
    display: "command",

    title: "스타일 복사",
    innerHTML: '<span class="se-icon-text">S</span>',
    buttonClass: '',

    add: function (core: Core, targetElement: HTMLElement) {
        const context = core.context;
        let enableStyleCopy: boolean = false

        // Store button reference in context
        context.toggleStyleCopyCommand = {
            targetButton: targetElement,
            enable: enableStyleCopy
        };
    },
    action: function () {
        if (this.context.toggleStyleCopyCommand.enableStyleCopy) {
            this.util.removeClass(this.context.toggleStyleCopyCommand.targetButton, "active");
            this.context.toggleStyleCopyCommand.enableStyleCopy = false;
        } else {
            this.util.addClass(this.context.toggleStyleCopyCommand.targetButton, "active");
            this.context.toggleStyleCopyCommand.enableStyleCopy = true;
        }
    },
}

const editorElement = document.getElementById("editor") as HTMLTextAreaElement;
if (!editorElement) {
    console.error("Editor element not found!");
    throw new Error("Editor element not found!");
}

const templates = [
    {
        name: "Chart-Template",
        html: "<div id='chart-container'> <table ><tbody><tr><td>title</td><td>xtitle</td><td>ytitle</td></tr><tr><td></td><td></td><td></td></tr></tbody></table><br><table id='chart' class=\"se-table-layout-fixed\"><tbody><tr><td>Category\\Series</td><td> </td></tr><tr><td></td><td></td></tr></tbody></table><br><table><tbody><tr><td>ChartType</td></tr><tr><td></td></tr></tbody></table></div>"
    }
]

const options: SunEditorOptions = {
    strictMode: false,
    lang: lang.ko,
    width: "100%",
    height: "auto",
    mode: "classic",
    templates: templates,
    rtl: false,
    videoFileInput: false,
    tabDisable: false,
    plugins: [plugins.table, plugins.template, plugins.font, plugins.fontSize, plugins.formatBlock, plugins.align, addNbspPlugin, toggleStyleCopyPlugin],
    buttonList: [
        ["table", "codeView", "template", "save"],
        ["undo", "redo"],
        ["font", "fontSize", "formatBlock"],
        ["subscript", "superscript"],
        ["removeFormat", "outdent", "indent", "align"],
        ["showBlocks"],
        ["addNbspPlugin", "toggleStyleCopyPlugin"]
    ],
}

const editor = SunEditor.create(editorElement, options);

editor.onPaste = function (e, cleanData, maxCharCount, core) {
    if (core.context.toggleStyleCopyCommand.enableStyleCopy) return;

    const plainText = e.clipboardData.getData('text/plain');
    this.insertHTML(plainText);
    e.preventDefault();
    return false;
};


const webChannel = WebChannelHandler.getInstance();

async function setupEditor() {
    await webChannel.registerCallback("editor", (msg) => {
        console.log("Message from Python (editor):", msg);
    });

    document.getElementById("update-chart")?.addEventListener("click", async () => {
        await webChannel.sendMessage("editor", "update");
    });
}

setupEditor();