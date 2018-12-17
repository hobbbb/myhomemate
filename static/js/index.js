var $ = require("jquery");

var CodeMirror = require("codemirror");
// var CodeMirror = require("codemirror/lib/codemirror.js");
require("codemirror/lib/codemirror.css");
// require("codemirror/theme/cobalt.css");
// require("codemirror/mode/python/python.js");

$(document).ready(function() {
    var myCodeMirror = CodeMirror.fromTextArea(document.getElementById('id_text'), {
        lineNumbers: true,
        mode: "python",
        theme: "cobalt",
    });
});
