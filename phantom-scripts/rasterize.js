//https://github.com/ariya/phantomjs/blob/master/examples/rasterize.js
var args = require('./minimist.js')(phantom.args);
var b64 = require('./b64.js');

var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

if (args['_'].length < 2 ) {
    console.log('Usage: rasterize.js URL filename [--session session-id] [--header header-base64]');
    phantom.exit(1);
} else {
    address = args['_'][0];
    output = args['_'][1];

    header_b64 = args['header'];
    headerStr = null;
    header : {};
    
    page.viewportSize = { width: 600, height: 600 };

    pz = {
        format: "A4",
        orientation: "portrait",

        footer: {
            height: "0.9cm",
            contents: phantom.callback(function (pageNum, numPages) {
                return '<h4 style="text-align:center; display: block ">' + pageNum + " / " + numPages + '</h4>';
            })
        },
    };

    

	if ((typeof header_b64 !== 'undefined') && (header_b64 != null)) {
        pz.header = { 'height':'1cm',
                      'contents': phantom.callback(function (pageNum, numPages) { return b64.toString(header_b64); })
                    }
    }

    page.paperSize = pz;

    if ((typeof args['session'] !== 'undefined') && (args['session'])) {
        var parser = document.createElement('a');
        parser.href = address;

        phantom.addCookie({
          'name': 'sessionid',
          'value': args['session'],
          'domain': parser.hostname
        });
        page.customHeaders = { 'Authorization': 'session '+args['session']};
    }

    page.onError = function(msg, trace) { 
      console.log('Ignoring error', msg, trace);
    }


    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
            //phantom.exit(1);
        } 
        window.setTimeout(function () {
            page.render(output);
            phantom.exit();
        },  10000);
    });
}

