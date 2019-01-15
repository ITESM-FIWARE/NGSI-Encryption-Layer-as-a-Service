var express = require('express');
var bodyParser = require('body-parser');
var mongoose = require('mongoose');
var methodOverride = require("method-override");
var app = express();
var User   = require('./models/user'); 
var service = require('./services/service');
var api = require('./routes/user');

// Connection to DB
// docker-compose static ip
// var mongodb = "172.16.238.10"
// docker-compose environment ip
var mongodb = process.env.MONGODB_PORT_27017_TCP_ADDR + "";
// var mongodb = "localhost"
mongoose.connect('mongodb://'+mongodb+':27017/encryp-users', function(err, res) {
 if(err) throw err;
 console.log('Connected to Database');
});

// Middlewares
app.use(bodyParser.urlencoded({ extended: true }));  
//app.use(bodyParser.json());  
app.use(methodOverride());

// =======================
// Routes ================
// =======================

app.get('/', function(req, res) {
    res.send('this is an api to encrypt / decrypt orion data models');
});

app.use('/', api);

// Start server
app.listen(8000, function() {
  console.log("Server running on http://localhost:8000");
});
