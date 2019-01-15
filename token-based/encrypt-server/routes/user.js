var express = require('express');
var middleware = require('../middlewares/middleware');
var User   = require('../models/user'); 
var encryp = require('../models/encryp');
var email = require('../services/send');
var router = express.Router();
//var exec = require('child_process').exec;
var service = require('../services/service');
var emailExistence = require('email-existence');
var exec = require('child-process-promise').exec;
var path = require('path');
var fs = require('fs');
//var FormData = require('form-data');
//var multer  = require('multer');
//var upload = multer({ dest: '.'})

function eliminar(){
  exec('rm key.txt').then(function(result){
  })
    .catch(function(err){
    console.error('Error to delete key.txt: ', err);
  });
  exec('rm outencrypt.json').then(function(result){
  })
    .catch(function(err){
    console.error('Error to delete key.txt: ', err);
  });
  exec('rm outdecrypt.txt').then(function(result){
  })
    .catch(function(err){
    console.error('Error to delete key.txt: ', err);
  });
}

function validateEmail(email) {
    var re = /^[(a-z0-9\_\-\.)]+@gmail.com/;
    return re.test(String(email).toLowerCase());
}

function validateurl(url) {
    var re = /^(?:http(s)?:\/\/)*[\w\_\-\.]+[:]?[0-9]*\/v2\/entities$/;
    return re.test(String(url).toLowerCase());
}

//Route (GET http://localhost:3000/service)
router.get('/', function(req, res) {
  res.json({ message: 'this is an api to encrypt / decrypt orion data models, please signup' });
});

/*
router.get('/users', function(req, res) {
  User.find({}, function(err, users) {
    res.json(users);
  });
});*/   

//https://itnext.io/how-to-handle-the-post-request-body-in-node-js-without-using-a-framework-cd2038b93190

//regist users
router.post('/signup', function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.name || !req.body.email){
    return res.status(409).send({ message: 'Please enter name and email'});
  }
  if(validateEmail(req.body.email)){

    emailExistence.check(req.body.email, function(error, response){
      if(response){
        
        User.findOne({ name: req.body.name }, function(err, existingUser){
          if(existingUser){
            return res.status(409).send({ message: 'Name is alredy taken'});
          }else{
            User.findOne({ email: req.body.email }, function(err, existingemail){
              if(existingemail){
                return res.status(409).send({ message: 'Email is alredy taken'});
              }
              var user = new User({
                name: req.body.name,
                email: req.body.email
              });
              user.save(function(err, result){
                if(err){
                  res.status(500).send({ message: err.message, service: "error in User or Email" });
                  throw err;
                }
                res.send({
                  success: true,
                  message: 'Enjoy your token!',
                  token: service.createToken(user)
                });
              });
            });
          } 
        });

      }else{
        return res.status(409).send({ message: 'The email no exists'});
      }
    });

  }
  else{
    return res.status(500).send({message: "error, use a gmail account" });
  }
});

// Route to authenticate a user (POST http://localhost:8000/service/authenticate)
router.post('/authenticate', function(req, res) {
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.name || !req.body.email){
    return res.status(409).send({ message: 'Please enter name and email'});
  }

  //find the user
  User.findOne( {name: req.body.name }, function(err, user) {
    if (err) throw err;
    if (!user) {
      res.json({ success: false, message: 'Authentication failed. User not found.' });
    }else if (user) {

      // check if email matches
      if (user.email != req.body.email) {
        res.json({ success: false, message: 'Authentication failed. Wrong email.' });
      } else {

        // return the information including token as JSON
        res.json({
          success: true,
          message: 'Enjoy your token!',
          token: service.createToken(user)
        });
      }
    }
  });
});

//routes encrypt -------------------------------------------------------------------------------------

