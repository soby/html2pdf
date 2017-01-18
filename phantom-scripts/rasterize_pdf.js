var page = new WebPage(),
    address, output, size;
 
if (phantom.args.length < 2 || phantom.args.length > 3) {
    console.log('Usage: rasterize.js URL filename');
    phantom.exit();
} else {
    address = phantom.args[0];
    output = phantom.args[1];
		
		page.paperSize = {
			format: 'A4',
			orientation: 'portrait',
			border: '1.5cm'
			header: {
            height: "1cm",
            contents: phantom.callback(function(pageNum, numPages) {
                return "<div><img src="http://files.parsetfss.com/54314910-905e-4901-af3c-56382e52a40e/tfss-89f75112-5812-4d65-8d51-0a947b2ecb71-st_logo.gif" style="text-align:left; display: block "/></div>";
            })
        }

			footer: {
            height: "1cm",
            contents: phantom.callback(function(pageNum, numPages) {
                if (pageNum == numPages) {
                    return "";
                }
                return "<h4 style="text-align:center; display: block ">" + pageNum + " / " + numPages + "</h4>";
            })
        }

		};

    page.onConsoleMessage = function(msg) { console.log(msg); };
    page.settings.userAgent = 'Mozilla/5.0 (Windows NT 6.0; WOW64) AppleWebKit/535.7 (KHTML, like Gecko) Chrome/16.0.912.75 Safari/535.7';
    page.open(address, function (status) {
        if (status !== 'success') {
            console.log('Unable to load the address!');
        } else {
            window.setTimeout(function () {
                page.render(output);
                phantom.exit();
            }, 50);
        }
    });
}