var fs = require('fs');
var idGenerator = require('shortid');
var bodyParser = require('body-parser');
var multer = require('multer');
// var io = require('socket.io')(app);
// var morgan = require('morgan');
var express = require('express');
var app = express();
// var upload = multer({ dest: './tmp/' });
// app.use(bodyParser.urlencoded({ extended: false }));
// app.use(bodyParser.json());

// app.use(morgan('dev'));
// app.use(multer({dest:'./tmp/'}));

// respond with "hello world" when a GET request is made to the homepage
app.get('/login', function(req, res) {
    console.log("YAHAN AAYA");
    res.end(idGenerator.generate());
});

app.post('/zip', upload.single('file'), function(req, res) {
    console.log(req.body);
    var file = __dirname + "/uploads/"+ req.body.id + "/" + 'files.zip';
    fs.readFile(req.file.path, function(err, data) {
        fs.mkdir(__dirname + '/' + req.body.id, function(err) {
            if (err)
                console.log(err);
            else {
                fs.writeFile(file, data, function(err) {
                    if (err) {
                        console.log(err);
                    } else {
                        response = {
                            message: 'File uploaded successfully',
                            filename: req.files.file.name
                        };

                    }
                    console.log(response);
                    res.json(response);
                    run_cmd('unzip', ['-a', file], function(output) {
                        console.log('output is', output);
                    });
                });
            }
        });

    });
});

app.listen(2000, function() {
    console.log('Server running');
});

function run_cmd(cmd, args, callBack) {
    var spawn = require('child_process').spawn;
    var child = spawn(cmd, args);
    var resp = "";

    child.stdout.on('data', function(buffer) { resp += buffer.toString(); });
    child.stdout.on('end', function() { callBack(resp); });
}

// run_cmd('host',['www.google.com'],function(output){
//     console.log("the output is: \n" + output);
// })