//encryp route
router.post('/encrypt/ocb',middleware.ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.urlFrom || !req.body.id || !req.body.type || !req.body.urlTo){
    return res.status(409).send({ message: 'Please enter urlFrom, id, type and urlTo'});
  }
  if(!(validateurl(req.body.urlFrom))){
    console.log(validateurl(req.body.urlFrom));
    return res.status(500).send({ message: 'Please enter a urlFrom valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  if(!(validateurl(req.body.urlTo))){
    return res.status(500).send({ message: 'Please enter a urlTo valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  eliminar();
  var token = req.headers.authorization;
  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }

    var urlin = req.body.urlFrom + '/'+ req.body.id + '?type=' + req.body.type;
    var urlout = req.body.urlTo + '/'+ req.body.id + '?type=' + req.body.type;

    var add = encryp({
      name: obj.name,
      urlFrom: urlin,
      urlTo: req.body.urlTo,
      service: "encrypt-ocb"
    });

    exec('wget -O ine.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlin + '&& jsonlint ine.json && jq . ine.json > inencrypt.json').then(function(result){
      var conte = fs.readFileSync('inencrypt.json', 'utf8');

      exec('wget -O orion.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlout + '&& jsonlint orion.json').then(function(resul){
        res.json({error : "Orion urlTo, server not found or id alredy exist"});
        
      })
      .catch(function(err){
        console.error('Error to find the orion urlin: ', err);
        
        exec('java -jar encryptJSON.jar').then(function(result1){

        }).then(function(result2){
          var content = fs.readFileSync('outencrypt.json', 'utf8');
          exec(`curl `+req.body.urlTo+` -s -S --header 'Content-Type: application/json' --header 'Fiware-Service: default' --header 'Fiware-ServicePath: /' -d @- <<EOF \n`+ content+ `EOF`).then(function(result3){
            
          }).then(function(save){
            add.save(function(err) {
              if (err) throw err;
            });
            email.sendemail(obj.name, obj.email, req.body.id, req.body.type, req.body.urlTo);
          }).then(function(elim){
            res.send(content);
          })
          .catch(function(err){
            console.error('Error to send the orion urlTo: ', err);
            res.json({error : "Error to send the Orion urlTo"});
          });

        })
        .catch(function(err){
          console.error('Error encryption failed: ', err);
          res.json({Error : "encryption failed"});
        });

      });

    })
    .catch(function(err){
      console.error('Error to find the orion urlin: ', err);
      res.json({error : "Orion urlFrom, entitie not found"});
    });
  });
});

//only encryp
//npm install jsonlint -g
router.post('/encrypt',middleware.ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.json){
    return res.status(409).send({ message: 'Please enter json'});
  }
  eliminar();
  var token = req.headers.authorization;
  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }
    var add = encryp({
      name: obj.name,
      service: "encrypt"
    });

    fs.writeFile('inencrypt.json', req.body.json, function (err) {
      if (err) throw err;
      console.log('Saved!');
    });

    exec('jsonlint inencrypt.json').then(function(result){

      exec('java -jar encryptJSON.jar').then(function(result){

      }).then(function(save){
        var contentjson = fs.readFileSync('outencrypt.json', 'utf8');
        res.send(contentjson);
        email.onlysendemail(obj.name, obj.email);
      }).then(function(data){
        add.save(function(err) {
          if (err) throw err;
        });
      })
      .catch(function(err){
        console.error('Error encryption failed: ', err);
        res.json({Error : "encryption failed"});
      });

    })
    .catch(function(err){
        console.error('Error encryption failed: ', err);
        res.json({Error : "json not valid"});
      });
  })
});

//routes decrypt -------------------------------------------------------------------------------------

//dencryp route
router.post('/decrypt/ocb',middleware.ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.urlFrom || !req.body.id || !req.body.type || !req.body.urlTo || !req.body.key){
    return res.status(409).send({ message: 'Please enter urlFrom, id, type, urlTo and key'});
  }
  if(!(validateurl(req.body.urlFrom))){
    return res.status(500).send({ message: 'Please enter urlFrom valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  if(!(validateurl(req.body.urlTo))){
    return res.status(500).send({ message: 'Please enter urlTo valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  eliminar();

  var urlin = req.body.urlFrom+ '/'+ req.body.id + '?type=' + req.body.type;
  var urlout = req.body.urlTo + '/'+ req.body.id + '?type=' + req.body.type;

  var token = req.headers.authorization;
  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }

    var add = encryp({
      name: obj.name,
      urlFrom: urlin,
      urlTo: req.body.urlTo,
      service: "decrypt-ocb"
    });

    exec('wget -O ind.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlin + '&& jsonlint ind.json && jq . ind.json > indecrypt.json ').then(function(result){
      fs.writeFile('key.txt', req.body.key, function (err) {
        if (err) throw err;
        console.log('Saved keys!');
      });
      exec('wget -O dorion.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlout + '&& jsonlint dorion.json').then(function(result){
        res.json({error : "Orion urlTo, server not found or id alredy exist"});

      })
      .catch(function(err){
        console.error('Error to find the orion urlout: ', err);

        exec('java -jar decryptJSON.jar').then(function(result1){

        }).then(function(result2){
          var content = fs.readFileSync('outdecrypt.json', 'utf8');
          res.send(content);

          exec(`curl `+req.body.urlTo+` -s -S --header 'Content-Type: application/json' --header 'Fiware-Service: default' --header 'Fiware-ServicePath: /' -d @- <<EOF \n`+ content+ `EOF`).then(function(result3){

          }).then(function(save){
            add.save(function(err) {
              if (err) throw err;
            });
          })
          .catch(function(err){
            console.error('Error to send the orion urlTo: ', err);
            res.json({error : "Error to send the Orion urlTo"});
          });

        })
        .catch(function(err){
          console.error('Error decryption failed: ', err);
          res.json({ error : "decryption failed, invalid keys" });
        });

      });

    })
    .catch(function(err){
      console.error('Error to find the orion urlin: ', err);
      res.json({error : "Orion urlFrom, entitie not found"});
    });
  });
});

