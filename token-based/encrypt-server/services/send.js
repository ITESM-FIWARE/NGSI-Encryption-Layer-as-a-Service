// Require'ing module and setting default options
exports.sendemail = function(user, email, id, type ,url){

  var send = require('gmail-send')({
    user: process.env.ngsi_address_send + "",
    pass: process.env.ngsi_encrypt_pass+ "",
    to:   email,
    // to:   credentials.user,                  // Send to yourself
                                             // you also may set array of recipients:
                                             // [ 'user1@gmail.com', 'user2@gmail.com' ]
    // from:    credentials.user,            // from: by default equals to user
    // replyTo: credentials.user,            // replyTo: by default undefined
    // bcc: 'some-user@mail.com',            // almost any option of `nodemailer` will be passed to it
    subject: 'test subject',
    text:    'Keys RSA \n urlTo : ' + url + '\n id : ' + id + '\n type : ' + type,         // Plain text
    //html:    '<b>html text</b>'            // HTML
  });
   
  // Override any default option and send email
   
  var filepath = 'key.txt';  // File to attach
   
  /*
  send({ // Overriding default parameters
    subject: 'Encryp Layer',         // Override value set as default
    files: [ filepath ],
  }, function (err, res) {
    console.log('*1 send() callback returned: err:', err, '; res:', res);
  }); */
   
  send({ // Overriding default parameters
    subject: user,              // Override value set as default
    files: [                                    // Array of files to attach
      {
        path: filepath,
        filename: 'key.txt' // You can override filename in the attachment if needed
      }
    ],
  }, function (err, res) {
    console.log('*2 send() callback returned: err:', err, '; res:', res);
  });
}

exports.onlysendemail = function(user, email){
  console.log(user, email);
  var send = require('gmail-send')({
  //var send = require('../index.js')({
    user: process.env.ngsi_address_send + "",
    pass: process.env.ngsi_encrypt_pass+ "",
    to:   email,
    // to:   credentials.user,                  // Send to yourself
                                             // you also may set array of recipients:
                                             // [ 'user1@gmail.com', 'user2@gmail.com' ]
    // from:    credentials.user,            // from: by default equals to user
    // replyTo: credentials.user,            // replyTo: by default undefined
    // bcc: 'some-user@mail.com',            // almost any option of `nodemailer` will be passed to it
    subject: 'test subject',
    text:    'Keys RSA ',         // Plain text
    //html:    '<b>html text</b>'            // HTML
  });
   
  // Override any default option and send email
   
  var filepath = 'key.txt';  // File to attach
   
  /*
  send({ // Overriding default parameters
    subject: 'Encryp Layer',         // Override value set as default
    files: [ filepath ],
  }, function (err, res) {
    console.log('*1 send() callback returned: err:', err, '; res:', res);
  }); */
   
  send({ // Overriding default parameters
    subject: user,              // Override value set as default
    files: [                                    // Array of files to attach
      {
        path: filepath,
        filename: 'key.txt' // You can override filename in the attachment if needed
      }
    ],
  }, function (err, res) {
    console.log('*2 send() callback returned: err:', err, '; res:', res);
  });
}

exports.sendemailocb_local = function(user, email, id, type){

  var send = require('gmail-send')({
    user: process.env.ngsi_address_send + "",
    pass: process.env.ngsi_encrypt_pass+ "",
    to:   email,
    // to:   credentials.user,                  // Send to yourself
                                             // you also may set array of recipients:
                                             // [ 'user1@gmail.com', 'user2@gmail.com' ]
    // from:    credentials.user,            // from: by default equals to user
    // replyTo: credentials.user,            // replyTo: by default undefined
    // bcc: 'some-user@mail.com',            // almost any option of `nodemailer` will be passed to it
    subject: 'test subject',
    text:    'Keys RSA \n' + '\n id : ' + id + '\n type : ' + type,         // Plain text
    //html:    '<b>html text</b>'            // HTML
  });
   
  // Override any default option and send email
   
  var filepath = 'key.txt';  // File to attach
   
  /*
  send({ // Overriding default parameters
    subject: 'Encryp Layer',         // Override value set as default
    files: [ filepath ],
  }, function (err, res) {
    console.log('*1 send() callback returned: err:', err, '; res:', res);
  }); */
   
  send({ // Overriding default parameters
    subject: user,              // Override value set as default
    files: [                                    // Array of files to attach
      {
        path: filepath,
        filename: 'key.txt' // You can override filename in the attachment if needed
      }
    ],
  }, function (err, res) {
    console.log('*2 send() callback returned: err:', err, '; res:', res);
  });
}
