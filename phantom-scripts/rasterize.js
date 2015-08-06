//https://github.com/ariya/phantomjs/blob/master/examples/rasterize.js
var args = require('./minimist.js')(phantom.args);
var b64 = require('./b64.js');

var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

function replaceCssWithComputedStyle(html) {
  return page.evaluate(function(html) {
    var host = document.createElement('div');
    host.setAttribute('style', 'display:none;'); // Silly hack, or PhantomJS will 'blank' the main document for some reason
    host.innerHTML = html;

    // Append to get styling of parent page
    document.body.appendChild(host);

    var elements = host.getElementsByTagName('*');
    // Iterate in reverse order (depth first) so that styles do not impact eachother
    for (var i = elements.length - 1; i >= 0; i--) {
      elements[i].setAttribute('style', window.getComputedStyle(elements[i], null).cssText);
    }

    // Remove from parent page again, so we're clean
    document.body.removeChild(host);
    return host.innerHTML;
  }, html);
}

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
                return replaceCssWithComputedStyle('<span class="footer">' + pageNum + " / " + numPages + '</span>');
            })
        },
    };

    

	if ((typeof header_b64 !== 'undefined') && (header_b64 != null)) {
        pz.header = { 'height':'1cm',
                      'contents': phantom.callback(function (pageNum, numPages) { return replaceCssWithComputedStyle(b64.toString(header_b64)); })
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