//only dencryp
//npm install jsonlint -g
router.post('/decrypt',middleware.ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.json || !req.body.key){
    return res.status(409).send({ message: 'Please enter json and key'});
  }
  var token = req.headers.authorization;
  eliminar();
  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }
    var add = encryp({
      name: obj.name,
      service: "decrypt"
    });

    fs.writeFile('indecrypt.json', req.body.json, function (err) {
      if (err) throw err;
      console.log('Saved json!');
    });
    fs.writeFile('key.txt', req.body.key, function (err) {
      if (err) throw err;
      console.log('Saved keys!');
    });

    exec('jsonlint indecrypt.json').then(function(result){

      exec('java -jar decryptJSON.jar').then(function(result){

      }).then(function(save){
        var contentjson = fs.readFileSync('outdecrypt.json', 'utf8');
        res.send(contentjson);
      }).then(function(data){
        add.save(function(err) {
          if (err) throw err;
        });
      })
      .catch(function(err){
        console.error('Error dencrypt failed: ', err);
        res.json({Error : "decrypt failed"});
      });

    })
    .catch(function(err){
        console.error('Error decrypt failed: ', err);
        res.json({Error : "json not valid"});
      });
  })
});

//routes encrypt/decrypt orion to local -------------------------------------------------------------------------------------

router.post('/encrypt/ocb-local', middleware. ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.urlFrom || !req.body.id || !req.body.type){
    return res.status(409).send({ message: 'Please enter urlFrom, id, type'});
  }
  if(!(validateurl(req.body.urlFrom))){
    return res.status(500).send({ message: 'Please enter urlFrom valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  eliminar();

  var urlin = req.body.urlFrom+ '/'+ req.body.id + '?type=' + req.body.type;

  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }

    var add = encryp({
      name: obj.name,
      urlFrom: urlin,
      service: "encrypt-ocb-local"
    });

    exec('wget -O ine.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlin + '&& jsonlint ine.json && jq . ine.json > inencrypt.json ').then(function(result){

      exec('java -jar encryptJSON.jar').then(function(result1){

      }).then(function(result2){
        var content = fs.readFileSync('outencrypt.json', 'utf8');
        res.send(content);
        email.sendemailocb_local(obj.name, obj.email, req.body.id, req.body.type);

      }).catch(function(err){
        console.error('Error encryption failed: ', err);
        res.json({ error : "encryption failed" });
      });

    })
    .catch(function(err){
      console.error('Error to find the orion urlFrom: ', err);
      res.json({error : "Orion urlFrom, entitie not found"});
    });
  });
});

router.post('/decrypt/ocb-local', middleware. ensureAuthenticated, function(req, res){
  const FORM_URLENCODED = 'application/x-www-form-urlencoded';
  if(!(req.headers['content-type'] === FORM_URLENCODED)) {
    return res.status(500).send({ message: 'Please use a x-www-form-urlencoded'});
  }
  if(!req.body.urlFrom || !req.body.id || !req.body.type){
    return res.status(409).send({ message: 'Please enter urlFrom, id, type'});
  }
  if(!(validateurl(req.body.urlFrom))){
    return res.status(500).send({ message: 'Please enter urlFrom valid', example: 'http://192.168.0.1:1026/v2/entities'});
  }
  eliminar();

  var urlin = req.body.urlFrom+ '/'+ req.body.id + '?type=' + req.body.type;

  User.findOne({ _id: req.user }, function(err, obj){
    if (err) throw err;
    if (!obj) {
      return res.status(500).send({ message: 'Unregistered user'});
    }

    var add = encryp({
      name: obj.name,
      urlFrom: urlin,
      service: "decrypt-ocb-local"
    });

    exec('wget -O ind.json -d --header="Accept: application/json" --header="Fiware-Service: default" --header="Fiware-ServicePath: /" '+ urlin + '&& jsonlint ind.json && jq . ind.json > indecrypt.json ').then(function(result){

      exec('java -jar decryptJSON.jar').then(function(result1){

      }).then(function(result2){
        var content = fs.readFileSync('outdecrypt.json', 'utf8');
        res.send(content);
        email.sendemailocb_local(obj.name, obj.email, req.body.id, req.body.type);

      }).catch(function(err){
        console.error('Error decryption failed: ', err);
        res.json({ error : "decryption failed" });
      });

    })
    .catch(function(err){
      console.error('Error to find the orion urlin: ', err);
      res.json({error : "Orion urlFrom, entitie not found"});
    });
  });
});

module.exports = router;
