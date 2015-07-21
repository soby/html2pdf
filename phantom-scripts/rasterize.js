//https://github.com/ariya/phantomjs/blob/master/examples/rasterize.js
var page = require('webpage').create(),
    system = require('system'),
    address, output, size;

if (system.args.length < 3 || system.args.length > 5) {
    console.log('Usage: rasterize.js URL filename [paperwidth*paperheight|paperformat] [zoom]');
    console.log('  paper (pdf output) examples: "5in*7.5in", "10cm*20cm", "A4", "Letter"');
    console.log('  image (png/jpg output) examples: "1920px" entire page, window width 1920px');
    console.log('                                   "800px*600px" window, clipped to 800x600');
    phantom.exit(1);
} else {
    address = system.args[1];
    output = system.args[2];
    page.viewportSize = { width: 600, height: 600 };

    page.paperSize = {
	format: "A4",
	orientation: "portrait",

	footer: {
		height: "0.9cm",
		contents: phantom.callback(function (pageNum, numPages) {
			return "<div style='text-align:center;'><small>" + pageNum +
					" / " + numPages + "</small></div>";
		})
	}
    };

    if (system.args.length > 3) {
        var parser = document.createElement('a');
        parser.href = address;

        phantom.addCookie({
          'name': 'sessionid',
          'value': system.args[3],
          'domain': parser.hostname
        });
        page.customHeaders = { 'Authorization': 'session '+system.args[3]};
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

